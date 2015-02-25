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
import optparse
import shutil
import json

this_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(this_path, 'utils'))
import build_utils
import build_environ


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--environ')
  build_utils.add_required_option(parser, '--openssl-path')
  build_utils.add_required_option(parser, '--build-path')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  build_environ.apply(options.environ)

  openssl_path = os.path.abspath(options.openssl_path)
  build_path = os.path.abspath(options.build_path)

  out_path = os.path.join(build_path, 'out')
  out_include_path = os.path.join(out_path, 'include', 'openssl')
  out_lib_path = os.path.join(out_path, 'lib')
  if os.path.exists(out_include_path) and os.listdir(out_include_path) \
      and os.path.exists(out_lib_path) and os.listdir(out_lib_path):
    print 'Nothing to do: headers and libs already built.'
    return

  if os.environ.has_key('XCODE_VERSION_MAJOR'):
    # Xcode specifies 'COMMAND_MODE = legacy' which prevents successful linkage
    del os.environ['COMMAND_MODE']

  openssl_target = None

  sdk = os.environ['BUILD_SDK']
  arch = os.environ['BUILD_ARCH']
  if sdk.startswith('iphoneos'):
    openssl_target = 'iphoneos-cross'
  elif sdk.startswith('macosx') or sdk.startswith('iphonesimulator'):
    if arch == 'i386':
      openssl_target = 'darwin-i386-cc'
    elif arch == 'x86_64':
      openssl_target = 'darwin64-x86_64-cc'

  if not openssl_target:
    sys.exit('Failed to determine OpenSSL target.')

  build_utils.mergetree(openssl_path, build_path)
  os.chdir(build_path)

  build_utils.check_call_die(['sh', './Configure', '--prefix=' + out_path, openssl_target])

  # Avoid 'install' because it fails on Yosemite, use 'all' + 'install_sw'.
  build_utils.check_call_die(['make', 'all']) # ld fails when -j option specified
  build_utils.check_call_die(['make', 'install_sw'])


if __name__ == '__main__':
    main(sys.argv)
