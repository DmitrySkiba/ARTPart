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
    'java-common.gypi',
  ],

  'variables': {
    'jar_dependencies': [
      '<!(<(dependency) libcore-rt_jar)',
      '<!(<(dependency) libcore-conscrypt_jar)',
    ],
  },

  'targets': [
    {
      'target_name': 'boot_jars<(any_variant)',
      'type': 'none',

      'dependencies': [ '<@(jar_dependencies)' ],
      'export_dependent_settings': [ '<@(jar_dependencies)' ],
    },
    {
      'target_name': 'boot_oat<(any_variant)',
      'type': 'none',

      'dependencies': [
        'boot_jars<(any_variant)',
        '<!(<(dependency) art-dex2oat)',
      ],

      'actions': [
        {
          'action_name': 'boot_oat',
          'message': 'Building boot.* files...',

          'inputs': [
            '>@(dependencies.dex_files)',
          ],
          'outputs': [
            '<(boot_art_path)',
            '<(boot_oat_path)',
          ],

          'action': [
            #TODO introduce dex2oat.py wrapper with --dex-files option and use >@(dependencies.dex_files)
            'python', 'utils/cwd_launcher.py', '<(android_fs_root)',
            '<!(<(relpath) <(android_fs_root) <(dex2oat_path))',
            '--android-root=<!(<(relpath) <(android_fs_root) <(android_root_path))',
            '--runtime-arg', '-Xms64m',
            '--runtime-arg', '-Xmx64m',
            '--dex-file=<!(<(relpath) <(android_fs_root) <!(<(dex_path_v) rt))',
            '--dex-file=<!(<(relpath) <(android_fs_root) <!(<(dex_path_v) conscrypt))',
            '--base=<(boot_oat_base)',
            '--image-classes=<(platform_root)/frameworks/base/preloaded-classes',
            '--image=<!(<(relpath) <(android_fs_root) <(boot_art_path))',
            '--oat-file=<!(<(relpath) <(android_fs_root) <(boot_oat_path))',
          ],
        },
      ],
    }
  ]
}
