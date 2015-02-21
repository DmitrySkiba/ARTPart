# Copyright (C) 2015 Dmitry Skiba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

{
  'includes': [
    'common.gypi',
  ],

  'variables': {
    'local_root': '<(platform_root)/libcore',
  },

  'targets': [
    {
      'target_name': 'libcore-libjavacore',
      'product_name': 'libjavacore',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) system-liblog)',
        '<!(<(dependency) system-include)',
        '<!(<(dependency) libnativehelper)',
        '<!(<(dependency) external-openssl)',
        '<!(<(dependency) external-icu4c)',
        '<!(<(dependency) external-expat)',
        '<!(<(dependency) external-fdlibm)',
        '<!(<(dependency) zlib)',
      ],

      'include_dirs': [
        '<(local_root)/include',
      ],

      # TODO not needed / fixable?
      'xcode_settings': {
        'CLANG_CXX_LANGUAGE_STANDARD': 'gnu++0x',
      },

      'sources': [
        '<(local_root)/dalvik/src/main/native/org_apache_harmony_dalvik_NativeTestTarget.cpp',

        '<(local_root)/luni/src/main/native/AsynchronousCloseMonitor.cpp',
        '<(local_root)/luni/src/main/native/ExecStrings.cpp',
        '<(local_root)/luni/src/main/native/IcuUtilities.cpp',
        '<(local_root)/luni/src/main/native/JniException.cpp',
        '<(local_root)/luni/src/main/native/NetworkUtilities.cpp',
        '<(local_root)/luni/src/main/native/Register.cpp',
        '<(local_root)/luni/src/main/native/ZipUtilities.cpp',
        '<(local_root)/luni/src/main/native/android_system_OsConstants.cpp',
        '<(local_root)/luni/src/main/native/canonicalize_path.cpp',
        '<(local_root)/luni/src/main/native/cbigint.cpp',
        '<(local_root)/luni/src/main/native/java_io_File.cpp',
        '<(local_root)/luni/src/main/native/java_io_FileDescriptor.cpp',
        '<(local_root)/luni/src/main/native/java_io_ObjectStreamClass.cpp',
        '<(local_root)/luni/src/main/native/java_lang_Character.cpp',
        '<(local_root)/luni/src/main/native/java_lang_Double.cpp',
        '<(local_root)/luni/src/main/native/java_lang_Float.cpp',
        '<(local_root)/luni/src/main/native/java_lang_Math.cpp',
        '<(local_root)/luni/src/main/native/java_lang_ProcessManager.cpp',
        '<(local_root)/luni/src/main/native/java_lang_RealToString.cpp',
        '<(local_root)/luni/src/main/native/java_lang_StrictMath.cpp',
        '<(local_root)/luni/src/main/native/java_lang_StringToReal.cpp',
        '<(local_root)/luni/src/main/native/java_lang_System.cpp',
        '<(local_root)/luni/src/main/native/java_math_NativeBN.cpp',
        '<(local_root)/luni/src/main/native/java_nio_ByteOrder.cpp',
        '<(local_root)/luni/src/main/native/java_nio_charset_Charsets.cpp',
        '<(local_root)/luni/src/main/native/java_text_Bidi.cpp',
        '<(local_root)/luni/src/main/native/java_util_jar_StrictJarFile.cpp',
        '<(local_root)/luni/src/main/native/java_util_regex_Matcher.cpp',
        '<(local_root)/luni/src/main/native/java_util_regex_Pattern.cpp',
        '<(local_root)/luni/src/main/native/java_util_zip_Adler32.cpp',
        '<(local_root)/luni/src/main/native/java_util_zip_CRC32.cpp',
        '<(local_root)/luni/src/main/native/java_util_zip_Deflater.cpp',
        '<(local_root)/luni/src/main/native/java_util_zip_Inflater.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_AlphabeticIndex.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_DateIntervalFormat.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_ICU.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeBreakIterator.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeCollation.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeConverter.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeDecimalFormat.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeIDN.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativeNormalizer.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_NativePluralRules.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_TimeZoneNames.cpp',
        '<(local_root)/luni/src/main/native/libcore_icu_Transliterator.cpp',
        '<(local_root)/luni/src/main/native/libcore_io_AsynchronousCloseMonitor.cpp',
        '<(local_root)/luni/src/main/native/libcore_io_Memory.cpp',
        '<(local_root)/luni/src/main/native/libcore_io_Posix.cpp',
        '<(local_root)/luni/src/main/native/org_apache_harmony_xml_ExpatParser.cpp',
        '<(local_root)/luni/src/main/native/readlink.cpp',
        '<(local_root)/luni/src/main/native/sun_misc_Unsafe.cpp',
        '<(local_root)/luni/src/main/native/valueOf.cpp',
      ],
    },
  ],
}
