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
    'local_root': '<(platform_root)/external/conscrypt',
  },

  'targets': [
    {
      'target_name': 'external-conscrypt_jar',
      'type': 'none',

      'dependencies': [
        '<!(<(dependency) libcore-rt_jar)',
      ],

      'variables': {
        'jar_path': '<!(<(jar_path_v) conscrypt)',
        'dex_path': '<!(<(dex_path_v) conscrypt)',

        'compile_jar.source_paths': [
          '<(local_root)/src/main/java',
          '<(local_root)/src/platform/java',
        ],
        'compile_jar.boot_class_paths': '>(dependencies.jar_files)',
        'compile_jar.jar_file': '<(jar_path)',
        'compile_jar.jarjar_tool': '<(jarjar_tool)',
        'compile_jar.jarjar_rules_file': '<(local_root)/jarjar-rules.txt',

        'dex.jar_file': '<(jar_path)',
        'dex.dex_file': '<(dex_path)',
      },
      'includes': [ 'utils/compile_jar.gypi', 'utils/dex.gypi' ],
    }
  ]
}