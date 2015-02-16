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
import tempfile
import optparse
import shutil

script_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(script_path, 'gyp', 'utils'))
import build_utils
import build_environ
import compile_jar
import dex


def main(arguments):
  # arguments = [
  #   '--sources', 'platform/testapps/HelloWorld', '--main-class-name', 'HelloWorld',
  # ]

  example = '' + \
    '\nExample:' + \
    '\n  --sources platform/testapps/HelloWorld --main-class-name HelloWorld' + \
    '\n'
  parser = optparse.OptionParser(usage = optparse.SUPPRESS_USAGE, epilog = example)
  parser.format_epilog = lambda formatter: parser.epilog

  build_utils.add_required_option(parser, '--sources')
  build_utils.add_required_option(parser, '--main-class-name')
  parser.add_option('--repro-dalvikvm', action='store_true')

  options, _ = parser.parse_args(arguments)
  build_utils.check_required_options(options, parser)

  root_path = os.getcwd()

  out_root = os.path.join(root_path, 'out', 'host')
  environ_file = os.path.join(out_root, 'build_environ.json')
  boot_class_path = os.path.join(out_root, 'jars')
  product_root = os.path.join(out_root, 'product')

  temp_root = os.path.realpath(tempfile.mkdtemp())
  try:
    build_environ.load(environ_file)

    jar_file = os.path.join(temp_root, options.main_class_name + '.jar')
    compile_jar.main([
      '--sources', options.sources,
      '--boot-class-paths', boot_class_path,
      '--jar-file', jar_file,
      '--intermediate-path', temp_root,
    ])

    dex_file = os.path.splitext(jar_file)[0] + '-dex.jar'
    dex.main([
      '--dx-tool', os.environ['BUILD_ANDROID_DX'],
      '--jar-file', jar_file,
      '--dex-file', dex_file
    ])

    android_fs_root = os.path.join(product_root, 'android_fs')
    android_root = os.path.join(android_fs_root, 'system')
    android_data = os.path.join(android_fs_root, 'data')
    boot_art_file = os.path.join(android_data, 'dalvik-cache', 'boot.art')

    os.chdir(android_fs_root)

    oat_file_name = os.path.splitext(os.path.basename(dex_file))[0] + '.odex'
    oat_file = os.path.join(os.path.dirname(dex_file), 'x86', oat_file_name)
    build_utils.make_directory(os.path.dirname(oat_file))

    build_utils.check_call_die([
      os.path.join(product_root, 'dex2oat'),
      '--android-root=' + os.path.relpath(android_root, android_fs_root),
      '--boot-image=' + boot_art_file,
      '--dex-file=' + dex_file,
      '--oat-file=' + oat_file,
      '--instruction-set=x86',
      '--host',
      '--runtime-arg', '-Xnorelocate',
    ])

    os.environ['ANDROID_ROOT'] = os.path.relpath(android_root, android_fs_root)
    os.environ['ANDROID_DATA'] = os.path.relpath(android_data, android_fs_root)

    framework_path = os.path.join(android_root, 'framework')
    boot_jars = build_utils.find_in_paths([framework_path], file_filters = ['*.jar'])
    bootclasspath = ':'.join((os.path.relpath(f, android_fs_root) for f in boot_jars))

    dalvikvm_cmd = [
      os.path.join(product_root, 'dalvikvm'),
      '-Ximage:' + boot_art_file,
      '-classpath', dex_file,
      '--runtime-arg', '-Xbootclasspath:' + bootclasspath,
      '--runtime-arg', '-Xnorelocate',
      options.main_class_name,
    ]
    build_utils.check_call_die(dalvikvm_cmd)

    if options.repro_dalvikvm:
      print
      print ' '.join(dalvikvm_cmd)
      print
    else:
      shutil.rmtree(temp_root)

    print 'Succeeded. Temp path was: {0}'.format(temp_root)

  except:
    print
    print 'Failed. Temp path was: {0}'.format(temp_root)
    print

    raise


if __name__ == '__main__':
  sys.exit(main(sys.argv))
