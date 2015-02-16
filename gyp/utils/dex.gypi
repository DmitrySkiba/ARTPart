## Copyright (C) 2015 Dmitry Skiba
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

# Arguments:
# dex.core_library  [1/0]
# dex.jar_file      REQUIRED
# dex.dex_file      REQUIRED
# dex.stamp_file
{
  'variables': {
    'my_path': '.',
    'dex.core_library%': 0,
    'dex.stamp_file%': '',
  },

  'direct_dependent_settings': {
    'variables': {
      'dependencies.dex_files': [ '<(dex.dex_file)' ],
    },
  },

  'actions': [
    {
      'variables': {
        'invocation': [
            'python', '<(my_path)/dex.py',
            '--dx-tool', '<(BUILD_ANDROID_DX)',
            '--jar-file', '<(dex.jar_file)',
            '--dex-file', '<(dex.dex_file)',
        ],
        'conditions': [
          [ "<(dex.core_library) == 1", {
            'invocation': [ '--core-library' ],
          }],
          [ '"<(dex.stamp_file)" != ""', {
            'invocation+': [ '--stamp-file', '<(dex.stamp_file)' ],
          }],
        ]
      },

      'action_name': 'dex-<(_target_name)',
      'message': 'Dexing <(dex.jar_file)...',

      'inputs': [ '<!@(<(invocation) --print-gyp-inputs)' ],
      'outputs': [ '<!@(<(invocation) --print-gyp-outputs)' ],

      'action': [ '<@(invocation)' ],
    },
  ],
}
