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
    'local_root': '<(platform_root)/external/gtest',
  },

  'targets': [
    {
      'target_name': 'external-gtest-include',
      'type': 'none',

      'direct_dependent_settings': {
        'include_dirs': [
          '<(local_root)/include',
        ],
        'defines': [
          'GTEST_USE_OWN_TR1_TUPLE=1',
        ],
      },
    },
    {
      'target_name': 'external-gtest',
      'product_name': 'gtest',
      'type': 'static_library',

      'dependencies': [
        'external-gtest-include',
      ],

      'export_dependent_settings': [
        'external-gtest-include',
      ],

      'include_dirs': [
        '<(local_root)',
      ],

      'sources': [
        '<(local_root)/src/gtest.cc',
        '<(local_root)/src/gtest-death-test.cc',
        '<(local_root)/src/gtest-filepath.cc',
        '<(local_root)/src/gtest-port.cc',
        '<(local_root)/src/gtest-printers.cc',
        '<(local_root)/src/gtest-test-part.cc',
        '<(local_root)/src/gtest-typed-test.cc',
        '<(local_root)/src/gtest_main.cc',
      ],
    },
  ],
}
