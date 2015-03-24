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
    'java-common.gypi',
  ],

  'variables': {
    'local_root': '<(platform_root)/libcore',
  },

  'targets': [
    {
      'target_name': 'libcore-rt_jar',
      'type': 'none',

      'variables': {
        'jar_file': '<!(<(jar_file_v) rt)',
        'dex_file': '<!(<(dex_file_v) rt)',

        'compile_jar.source_paths': [
          '<(local_root)/luni/src/main/java',
          '<(local_root)/libart/src/main/java',
          '<(local_root)/dalvik/src/main/java',
          '<(local_root)/dex/src/main/java',
          '<(local_root)/xml/src/main/java',
        ],
        'compile_jar.resource_paths': [
          '<(local_root)/luni/src/main/java',
          '<(local_root)/luni/src/main/resources',
        ],
        'compile_jar.boot_class_paths': [ ':' ],
        'compile_jar.jar_file': '<(jar_file)',

        'dex.jar_file': '<(jar_file)',
        'dex.dex_file': '<(dex_file)',
        'dex.core_library': 1,
      },
      'includes': [ 'utils/compile_jar.gypi', 'utils/dex.gypi' ],
    }
  ]
}