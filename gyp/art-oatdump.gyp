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
      'target_name': 'art-oatdump',
      'product_name': 'oatdump',
      'type': 'executable',

      'dependencies': [
        '<!(<(dependency) art-runtime)',
        '<!(<(dependency) system-libcutils)',
        '<!(<(dependency) external-valgrind)',
      ],

      'include_dirs': [
        '<(art_root)/disassembler',
      ],

      'sources': [
        '<(art_root)/oatdump/oatdump.cc',
        '<(art_root)/disassembler/disassembler.cc',
        '<(art_root)/disassembler/disassembler_x86.cc',
      ],
    },
  ],
}
