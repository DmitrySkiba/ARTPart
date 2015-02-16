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

import optparse
import os
import sys

import build_utils
import md5_check


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--print-gyp-inputs', action='store_true')
  parser.add_option('--print-gyp-outputs', action='store_true')
  build_utils.add_required_option(parser, '--dx-tool')
  parser.add_option('--core-library', action='store_true')
  build_utils.add_required_option(parser, '--jar-file')
  build_utils.add_required_option(parser, '--dex-file')
  parser.add_option('--stamp-file')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  # Handle --print-gyp-XXX options and exit
  if options.print_gyp_inputs:
    print options.jar_file
    return
  elif options.print_gyp_outputs:
    print options.dex_file
    return

  # Main course

  cmd = [options.dx_tool, '--dex']
  if options.core_library:
    cmd.append('--core-library')
  cmd.append('--output=' + options.dex_file)
  cmd.append(options.jar_file)

  def _dx():
    build_utils.check_call_die(cmd)

  if options.stamp_file:
    md5_check.CallAndRecordIfStale(
        _dx,
        record_path = options.stamp_file,
        input_paths = [options.jar_file],
        input_strings = cmd)
  else:
    _dx()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
