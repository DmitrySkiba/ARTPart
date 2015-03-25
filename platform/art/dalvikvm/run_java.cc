#include <signal.h>

#include <cstdio>
#include <cstring>
#include <string>

#include "jni.h"
#include "ScopedLocalRef.h"
#include "toStringArray.h"
#include "UniquePtr.h"

#include "scoped_thread_state_change.h"
#include "class_linker.h"
#include "mirror/class_loader.h"

#include <utils/String8.h>
#ifdef __APPLE__
#include <mach-o/dyld.h>
#endif

// Determine whether or not the specified method is public.
static bool IsMethodPublic(JNIEnv* env, jclass c, jmethodID method_id) {
  ScopedLocalRef<jobject> reflected(env, env->ToReflectedMethod(c, method_id, JNI_FALSE));
  if (reflected.get() == NULL) {
    fprintf(stderr, "Failed to get reflected method\n");
    return false;
  }
  // We now have a Method instance.  We need to call its
  // getModifiers() method.
  jclass method_class = env->FindClass("java/lang/reflect/Method");
  if (method_class == NULL) {
    fprintf(stderr, "Failed to find class java.lang.reflect.Method\n");
    return false;
  }
  jmethodID mid = env->GetMethodID(method_class, "getModifiers", "()I");
  if (mid == NULL) {
    fprintf(stderr, "Failed to find java.lang.reflect.Method.getModifiers\n");
    return false;
  }
  int modifiers = env->CallIntMethod(reflected.get(), mid);
  static const int PUBLIC = 0x0001;  // java.lang.reflect.Modifiers.PUBLIC
  if ((modifiers & PUBLIC) == 0) {
    return false;
  }
  return true;
}

static bool InvokeMain(JNIEnv* env, const char* class_name, const char* const* arguments) {
  ScopedLocalRef<jobjectArray> args(env, toStringArray(env, arguments));
  if (args.get() == NULL) {
    env->ExceptionDescribe();
    return false;
  }

  // Find [class].main(String[]).

  // Convert "com.android.Blah" to "com/android/Blah".
  std::string klass_name(class_name);
  std::replace(klass_name.begin(), klass_name.end(), '.', '/');

  ScopedLocalRef<jclass> klass(env, env->FindClass(klass_name.c_str()));
  if (klass.get() == NULL) {
    fprintf(stderr, "Unable to locate class '%s'\n", klass_name.c_str());
    env->ExceptionDescribe();
    return false;
  }

  jmethodID method = env->GetStaticMethodID(klass.get(), "main", "([Ljava/lang/String;)V");
  if (method == NULL) {
    fprintf(stderr, "Unable to find static main(String[]) in '%s'\n", klass_name.c_str());
    env->ExceptionDescribe();
    return false;
  }

  // Make sure the method is public.  JNI doesn't prevent us from
  // calling a private method, so we have to check it explicitly.
  if (!IsMethodPublic(env, klass.get(), method)) {
    fprintf(stderr, "Sorry, main() is not public in '%s'\n", klass_name.c_str());
    env->ExceptionDescribe();
    return false;
  }

  // Invoke main().
  env->CallStaticVoidMethod(klass.get(), method, args.get());

  // Check whether there was an uncaught exception. We don't log any uncaught exception here;
  // detaching this thread will do that for us, but it will clear the exception (and invalidate
  // our JNIEnv), so we need to check here.
  return env->ExceptionCheck();
}

extern "C" bool LoadApp(JNIEnv* env, const char* oat_location) {
  using namespace art;

  ScopedObjectAccess soa(env);
  StackHandleScope<1> hs(soa.Self());

  ClassLinker* linker = Runtime::Current()->GetClassLinker();
  Handle<mirror::ClassLoader> class_loader(hs.NewHandle(soa.Decode<mirror::ClassLoader*>(
    Runtime::Current()->GetSystemClassLoader())));

  std::string error_msg;
  OatFile* oat_file = OatFile::Open(oat_location, oat_location, nullptr, nullptr, false, &error_msg); //OatFile::OpenLinked("app");
  if (!oat_file) {
    fprintf(stderr, "Failed to open app oat file: %s\n", error_msg.c_str());
    return false;
  }

  linker->RegisterOatFile(oat_file);

  for (auto oat_dex_file: oat_file->GetOatDexFiles()) {
    const DexFile* dex_file = oat_dex_file->OpenDexFile(&error_msg);
    if (!dex_file) {
      fprintf(stderr, "Failed to open dex file '%s', error: %s.\n", oat_dex_file->GetDexFileLocation().c_str(), error_msg.c_str());
      return false;
    }

    linker->RegisterDexFile(*dex_file);

    for (size_t i = 0, e = dex_file->NumClassDefs(); i != e; ++i) {
      const DexFile::ClassDef& descriptor = dex_file->GetClassDef(i);
      std::string descriptor_string = dex_file->GetClassDescriptor(descriptor);
      const size_t hash(ComputeModifiedUtf8Hash(descriptor_string.c_str()));
      linker->DefineClass(soa.Self(),
                          descriptor_string.c_str(),
                          ComputeModifiedUtf8Hash(descriptor_string.c_str()),
                          class_loader,
                          *dex_file,
                          descriptor);
    }
  }

  return true;
}

extern "C" bool RunJava(const char* oat_location, const char* class_name, const char* const* arguments) {
  setvbuf(stderr, NULL, _IONBF, 0);

  android::String8 android_data;
  if (!getenv("ANDROID_FS_ROOT")) {
    android::String8 my_path;
#ifdef __APPLE__
    {
      uint32_t length = 128;
      if (_NSGetExecutablePath(my_path.lockBuffer(length), &length) &&
          _NSGetExecutablePath(my_path.lockBuffer(length), &length))
      {
        fprintf(stderr, "Failed to get executable path\n");
        return false;
      }
      my_path.unlockBuffer();
    }
#else
    #error TODO: get executable path for the platform
#endif

    android::String8 my_dir = my_path.getPathDir();

    android::String8 android_fs = my_dir.appendPathCopy("android_fs");
    android::String8 android_root = android_fs.appendPathCopy("system");
    android_data = android_fs.appendPathCopy("data");

    setenv("ANDROID_FS_ROOT", android_fs, true);
    setenv("ANDROID_ROOT", android_root, true);
    setenv("ANDROID_DATA", android_data, true);
  } else {
    android_data = getenv("ANDROID_DATA");
  }

  android::String8 optionString;
  optionString += "-Ximage:";
  optionString += android_data.appendPathCopy("dalvik-cache/boot.art");

  JavaVMOption options[3];
  options[0].optionString = optionString;
  options[1].optionString = "-Xnorelocate";
  options[2].optionString = "-XX:DisableHSpaceCompactForOOM";

  JavaVMInitArgs init_args;
  init_args.version = JNI_VERSION_1_6;
  init_args.options = options;
  init_args.nOptions = arraysize(options);
  init_args.ignoreUnrecognized = JNI_FALSE;

  // Start the runtime. The current thread becomes the main thread.
  JavaVM* vm = NULL;
  JNIEnv* env = NULL;
  if (JNI_CreateJavaVM(&vm, &env, &init_args) != JNI_OK) {
    fprintf(stderr, "Failed to initialize runtime (check log for details)\n");
    return false;
  }

  bool success = LoadApp(env, oat_location) && InvokeMain(env, class_name, arguments);

#if defined(NDEBUG)
  // The DestroyJavaVM call will detach this thread for us. In debug builds, we don't want to
  // detach because detaching disables the CheckSafeToLockOrUnlock checking.
  if (vm->DetachCurrentThread() != JNI_OK) {
    fprintf(stderr, "Warning: unable to detach main thread\n");
    success = false;
  }
#endif

  if (vm->DestroyJavaVM() != 0) {
    fprintf(stderr, "Warning: runtime did not shut down cleanly\n");
    success = false;
  }

  return success;
}
