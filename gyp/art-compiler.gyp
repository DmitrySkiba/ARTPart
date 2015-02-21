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
  'includes': [
    'common.gypi',
    'art-common.gypi',
  ],

  'variables': {
    'local_root': '<(art_root)/compiler',
  },

  'targets': [
    {
      'target_name': 'art-compiler',
      'product_name': 'compiler',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) art-runtime)',
        '<!(<(dependency) system-include)',
        '<!(<(dependency) system-libcutils)',
        '<!(<(dependency) system-liblog)',
        '<!(<(dependency) libnativehelper)',
        '<!(<(dependency) libcurses)',
        '<!(<(dependency) external-valgrind)',
        'external-gtest.gyp:external-gtest-include',
      ],

      'sources': [

        '<(local_root)/generated_operator_out.cc', # TODO generate during build

        '<(local_root)/buffered_output_stream.cc',
        '<(local_root)/compiled_method.cc',
        '<(local_root)/compiler.cc',
        '<(local_root)/compilers.cc',
        '<(local_root)/dex/bb_optimizations.cc',
        '<(local_root)/dex/dex_to_dex_compiler.cc',
        '<(local_root)/dex/frontend.cc',
        '<(local_root)/dex/global_value_numbering.cc',
        '<(local_root)/dex/local_value_numbering.cc',
        '<(local_root)/dex/mir_analysis.cc',
        '<(local_root)/dex/mir_dataflow.cc',
        '<(local_root)/dex/mir_field_info.cc',
        '<(local_root)/dex/mir_graph.cc',
        '<(local_root)/dex/mir_method_info.cc',
        '<(local_root)/dex/mir_optimization.cc',
        '<(local_root)/dex/pass_driver_me_opts.cc',
        '<(local_root)/dex/pass_driver_me_post_opt.cc',
        '<(local_root)/dex/post_opt_passes.cc',
        '<(local_root)/dex/quick/codegen_util.cc',
        '<(local_root)/dex/quick/dex_file_method_inliner.cc',
        '<(local_root)/dex/quick/dex_file_to_method_inliner_map.cc',
        '<(local_root)/dex/quick/gen_common.cc',
        '<(local_root)/dex/quick/gen_invoke.cc',
        '<(local_root)/dex/quick/gen_loadstore.cc',
        '<(local_root)/dex/quick/local_optimizations.cc',
        '<(local_root)/dex/quick/mir_to_lir.cc',
        '<(local_root)/dex/quick/ralloc_util.cc',
        '<(local_root)/dex/quick/resource_mask.cc',
        '<(local_root)/dex/quick_compiler_callbacks.cc',
        '<(local_root)/dex/ssa_transformation.cc',
        '<(local_root)/dex/verification_results.cc',
        '<(local_root)/dex/verified_method.cc',
        '<(local_root)/dex/vreg_analysis.cc',
        '<(local_root)/driver/compiler_driver.cc',
        '<(local_root)/driver/dex_compilation_unit.cc',
        '<(local_root)/elf_fixup.cc',
        '<(local_root)/elf_patcher.cc',
        '<(local_root)/elf_stripper.cc',
        '<(local_root)/elf_writer.cc',
        '<(local_root)/elf_writer_quick.cc',
        '<(local_root)/file_output_stream.cc',
        '<(local_root)/image_writer.cc',
        '<(local_root)/jni/quick/calling_convention.cc',
        '<(local_root)/jni/quick/jni_compiler.cc',
        '<(local_root)/oat_writer.cc',
        '<(local_root)/trampolines/trampoline_compiler.cc',
        '<(local_root)/utils/arena_allocator.cc',
        '<(local_root)/utils/arena_bit_vector.cc',
        '<(local_root)/utils/assembler.cc',
        '<(local_root)/utils/scoped_arena_allocator.cc',
        '<(local_root)/vector_output_stream.cc',

        # ART_USE_X86_INSTRUCTION_SET
        '<(local_root)/dex/quick/x86/assemble_x86.cc',
        '<(local_root)/dex/quick/x86/call_x86.cc',
        '<(local_root)/dex/quick/x86/fp_x86.cc',
        '<(local_root)/dex/quick/x86/int_x86.cc',
        '<(local_root)/dex/quick/x86/target_x86.cc',
        '<(local_root)/dex/quick/x86/utility_x86.cc',
        '<(local_root)/jni/quick/x86/calling_convention_x86.cc',
        '<(local_root)/utils/x86/assembler_x86.cc',
        '<(local_root)/utils/x86/managed_register_x86.cc',
      ],
    },
  ],
}
