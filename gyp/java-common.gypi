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

{
  'variables': {

    # scripts
    'jar_path_v': '<(format) <(jars_root)/{}.jar',
    'dex_path_v': '<(format) <(android_framework_path)/{}.jar',

    'compile_jar.intermediate_path': '<(intermediate_build_root)/>(_target_name)/compile_jar',
    'compile_jar.stamp_file': '<(intermediate_build_root)/>(_target_name)/compile_jar.stamp',

    'dex.stamp_file': '<(intermediate_build_root)/>(_target_name)/dex.stamp',
  },
}
