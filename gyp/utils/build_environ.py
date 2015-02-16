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
import json
import optparse
import re

import build_utils


def _read_api_level(property_file):
  line_matcher = re.compile('^Pkg.Revision\s*=\s*([0-9.]+)$')
  for line in open(property_file, 'r').readlines():
    match = line_matcher.match(line)
    if match:
      revision = match.group(1)
      return tuple(map(int, revision.split(".")))

  return None


# Generates environment dictionary with the following keys:
#
# BUILD_SDK - Native SDK name (sdk argument)
# BUILD_ARCH - Native architecture (arch argument)
# BUILD_ANDROID_SDK_ROOT - Path to Android SDK (android_sdk_root argument)
# BUILD_ANDROID_API - Android API (android_api argument)
#
# BUILD_SDK_VERSION - Native SDK version
# CC - cc tool invocation
# CXX - c++ tool invocation
# LD - ld tool invocation
# BUILD_LIBTOOL - libtool invocation
#
# BUILD_ANDROID_DX - dx tool invocation
# BUILD_ANDROID_AAPT - aapt tool invocation
# BUILD_ANDROID_AIDL - aidl tool invocation
#
# BUILD_ENVIRON - all of the above fields packed in a string (for apply() function)
#
def generate(sdk, arch, android_sdk_root, android_api):
  environment = {}

  if sdk and arch:
    environment['BUILD_SDK'] = sdk
    environment['BUILD_ARCH'] = arch
    environment['BUILD_ANDROID_SDK_ROOT'] = android_sdk_root
    environment['BUILD_ANDROID_API'] = android_api

    environment['BUILD_SDK_VERSION'] = build_utils.invoke_xcrun(sdk, ['--show-sdk-version'])

    cc = build_utils.invoke_xcrun(sdk, ['-f', 'cc'])
    cxx = build_utils.invoke_xcrun(sdk, ['-f', 'c++'])
    sdk_path = build_utils.invoke_xcrun(sdk, ['--show-sdk-path'])
    environment['CC'] = '{0} -isysroot {1} -arch {2}'.format(cc, sdk_path, arch)
    environment['CXX'] = '{0} -isysroot {1} -arch {2}'.format(cxx, sdk_path, arch)

    ld = build_utils.invoke_xcrun(sdk, ['-f', 'ld'])
    sdk_version = build_utils.invoke_xcrun(sdk, ['--show-sdk-version'])
    if sdk.startswith('macosx'):
      version_min_option = '-macosx_version_min'
    else:
      version_min_option = '-iphone_version_min'
    environment['LD'] = '{0} {1} {2} -arch {3}'.format(ld, version_min_option, sdk_version, arch)

    environment['BUILD_LIBTOOL'] = build_utils.invoke_xcrun(sdk, ['-f', 'libtool'])

  if android_sdk_root and android_api:
    build_tools_root = os.path.join(android_sdk_root, 'build-tools')
    if not os.path.exists(build_tools_root):
      raise Exception("'{}' doesn't exists".format(build_tools_root))

    max_api = None
    for build_tools in os.listdir(build_tools_root):
      build_tools_path = os.path.join(build_tools_root, build_tools)
      property_file = os.path.join(build_tools_path, 'source.properties')
      if os.path.isfile(property_file):
        api = _read_api_level(property_file)
        if api and str(api[0]) == android_api:
          if not max_api or api > max_api[0]:
            max_api = (api, build_tools_path)

    if not max_api:
      raise Exception("Failed to find Android build tools version {} in '{}'".
                      format(android_api, build_tools_root))

    build_tools_path = max_api[1]

    def set_tool(key, name):
      tool_path = os.path.join(build_tools_path, name)
      if not os.path.isfile(tool_path):
        raise Exception("Android tool '{}' doesn't exist".format(tool_path))
      environment[key] = tool_path

    set_tool('BUILD_ANDROID_DX', 'dx')
    set_tool('BUILD_ANDROID_AIDL', 'aidl')
    set_tool('BUILD_ANDROID_AAPT', 'aapt')

  environment['BUILD_ENVIRON'] = json.dumps(environment)
  return environment


# Unpacks environment dictionary from a string and applies it to os.environ.
def apply(string):
  os.environ.update(json.loads(string))


# Loads environment dictionary from a file and applies it to os.environ.
def load(file):
  with open(file) as environ_file:
    os.environ.update(json.load(environ_file))


# Saves environment dictionary to a file.
def dump(environ, file):
  with open(file, 'w') as environ_file:
    json.dump(environ, environ_file, indent = True)


def main(arguments):
  parser = optparse.OptionParser()
  parser.add_option('--sdk')
  parser.add_option('--arch')
  parser.add_option('--android-sdk-root')
  parser.add_option('--android-api')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  if bool(options.sdk) != bool(options.arch):
    parser.error('Both --sdk and --arch options must be specified')

  if bool(options.android_sdk_root) != bool(options.android_api):
    parser.error('Both --android-sdk-root and --android-api options must be specified')

  print generate(options.sdk, options.arch, options.android_sdk_root, options.android_api)


if __name__ == '__main__':
  sys.exit(_main(sys.argv))
