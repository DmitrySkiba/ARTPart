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
    'art-common.gypi',
  ],

  'targets': [
    {
      'target_name': 'art-run_java<(any_variant)',
      'product_name': 'run_java',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) system-libcutils)',
        '<!(<(dependency) art-compiler)',
        '<!(<(dependency) art-runtime)',
        '<!(<(dependency) libnativehelper)',
      ],

      'sources': [
        '<(art_root)/dalvikvm/run_java.cc'
      ],
    },
  ],
}
