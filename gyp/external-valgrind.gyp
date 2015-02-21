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
    'common.gypi'
  ],

  'variables': {
    'local_root': '<(platform_root)/external/valgrind',
  },

  'targets': [
    {
      'target_name': 'external-valgrind',
      'product_name': 'valgrind',
      'type': 'none',

      'direct_dependent_settings': {
        'include_dirs': [
          '<(local_root)/main/include',
          '<(local_root)/main', # for <memcheck/memcheck.h>
        ],
      },
    },
  ],
}
