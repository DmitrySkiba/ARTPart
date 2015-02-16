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
    'local_root': '<(system_root)/libcutils',
  },

  'targets': [
    {
      'target_name': 'system-libcutils<(any_variant)',
      'product_name': 'libcutils',
      'type': 'static_library',

      'sources': [
        '<(local_root)/atomic.c',
        '<(local_root)/ashmem-host.c',
        '<(local_root)/open_memstream.c',
        '<(local_root)/threads.c',
        '<(local_root)/native_handle.c',
        '<(local_root)/process_name.c',
        '<(local_root)/sched_policy.c',
        '<(local_root)/properties.c',
        '<(local_root)/memory.c',
        '<(local_root)/sockets.c',
        '<(local_root)/socket_local_client.c',
        '<(local_root)/socket_local_server.c',
      ],
    },
  ],
}
