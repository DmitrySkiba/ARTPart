#!/usr/bin/env python
#
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

import os
import sys
import shutil
import optparse
import subprocess
import xml.etree.ElementTree as ET
import json

script_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(script_path, 'platform', 'external', 'gyp', 'pylib'))
import gyp

sys.path.append(os.path.join(script_path, 'gyp', 'utils'))
import build_utils
import build_environ


def _generate_xcode_workspace(projects_path, workspace_path):
  projects_relpath = os.path.relpath(projects_path, os.path.dirname(workspace_path))

  workspace_xml = ET.Element('Workspace')
  workspace_xml.set('version', '1.0')
  for project in sorted(os.listdir(projects_path)):
    if project.endswith('.xcodeproj'):
      fileref = ET.SubElement(workspace_xml, 'FileRef')
      fileref.set('location', 'group:' + os.path.join(projects_relpath, project))

  workspace_file_content = ET.tostring(workspace_xml, encoding = 'UTF-8')

  workspace_file_path = os.path.join(workspace_path, 'contents.xcworkspacedata')
  build_utils.make_directory(workspace_path)

  update_workspace = True
  if os.path.exists(workspace_file_path):
    with open(workspace_file_path, 'r') as workspace_file:
      update_workspace = workspace_file.read() != workspace_file_content

  if update_workspace:
    with open(workspace_file_path, 'w') as workspace_file:
      workspace_file.write(workspace_file_content)


def _add_common_build_props(build_props):

  build_props['platform_root'] = os.path.join(build_props['root_path'], 'platform')
  build_props['gradle_root'] = os.path.join(build_props['root_path'], 'gradle')

  # out/ paths
  build_props['product_root'] = os.path.join(build_props['out_root'], 'product')
  build_props['bin_root'] = build_props['product_root']
  build_props['lib_root'] = os.path.join(build_props['out_root'], 'lib')
  build_props['jars_root'] = os.path.join(build_props['out_root'], 'jars')
  build_props['headers_root'] = os.path.join(build_props['out_root'], 'include')
  build_props['build_root'] = os.path.join(build_props['out_root'], 'build')

  build_props['dex2oat_file'] = os.path.join(build_props['bin_root'], 'dex2oat')

  # android_fs/ paths
  build_props['android_fs_root'] = os.path.join(build_props['product_root'], 'android_fs')
  build_props['android_root_path'] = os.path.join(build_props['android_fs_root'], 'system')
  build_props['android_framework_path'] = os.path.join(build_props['android_root_path'], 'framework')
  build_props['android_data_path'] = os.path.join(build_props['android_fs_root'], 'data')

  build_props['boot_art_file'] = os.path.join(build_props['android_data_path'], 'dalvik-cache',
                                              build_props['instruction_set'], 'boot.art')
  build_props['boot_oat_file'] = os.path.join(build_props['android_data_path'], 'dalvik-cache',
                                              build_props['instruction_set'], 'boot.oat')

  # constants
  build_props['boot_oat_base'] = '0x60000000'

  build_props['jarjar_tool'] = os.path.join(build_props['platform_root'],
                                            'prebuilts/misc/common/jarjar/jarjar-1.4.jar')

  return build_props


def _write_build_props(build_props):
  json_path = os.path.join(build_props['out_root'], 'build_props.json')
  with open(json_path, 'w') as file:
    json.dump(build_props, file, indent = True)

  gypi = { 'variables': build_props }
  gypi_path = os.path.join(build_props['out_root'], 'build_props.gypi')
  with open(gypi_path, 'w') as file:
    json.dump(gypi, file, indent = True)

  return json_path


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--debug-gyp', action = 'store_true')
  parser.add_option('--ninja', action = 'store_true')
  parser.add_option('--update', action = 'store_true')
  parser.add_option('--android-sdk-root')
  parser.add_option('--no-gradle', dest = 'using_gradle', default = True, action = 'store_false')
  parser.add_option('--x86_64', dest = 'x86_build', default = True, action = 'store_false')

  options, _ = parser.parse_args(arguments)

  android_sdk_root = options.android_sdk_root
  if not android_sdk_root:
    android_sdk_root = os.environ.get('ANDROID_SDK')
    if not android_sdk_root:
      parser.error('Specify path to Android SDK with --android-sdk-root option ' +
                   'or ANDROID_SDK environment variable')
  android_api = '19' # KitKat

  if options.ninja:
    generator = 'ninja'
  else:
    generator = 'xcode'

  root_path = os.getcwd()
  projects_path = os.path.join(root_path, 'projects')
  generator_output_path = os.path.join(projects_path, generator)
  out_root = os.path.join(root_path, 'out')

  # Delete output directories
  if not options.update:
    build_utils.delete_directory(out_root)
    build_utils.delete_directory(generator_output_path)

  # Generate projects

  main_gyp_file = 'out'

  sdk = 'macosx10.9'
  if options.x86_build:
    arch = 'i386'
    instruction_set = 'x86'
  else:
    arch = 'x86_64'
    instruction_set = 'x86_64'

  build_utils.make_directory(out_root)

  build_props = {
    'root_path': root_path,
    'out_root': out_root,
    'arch': arch,
    'instruction_set': instruction_set,
    'using_gradle': int(options.using_gradle),
  }
  _add_common_build_props(build_props)

  environ = build_environ.generate(sdk, arch, android_sdk_root, android_api)
  build_environ.dump(environ, os.path.join(out_root, 'build_environ.json'))

  build_props.update(environ)

  _write_build_props(build_props)

  gyp_arguments = [
    '-f', generator,
  ]

  if options.debug_gyp:
    gyp_arguments += [ '-d', 'all' ]

  gyp_arguments += [
    '--depth', '.',
    '--generator-output', generator_output_path,
    '{}.gyp'.format(main_gyp_file),
  ]

  os.chdir('gyp')
  gyp.main(gyp_arguments)

  # Generate Xcode workspace
  if generator == 'xcode':
    _generate_xcode_workspace(generator_output_path,
                              os.path.join(generator_output_path, 'ARTPart.xcworkspace'))


if __name__ == '__main__':
  sys.exit(main(sys.argv))
