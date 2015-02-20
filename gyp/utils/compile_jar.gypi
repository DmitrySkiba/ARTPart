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

# Arguments:
# compile_jar.source_paths              REQUIRED, array
# compile_jar.source_exclude_filters    array
# compile_jar.resource_paths            array
# compile_jar.manifest_file
# compile_jar.boot_class_paths          array
# compile_jar.jar_file                  REQUIRED
# compile_jar.jar_include_filters       array
# compile_jar.jarjar_tool
# compile_jar.jarjar_rules_file
# compile_jar.intermediate_path         REQUIRED
# compile_jar.stamp_file
# compile_jar.extra_action_inputs       array
{
  'variables': {
    'my_path': '.',

    'compile_jar.boot_class_paths%': [],
    'compile_jar.source_exclude_filters%': [],
    'compile_jar.manifest_file%': '',
    'compile_jar.resource_paths%': [],
    'compile_jar.jar_include_filters%': [],
    'compile_jar.jarjar_tool%': '',
    'compile_jar.jarjar_rules_file%': '',
    'compile_jar.stamp_file%': '',
    'compile_jar.extra_action_inputs%': [],

    # TODO: use force_action target instead
    'compile_jar._force_file': '<(compile_jar.intermediate_path)/compile_jar.force',
  },

  'direct_dependent_settings': {
    'variables': {
      'dependencies.jar_files': [ '<(compile_jar.jar_file)' ],
    },
  },

  'actions': [
    {
      'variables': {
        'invocation': [
            'python', '<(my_path)/compile_jar.py',
            '--sources', '<(compile_jar.source_paths)',
            '--jar-file', '<(compile_jar.jar_file)',
            '--boot-class-paths', '<(compile_jar.boot_class_paths)',
            '--intermediate-path', '<(compile_jar.intermediate_path)',
        ],
        'conditions': [
          [ '"<(compile_jar.stamp_file)" != ""', {
            'invocation+': [ '--stamp-file', '<(compile_jar.stamp_file)' ],
          }],
          [ '<!(<(len) <(compile_jar.source_exclude_filters)) > 0', {
            'invocation+': [ '--source-exclude-filters', '<(compile_jar.source_exclude_filters)' ],
          }],
          [ '"<(compile_jar.manifest_file)" != ""', {
            'invocation+': [ '--manifest-file', '<(compile_jar.manifest_file)' ],
          }],
          [ '<!(<(len) <(compile_jar.resource_paths)) > 0', {
            'invocation+': [ '--resources', '<(compile_jar.resource_paths)' ],
          }],
          [ '<!(<(len) <(compile_jar.jar_include_filters)) > 0', {
            'invocation+': [ '--jar-include-filters', '<(compile_jar.jar_include_filters)' ],
          }],
          [ '"<(compile_jar.jarjar_tool)" != ""', {
            'invocation+': [ '--jarjar-tool', '<(compile_jar.jarjar_tool)' ],
          }],
          [ '"<(compile_jar.jarjar_rules_file)" != ""', {
            'invocation+': [ '--jarjar-rules-file', '<(compile_jar.jarjar_rules_file)' ],
          }],
        ],
      },

      'action_name': 'jar-<(_target_name)',
      'message': 'Compiling <(compile_jar.jar_file)...',

      'conditions': [
        [ '"<(GENERATOR)" == "xcode"', {
          'inputs': [
            # Not using '--print-gyp-inputs' output here to avoid getting
            # "Argument list too long" OS error from Xcode. To make sure this
            # action runs on every build, we add a dependency on a dummy file
            # which we touch on every build (see 'force' action below).
            '<(compile_jar._force_file)',
            '<@(compile_jar.extra_action_inputs)',
          ],
        }, {
          'inputs': [
            '<@(compile_jar.extra_action_inputs)',
            '<!@(<(invocation) --print-gyp-inputs)',
          ],
        }],
      ],
      'outputs': [ '<!@(<(invocation) --print-gyp-outputs)' ],

      'action': [ '<@(invocation)' ],
    },
  ],
  'conditions': [
    [ '"<(GENERATOR)" == "xcode"', {
      'actions': [
        {
          'action_name': 'force-jar-<(_target_name)',

          'inputs': [],
          'outputs': [],

          'action': [ 'python', 'utils/touch.py', '<(compile_jar._force_file)' ],
        },
      ],
    }],
  ],
}
