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

# Arguments:
# ar.action_name    REQUIRED
# ar.message
# ar.archive_file   REQUIRED
# ar.input_files    REQUIRED
{
  'variables': {
    'ar.message%': '',
  },

  'actions': [
    {
      'action_name': '<(ar.action_name)',
      'message': '<(ar.message)',

      'inputs': [ '<@(ar.input_files)' ],
      'outputs': [ '<(ar.archive_file)' ],

      'action': [ '<(BUILD_LIBTOOL)', '-static', '-o', '<(ar.archive_file)', '<@(ar.input_files)' ],
    },
  ],
}
