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
    'local_root': '<(platform_root)/testapps/HelloWorld',
    'build_root': '<(intermediate_build_root)/HelloWorld',

    'jar_file': '<(build_root)/app.jar',
    'dex_file': '<(build_root)/app-dex.jar',
    'oat_file': '<(build_root)/<(instruction_set)/app-dex.odex',
  },

  'targets': [
    {
      'target_name': 'testapps-HelloWorld-jar',
      'type': 'none',

      'dependencies': [
        '<!(<(dependency) boot_oat)',
      ],

      'variables': {
        'compile_jar.source_paths': [
          '<(local_root)/HelloWorld.java',
        ],
        'compile_jar.jar_file': '<(jar_file)',

        'dex.jar_file': '<(jar_file)',
        'dex.dex_file': '<(dex_file)',
      },
      'includes': [ 'utils/compile_jar.gypi', 'utils/dex.gypi' ],
    },
    {
      'target_name': 'testapps-HelloWorld',
      'product_name': 'HelloWorld',
      'type': 'executable',

      'dependencies': [
        'testapps-HelloWorld-jar',
        '<!(<(dependency) art-run_java)',
        '<!(<(dependency) art-dex2oat)',
      ],

      'defines': [
        'APP_OAT_PATH="<(oat_file)"',
      ],

      'sources': [
        '<(local_root)/hello_world.cc'
      ],

      'actions': [
        {
          'action_name': 'oat_file',
          'message': 'Building oat file...',

          'inputs': [ '<(dex_file)' ],
          'outputs': [ '<(oat_file)' ],

          'action': [
            'python', 'utils/cwd_launcher.py', '<(android_fs_root)',
            '<(dex2oat_file)',
            '--android-root=<!(<(relpath) <(android_fs_root) <(android_root_path))',
            '--runtime-arg', '-Xms64m',
            '--runtime-arg', '-Xmx64m',
            '--runtime-arg', '-Xnorelocate',
            '--runtime-arg', '-XX:DisableHSpaceCompactForOOM',
            '--boot-image=<(boot_art_file)',
            '--dex-file=<(dex_file)',
            '--oat-file=<(oat_file)',
            '--instruction-set=<(instruction_set)',
            '--host',
          ],
        },
      ],
    },
  ],
}
