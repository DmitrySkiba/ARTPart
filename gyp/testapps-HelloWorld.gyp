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

    'jar_path': '<(build_root)/app.jar',
    'dex_path': '<(build_root)/app-dex.jar',
    'oat_path': '<(build_root)/x86/app-dex.odex', # TODO use script to add 'x86'
  },

  'targets': [
    {
      'target_name': 'testapps-HelloWorld-jar<(any_variant)',
      'type': 'none',

      'dependencies': [
        '<!(<(dependency) boot_oat)',
      ],

      'variables': {
        'compile_jar.source_paths': [
          '<(local_root)/HelloWorld.java',
        ],
        'compile_jar.jar_file': '<(jar_path)',

        'dex.jar_file': '<(jar_path)',
        'dex.dex_file': '<(dex_path)',
      },
      'includes': [ 'utils/compile_jar.gypi', 'utils/dex.gypi' ],
    },
    {
      'target_name': 'testapps-HelloWorld<(any_variant)',
      'product_name': 'HelloWorld',
      'type': 'executable',

      'dependencies': [
        'testapps-HelloWorld-jar<(any_variant)',
        '<!(<(dependency) art-run_java)',
      ],

      'defines': [
        'APP_OAT_PATH="<(oat_path)"',
      ],

      'sources': [
        '<(local_root)/hello_world.cc'
      ],

      'conditions': [
        [ 'variant == "host"', {
          'dependencies': [
            '<!(<(dependency) art-dex2oat)',
          ],
        }],
        [ 'OS_variant == "ios"', {
          'mac_bundle': 1,
          'sources=': [
            '<(local_root)/hello_world.mm',
          ],
          'xcode_settings': {
            'IPHONEOS_DEPLOYMENT_TARGET': '<(BUILD_SDK_VERSION)',
            'TARGETED_DEVICE_FAMILY': '1,2',
            'INFOPLIST_FILE': '<(local_root)/Info.plist',
          },
        }],
      ],

      'actions': [
        {
          'action_name': 'oat_file',
          'message': 'Building oat file...',

          'inputs': [ '<(dex_path)' ],
          'outputs': [ '<(oat_path)' ],

          'action': [
            'python', 'utils/cwd_launcher.py', '<(android_fs_root)',
            '<(dex2oat_path)',
            '--android-root=<!(<(relpath) <(android_fs_root) <(android_root_path))',
            '--runtime-arg', '-Xms64m',
            '--runtime-arg', '-Xmx64m',
            '--runtime-arg', '-Xnorelocate',
            '--boot-image=<(boot_art_path)',
            '--dex-file=<(dex_path)',
            '--oat-file=<(oat_path)',
            '--instruction-set=x86',
            '--host',
          ],
        },
      ],
    },
  ],
}
