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
    'system-common.gypi',
  ],

  'variables': {
    'local_root': '<(system_root)/libcorkscrew',
  },

  'targets': [
    {
      'target_name': 'system-libcorscrew<(any_variant)',
      'product_name': 'libcorscrew',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) system-liblog)',
      ],

      'sources': [
        '<(local_root)/backtrace.c',
        '<(local_root)/backtrace-helper.c',
        '<(local_root)/map_info.c',
        '<(local_root)/ptrace.c',
        '<(local_root)/symbol_table.c',
        '<(local_root)/arch-x86/backtrace-x86.c',
      ],
    },
  ],
}
