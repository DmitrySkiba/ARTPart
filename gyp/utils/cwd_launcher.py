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
import build_utils

def main(arguments):
    if len(arguments) < 3:
        sys.exit('Invalid arguments: <working directory> <program and arguments> expected.')

    cwd = arguments[1]
    command = arguments[2:]

    program = command[0]
    if not os.path.isabs(program) and os.path.exists(os.path.join(cwd, program)):
        command[0] = os.path.join('./', program)

    build_utils.check_call_die(command, cwd = cwd)


if __name__ == "__main__":
    sys.exit(main(sys.argv))