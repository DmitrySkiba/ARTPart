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
    'local_root': '<(platform_root)/external/openssl',

    'build_root': '<(intermediate_build_root)/openssl',
    'build_out_root': '<(build_root)/out',
    'built_libraries': [
      '<(build_out_root)/lib/libcrypto.a',
      '<(build_out_root)/lib/libssl.a',
    ],
    'built_headers': '<(build_out_root)/include/openssl',

    'headers_root': '<(intermediate_headers_root)',
    'libopenssl_path': '<(lib_root)/libopenssl.a',
  },

  'targets': [
    {
      'target_name': 'external-openssl',
      'type': 'none',

      'direct_dependent_settings': {
        'include_dirs': [ '<(headers_root)' ],
        'link_settings': {
          'libraries': [ '<(libopenssl_path)' ]
        },
      },

      'hard_dependency': 1,

      'actions': [
        {
          'action_name': 'openssl',
          'message': 'Building OpenSSL...',

          'inputs': [ '<(local_root)' ],
          'outputs': [
            '<(built_headers)',
            '<@(built_libraries)',
          ],

          'action': [
            'python', 'external-openssl-build.py',
            '--environ', '<(BUILD_ENVIRON)',
            '--openssl-path', '<(local_root)',
            '--build-path' ,'<(build_root)'
          ]
        },
        {
          'action_name': 'openssl-headers',
          'message': 'Copying OpenSSL headers...',

          'inputs': [ '<(built_headers)' ],
          'outputs': [ '<(headers_root)/openssl' ],

          'action': [
            'python', 'utils/copy.py',
            '--source', '<(built_headers)',
            '--destination' ,'<(headers_root)/openssl'
          ]
        }
      ],

      'variables': {
        'ar.action_name': 'libopenssl',
        'ar.message': 'Archiving OpenSSL libraries...',
        'ar.archive_path': '<(libopenssl_path)',
        'ar.input_files': [ '<@(built_libraries)' ],
      },
      'includes': [ 'utils/ar.gypi' ],
    },
  ],
}
