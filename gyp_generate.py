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


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--debug-gyp', action = 'store_true')
  parser.add_option('--ninja', action = 'store_true')
  parser.add_option('--update', action = 'store_true')
  parser.add_option('--android-sdk-root')
  parser.add_option('--no-gradle', dest = 'using_gradle', default = True, action = 'store_false')

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
  arch = 'i386'

  build_utils.make_directory(out_root)

  environ = build_environ.generate(sdk, arch, android_sdk_root, android_api)
  build_environ.dump(environ, os.path.join(out_root, 'build_environ.json'))

  gyp_arguments = [
    '-f', generator,
    '-D', 'root_path=' + root_path,
    '-D', 'using_gradle=' + str(int(options.using_gradle)),
  ]

  for key, value in environ.iteritems():
    gyp_arguments += [ '-D', key + '=' + value ]

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
