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
    'local_root': '<(platform_root)/external/expat',
    'libexpat_headers_path': '<(intermediate_headers_root)/libexpat',
  },

  'targets': [
    {
      'target_name': 'external-expat',
      'product_name': 'expat',
      'type': 'static_library',

      'direct_dependent_settings': {
        'include_dirs': [
          '<(intermediate_headers_root)',
        ],
      },

      'include_dirs': [
        '<(local_root)',
        '<(local_root)/lib',
      ],

      'defines': [
        'HAVE_EXPAT_CONFIG_H'
      ],

      'sources': [
        '<(local_root)/lib/xmlparse.c',
        '<(local_root)/lib/xmlrole.c',
        '<(local_root)/lib/xmltok.c',
      ],

      'hard_dependency': 1,
      'actions': [
        {
          'action_name': 'libexpat-headers',
          'message': 'Copying headers to libexpat...',

          'inputs': [],
          'outputs': [ '<(libexpat_headers_path)' ],
          'action': [
            'python', 'utils/copy.py',
            '--source', '<(local_root)/lib/expat.h',
            '--source', '<(local_root)/lib/expat_external.h',
            '--destination-path' ,'<(libexpat_headers_path)'
          ]
        },
      ],
    },
  ],
}
