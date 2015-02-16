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

import sys
import os
import shutil
import optparse

import build_utils


def main(arguments):
  parser = optparse.OptionParser()
  build_utils.add_required_option(parser, '--source', action = 'append')
  parser.add_option('--destination-path')
  parser.add_option('--destination')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  if not options.destination_path and not options.destination:
    parser.error('Destination is not specified!')

  for source in options.source:
    if not os.path.exists(source):
      sys.exit("'{0}' doesn't exist!".format(source))

    if options.destination:
      destination = options.destination
    else:
      destination = os.path.join(options.destination_path, os.path.basename(source))

    if not os.path.exists(destination):
      destinationPath = os.path.dirname(destination)
      if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)
      if os.path.isfile(source):
        shutil.copy(source, destination)
      else:
        shutil.copytree(source, destination)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
