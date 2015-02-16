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
  'variables': {
    'art_root': '<(platform_root)/art',
  },

  'target_defaults': {

    'defines': [
      #'ART_USE_PORTABLE_COMPILER',
      #'ART_USE_OPTIMIZING_COMPILER',
      #'ART_USE_ARM_INSTRUCTION_SET',
      #'ART_USE_ARM64_INSTRUCTION_SET',
      #'ART_USE_MIPS_INSTRUCTION_SET',
      #'ART_USE_MIPS64_INSTRUCTION_SET',
      'ART_USE_X86_INSTRUCTION_SET',
      #'ART_USE_X86_64_INSTRUCTION_SET',
      #'ART_USE_DLMALLOC_ALLOCATOR',
    ],

    'include_dirs': [
      '<(art_root)/runtime',
      '<(art_root)/compiler',
    ],

    'xcode_settings': {
      'CLANG_CXX_LANGUAGE_STANDARD': 'gnu++0x',
    },
  },
}
