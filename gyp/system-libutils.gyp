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
    'system-common.gypi',
  ],

  'variables': {
    'local_root': '<(system_root)/libutils'
  },

  'targets': [
    {
      'target_name': 'system-libutils<(any_variant)',
      'product_name': 'libutils',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) frameworks-include)',
        '<!(<(dependency) system-libcorscrew)',
      ],

      'sources': [
        '<(local_root)/BasicHashtable.cpp',
        '<(local_root)/BlobCache.cpp',
        '<(local_root)/CallStack.cpp',
        '<(local_root)/FileMap.cpp',
        '<(local_root)/JenkinsHash.cpp',
        '<(local_root)/LinearAllocator.cpp',
        '<(local_root)/LinearTransform.cpp',
        '<(local_root)/Log.cpp',
        #'<(local_root)/Looper.cpp',
        '<(local_root)/misc.cpp',
        '<(local_root)/PropertyMap.cpp',
        '<(local_root)/RefBase.cpp',
        '<(local_root)/SharedBuffer.cpp',
        '<(local_root)/Static.cpp',
        '<(local_root)/StopWatch.cpp',
        '<(local_root)/String16.cpp',
        '<(local_root)/String8.cpp',
        '<(local_root)/SystemClock.cpp',
        '<(local_root)/Threads.cpp',
        '<(local_root)/Timers.cpp',
        '<(local_root)/Tokenizer.cpp',
        '<(local_root)/Unicode.cpp',
        '<(local_root)/VectorImpl.cpp',
      ],
    },
  ],
}
