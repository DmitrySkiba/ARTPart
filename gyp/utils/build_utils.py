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

import fnmatch
import json
import os
import pipes
import shlex
import shutil
import subprocess
import sys
import traceback
import optparse


def invoke_xcrun(sdk, command):
  tool_path = check_call_die(
      ['xcrun', '-sdk', sdk] + command,
      suppress_output = True, return_stdout = True)
  return tool_path.strip()


def add_required_option(parser, *args, **kwargs):
  fixed_kwargs = {}
  if kwargs is not None:
    fixed_kwargs = kwargs
  help = fixed_kwargs.get('help')
  help_required = '[REQUIRED]'
  if help is not None:
    help = help_required + ' ' + str(help)
  else:
    help = help_required
  fixed_kwargs['help'] = help
  parser.add_option(*args, **fixed_kwargs)


def check_required_options(options, parser):
  missing_options = []
  for option in parser.option_list:
    if option.help and option.help.startswith('[REQUIRED]') \
        and getattr(options, option.dest) == None:
      missing_options.extend(option._long_opts)
  if len(missing_options) > 0:
    parser.error('Missing REQUIRED options: ' + str(missing_options))


def make_directory(dir_path):
  try:
    os.makedirs(dir_path)
  except OSError:
    pass


def delete_directory(dir_path):
  if os.path.exists(dir_path):
    shutil.rmtree(dir_path)


def touch(path):
  make_directory(os.path.dirname(path))
  with open(path, 'a'):
    os.utime(path, None)


def find_in_paths(paths, file_filters = None, directory_filters = None, invert_filters = False):
  def _match(name, filters):
    if filters is None:
      return True
    if len(filters) == 0:
      return invert_filters
    for filter in filters:
      if fnmatch.fnmatch(name, filter) == invert_filters:
        return False
    return True

  all_files = []
  for path in paths:
    if os.path.isfile(path):
      if _match(os.path.basename(path), file_filters):
        all_files.append(path)
    elif os.path.isdir(path):
      for root, directories, files in os.walk(path):
        all_files.extend((os.path.join(root, f) for f in files if _match(f, file_filters)))
        directories[:] = [d for d in directories if _match(d, directory_filters)]

  return all_files


def parse_gyp_list(gyp_string):
  # The ninja generator doesn't support $ in strings, so use ## to
  # represent $.
  # TODO(cjhopman): Remove when
  # https://code.google.com/p/gyp/issues/detail?id=327
  # is addressed.
  gyp_string = gyp_string.replace('##', '$')
  return shlex.split(gyp_string)


# This can be used in most cases like subprocess.check_call. The output,
# particularly when the command fails, better highlights the command's failure.
# This call will directly exit on a failure in the subprocess so that no python
# stacktrace is printed after the output of the failed command.
def check_call_die(args, suppress_output=False, cwd=None, return_stdout=False):
  if not cwd:
    cwd = os.getcwd()

  if suppress_output or return_stdout:
    stdout_fd = subprocess.PIPE
  else:
    stdout_fd = None
  if suppress_output:
    stderr_fd = subprocess.PIPE
  else:
    stderr_fd = None
  child = subprocess.Popen(args, stdout=stdout_fd, stderr=stderr_fd, cwd=cwd)

  stdout, stderr = child.communicate()

  if child.returncode:
    stacktrace = traceback.extract_stack()
    print >> sys.stderr, ''.join(traceback.format_list(stacktrace))
    # A user should be able to simply copy and paste the command that failed
    # into their shell.
    copyable_command = ' '.join(map(pipes.quote, args))
    copyable_command = ('( cd ' + os.path.abspath(cwd) + '; '
        + copyable_command + ' )')
    print >> sys.stderr, 'Command failed:', copyable_command, '\n'

    if stdout:
      print stdout,
    if stderr:
      print stderr,

    # Directly exit to avoid printing stacktrace.
    sys.exit(child.returncode)

  else:
    if not suppress_output:
      if stdout:
        print stdout,
      if stderr:
        print stderr,
    if return_stdout:
      return stdout
    else:
      return None


def mergetree(src, dst, symlinks=False, ignore=None):
  """Same as shutil.copytree() from 2.7 except it allows 'dst' to exist.

  Files and links in 'dst' are replaced with ones from 'src'.
  """
  names = os.listdir(src)
  if ignore is not None:
    ignored_names = ignore(src, names)
  else:
    ignored_names = set()

  if not os.path.exists(dst):
    os.makedirs(dst)

  errors = []
  for name in names:
    if name in ignored_names:
      continue
    srcname = os.path.join(src, name)
    dstname = os.path.join(dst, name)
    try:
      if symlinks and os.path.islink(srcname):
        linkto = os.readlink(srcname)
        if os.path.exists(dstname):
          os.remove(dstname)
        os.symlink(linkto, dstname)
      elif os.path.isdir(srcname):
        mergetree(srcname, dstname, symlinks, ignore)
      else:
        if os.path.exists(dstname):
          os.remove(dstname)
        # Will raise a SpecialFileError for unsupported file types
        shutil.copy2(srcname, dstname)
    # catch the Error from the recursive mergetree so that we can
    # continue with other files
    except shutil.Error, err:
      errors.extend(err.args[0])
    except EnvironmentError, why:
      errors.append((srcname, dstname, str(why)))
  try:
    shutil.copystat(src, dst)
  except OSError, why:
    if WindowsError is not None and isinstance(why, WindowsError):
      # Copying file access times may fail on Windows
      pass
    else:
      errors.extend((src, dst, str(why)))
  if errors:
    raise shutil.Error, errors
