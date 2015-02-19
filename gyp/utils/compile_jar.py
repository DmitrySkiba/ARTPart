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
#
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import optparse
import os
import sys

import fnmatch
import build_utils
import md5_check


def _is_filtered(name, filters):
  for filter in filters:
    if fnmatch.fnmatch(name, filter):
      return True
  return False


def _find_source_files(options):
  sources = build_utils.parse_gyp_list(options.sources)
  files = build_utils.find_in_paths(sources, file_filters = ['*.java'])

  if options.source_exclude_filters:
    filters = build_utils.parse_gyp_list(options.source_exclude_filters)
    files = [f for f in files if not _is_filtered(f, filters)]

  return files


def _find_boot_class_files(options):
  if not options.boot_class_paths:
    return None
  paths = build_utils.parse_gyp_list(options.boot_class_paths)
  return build_utils.find_in_paths(paths, file_filters = ['*.jar'])


def _find_resource_files(options):
  if not options.resources:
    return []

  file_filters = [
    '*.java',
    'package.html',
    'overview.html',
    '.*.swp',
    '.DS_Store',
    '*~',
  ]
  directory_filters = [
    '.svn',
  ]

  resources = []
  for resource in build_utils.parse_gyp_list(options.resources):
    path = os.path.abspath(resource)
    files = build_utils.find_in_paths(
        [path],
        file_filters = file_filters,
        directory_filters = directory_filters,
        invert_filters = True)
    resources.append((path, files))

  return resources


def _compile_and_jar(options):
  output_classes_path = os.path.join(options.intermediate_path, 'classes')

  javac_cmd = [
    'javac',
    '-g',
    '-source', '1.7',
    '-target', '1.7',
    '-encoding', 'UTF-8',
    '-d', output_classes_path,
  ]

  boot_class_files = _find_boot_class_files(options)
  if boot_class_files:
    javac_cmd.append('-bootclasspath')
    if boot_class_files == ['']:
      javac_cmd.append(':')
    else:
      javac_cmd.append(':'.join(boot_class_files))

  source_files = _find_source_files(options)
  javac_cmd += source_files

  jar_file = os.path.abspath(options.jar_file)

  def _do():
    # Delete the classes directory. This ensures that all .class files in the
    # output are actually from the input .java files. For example, if a .java
    # file is deleted or an inner class is removed, the classes directory should
    # not contain the corresponding old .class file after running this action.
    build_utils.delete_directory(output_classes_path)
    build_utils.make_directory(output_classes_path)
    build_utils.check_call_die(javac_cmd, suppress_output = True)

    jar_file_path = os.path.dirname(jar_file)
    if not os.path.exists(jar_file_path):
      os.makedirs(jar_file_path)

    raw_jar_file = jar_file
    if options.jarjar_tool:
      raw_jar_file = os.path.join(options.intermediate_path, 'jar.jar')

    jar_options = 'cf0'
    if options.manifest_file:
      jar_options += 'm'
    jar_cmd = ['jar', jar_options, raw_jar_file]
    if options.manifest_file:
      jar_cmd += [os.path.abspath(options.manifest_file)]
    for path, files in _find_resource_files(options):
      for file in files:
        jar_cmd += ['-C', path, os.path.relpath(file, path)]

    # Remove .class files that are not included. We need to physically remove
    # then because we are including all .class files in output_classes_path.
    if options.jar_include_filters:
      filters = build_utils.parse_gyp_list(options.jar_include_filters)
      for root, directories, files in os.walk(output_classes_path):
        for file in files:
          path = os.path.join(root, file)
          relative_path = os.path.relpath(path, output_classes_path)
          if not _is_filtered(relative_path, filters):
            os.remove(path)

    # The paths of the files in the jar will be the same as they are passed in to
    # the command. Because of this, the command should be run in output_classes_path.
    jar_cmd.append('.')
    build_utils.check_call_die(jar_cmd, cwd = output_classes_path)

    if options.jarjar_tool:
      jarjar_cmd = [
        'java',
        '-jar', options.jarjar_tool,
        'process',
        options.jarjar_rules_file,
        raw_jar_file,
        jar_file
      ]
      build_utils.check_call_die(jarjar_cmd)


  if options.stamp_file:
    input_paths = source_files[:]
    if boot_class_files:
      input_paths += boot_class_files
    md5_check.CallAndRecordIfStale(
        _do,
        record_path = options.stamp_file,
        input_paths = input_paths,
        input_strings = javac_cmd)
  else:
    _do()


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--print-gyp-inputs', action='store_true')
  parser.add_option('--print-gyp-outputs', action='store_true')
  build_utils.add_required_option(parser, '--sources')
  parser.add_option('--source-exclude-filters')
  parser.add_option('--resources')
  parser.add_option('--boot-class-paths')
  build_utils.add_required_option(parser, '--jar-file')
  parser.add_option('--jar-include-filters')
  parser.add_option('--manifest-file')
  parser.add_option('--intermediate-path')
  parser.add_option('--stamp-file')
  parser.add_option('--jarjar-tool')
  parser.add_option('--jarjar-rules-file')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  if bool(options.jarjar_tool) != bool(options.jarjar_rules_file):
    parser.error('Both --jarjar-tool and --jarjar-rules-file must be specified!')

  if options.print_gyp_inputs:
    print '\n'.join(_find_source_files(options))
    for path, files in _find_resource_files(options):
      print '\n'.join(files)
    if options.boot_class_paths:
      print '\n'.join(build_utils.parse_gyp_list(options.boot_class_paths))
  elif options.print_gyp_outputs:
    print options.jar_file
    if options.stamp_file:
      print options.stamp_file
  else:
    if not options.intermediate_path:
      parser.error('Intermediate path is not specified!')
    _compile_and_jar(options)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
