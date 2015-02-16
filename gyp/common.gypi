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
  # External variables:
  # root_path    - absolute path to the root of the repo
  # variant      - build variant (host / target)
  # OS_variant   - OS variant we are building for
  # using_gradle - whether Gradle integration is used (1/0)
  # <Values generated by build_environ.generate()>

  'variables': {
    'OS_variant%': '<(OS)',

    # scripts
    'format': 'python utils/format.py',
    'relpath': 'python utils/relpath.py',
    'len': 'python -c "import sys; print (len(sys.argv) - 1)"',
    'dependency': '<(format) "{0}.gyp:{0}<(any_variant)"',

    # variants
    #TODO: one would expect <(host_variant) to be equal to 'host' version of <(variant) -
    #      either rename variant to build_variant and introduce {host/target}_build_variant,
    #      or think of something else:
    #        ? rename to just <(host) / <(target) / <(any)
    #        ? use script: <!(<(depends) <target/gyp name> [host/target]) where 'any' is the default
    #          examples: <!(<(depends) art_dex2oat host), <!(<(depends) libcore-rt_jar)
    'host_variant': '@host',
    'target_variant': '@target',
    'any_variant': '@<(variant)',

    # paths (keep in sync with settings.gradle)
    'gyp_relpath': '<(relpath) <(root_path)/gyp',
    'platform_root': '<!(<(gyp_relpath) <(root_path)/platform)',

    'out_root_v': '<(format) <(root_path)/out/{}',
    'product_root_v': '<(out_root_v)/product',
    'bin_root_v': '<(product_root_v)',

    'out_root': '<!(<(out_root_v) <(variant))',
    'product_root': '<!(<(product_root_v) <(variant))',
    'bin_root': '<!(<(bin_root_v) <(variant))',
    'lib_root': '<(out_root)/lib',
    'jars_root': '<(out_root)/jars',
    'android_fs_root': '<(product_root)/android_fs',

    'intermediate_headers_root': '<(out_root)/include', # TODO: rename to headers_root
    'intermediate_build_root': '<(out_root)/build', # TODO: rename to build_root

    'host_bin_root': '<!(<(bin_root_v) host)',

    # well known paths
    'android_root_path': '<(android_fs_root)/system',
    'android_framework_path': '<(android_root_path)/framework',
    'android_data_path': '<(android_fs_root)/data',

    'boot_art_path': '<(android_data_path)/dalvik-cache/x86/boot.art', # TODO use script to add 'x86'
    'boot_oat_path': '<(android_data_path)/dalvik-cache/x86/boot.oat', # TODO use script to add 'x86'
    'dex2oat_path': '<(host_bin_root)/dex2oat',

    'force_action_input': '<(intermediate_build_root)/force_action/cookie',

    # tools
    'jarjar_tool': '<(platform_root)/prebuilts/misc/common/jarjar/jarjar-1.4.jar',

    # constants
    'boot_oat_base': '0x60000000',
  },

  'make_global_settings': [
    [ 'CC', '<(CC)' ],
    [ 'CXX', '<(CXX)' ],
    [ 'LD', '<(LD)' ],
  ],

  'target_defaults': {

    'default_configuration': 'Debug',
    'configurations': {
      'Debug': {
      },
      'Release': {
        'defines': [
          'NDEBUG',
        ],
      },
    },

    'defines': [
      'HAVE_ANDROID_OS', # Use (undefined) HAVE_LINUX_ANDROID_OS for Linux-specific stuff
      'HAVE_POSIX_FILEMAP',
      'HAVE_PTHREADS',
      'HAVE_STRLCPY',
      '_FILE_OFFSET_BITS=64',
      'ANDROID_SMP=0',
      "OS_PATH_SEPARATOR='/'",
      'OS_SHARED_LIB_FORMAT_STR="lib%s.dylib"',
      'ANDROID_STATICALLY_LINKED',
      'HAVE_SYS_UIO_H',
    ],

    'xcode_settings': {
      'SDKROOT': '<(BUILD_SDK)',
      'ARCHS': [ '<(BUILD_ARCH)' ],
      'VALID_ARCHS': [ '<(BUILD_ARCH)' ],
      'ONLY_ACTIVE_ARCH': 'YES',
      'CLANG_CXX_LANGUAGE_STANDARD': 'c++11',
      'CLANG_CXX_LIBRARY': 'libc++',
      'GCC_C_LANGUAGE_STANDARD': 'c99',
      'GCC_OPTIMIZATION_LEVEL': '0', # TODO
      'OTHER_CFLAGS': [ '-fvisibility-inlines-hidden' ]
    },

    'dependencies+': [
      '<!(<(dependency) linuxemu)',
      '<!(<(dependency) bionicemu)',
    ],

    'target_conditions': [
      [ '_type == "shared_library" or _type == "executable"', {
        'conditions': [
          [ 'GENERATOR == "xcode"', {
            'xcode_settings': {
              'CONFIGURATION_BUILD_DIR': '<(bin_root)',
              'LD_NO_PIE': 'YES', # to get mmap(addr) working
            },
          }, {
            'product_dir': '<(bin_root)',
          }],
        ],
      }],
      [ '_type == "static_library"', {
        'conditions': [
          [ 'GENERATOR == "xcode"', {
            'xcode_settings': {
              'CONFIGURATION_BUILD_DIR': '<(lib_root)'
            },
          }, {
            'product_dir': '<(lib_root)',
          }],
        ],
      }],
      [ '_type == "shared_library"', {
        'xcode_settings': {
          'LD_DYLIB_INSTALL_NAME': '@executable_path/$(EXECUTABLE_PATH)',
        },
      }],
    ],
  },
}