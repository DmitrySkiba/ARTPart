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
    'local_root': '<(platform_root)/external/icu4c',
  },

  'targets': [
    {
      'target_name': 'external-icu4c',
      'product_name': 'icu4c',
      'type': 'static_library',

      'includes': [
        'external-icu4c-common.gypi',
        'external-icu4c-i18n.gypi',
      ],

      'direct_dependent_settings': {
        'include_dirs': [
          '<(local_root)/common',
          '<(local_root)/i18n',
        ],
      },

      'defines': [
        '_REENTRANT',
      ],

      'include_dirs': [
        '<(local_root)/common',
        '<(local_root)/i18n',
      ],

      'actions': [
        {
          'variables': {
            'source_file_name': 'icudt51l-all.dat',
            'source_file': '<(local_root)/stubdata/<(source_file_name)',
            'destination_file': '<(android_root_path)/usr/icu/icudt51l.dat'
          },

          'action_name': 'icudt',
          'message': 'Copying <(source_file_name)...',

          'inputs': [ '<(source_file)' ],
          'outputs': [ '<(destination_file)' ],
          'action': [
            'python', 'utils/copy.py',
            '--source', '<(source_file)',
            '--destination', '<(destination_file)'
          ]
        },
      ],
    },
  ],
}
