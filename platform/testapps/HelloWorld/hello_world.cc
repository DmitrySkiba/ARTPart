/*
 * Copyright (C) 2015 Dmitry Skiba
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdlib.h>
#include <jni.h>

extern "C" bool RunJava(const char* oat_location, const char* class_name, const char* const* arguments);

int main(int argc, const char* const* argv) {
  const char* arguments[] = {nullptr};
  return !RunJava(APP_OAT_PATH, "HelloWorld", arguments);
}

extern "C" JNIEXPORT jint HelloWorld_JNI_OnLoad(JavaVM* vm, void*) {
  return JNI_VERSION_1_6;
}

extern "C" JNIEXPORT void JNICALL Java_HelloWorld_nativeMain(JNIEnv* env, jclass clazz, jarray args) {
  jmethodID sayHello = env->GetStaticMethodID(clazz, "sayHello", "()V");
  env->CallStaticVoidMethod(clazz, sayHello);
}
