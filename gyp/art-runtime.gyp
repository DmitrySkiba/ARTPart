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
    'local_root': '<(art_root)/runtime',
  },

  'targets': [
    {
      'target_name': 'art-runtime<(any_variant)',
      'product_name': 'runtime',
      'type': 'static_library',

      'dependencies': [
        '<!(<(dependency) libnativehelper)',
        '<!(<(dependency) system-include)',
        '<!(<(dependency) system-libcutils)',
        '<!(<(dependency) system-libutils)',
        '<!(<(dependency) system-liblog)',
        '<!(<(dependency) system-libnativebridge)',
        '<!(<(dependency) system-libziparchive)',
        '<!(<(dependency) libcore-libjavacore)',
        '<!(<(dependency) zlib)',
        '<!(<(dependency) external-valgrind)',
        'external-gtest.gyp:external-gtest-include<(any_variant)', # TODO improve <(dependency)
      ],

      'export_dependent_settings': [
        '<!(<(dependency) libnativehelper)',
        '<!(<(dependency) system-libziparchive)',
        'external-gtest.gyp:external-gtest-include<(any_variant)', # TODO improve <(dependency)
      ],

      'all_dependent_settings': {
        'target_conditions': [
          [ '_type == "shared_library" or _type == "executable"', {
            'xcode_settings': {
              'OTHER_LDFLAGS': [
                '-read_only_relocs suppress',
                '-Wl,-no_compact_unwind',
              ],
            }
          }],
        ],
      },

      'xcode_settings': {
        'ALWAYS_SEARCH_USER_PATHS': 'NO',
      },

      'include_dirs': [
        '<(art_root)/sigchainlib',
      ],

      'defines': [
        'ART_BASE_ADDRESS=<(boot_oat_base)',
        'ART_BASE_ADDRESS_MIN_DELTA=-0x1000000',
        'ART_BASE_ADDRESS_MAX_DELTA=0x1000000',
        'ART_DEFAULT_GC_TYPE_IS_CMS',
        'ART_DEFAULT_INSTRUCTION_SET_FEATURES=default',
      ],

      'sources': [
        '<(art_root)/sigchainlib/sigchain.cc',

        '<(local_root)/generated_operator_out.cc', # TODO generate during build

        '<(local_root)/arch/context.cc',
        '<(local_root)/arch/memcmp16.cc',
        '<(local_root)/atomic.cc',
        '<(local_root)/barrier.cc',
        '<(local_root)/base/allocator.cc',
        '<(local_root)/base/bit_vector.cc',
        '<(local_root)/base/hex_dump.cc',
        '<(local_root)/base/logging.cc',
        '<(local_root)/base/logging_android.cc',
        '<(local_root)/base/mutex.cc',
        '<(local_root)/base/scoped_flock.cc',
        '<(local_root)/base/stringpiece.cc',
        '<(local_root)/base/stringprintf.cc',
        '<(local_root)/base/timing_logger.cc',
        '<(local_root)/base/unix_file/fd_file.cc',
        '<(local_root)/base/unix_file/mapped_file.cc',
        '<(local_root)/base/unix_file/null_file.cc',
        '<(local_root)/base/unix_file/random_access_file_utils.cc',
        '<(local_root)/base/unix_file/string_file.cc',
        '<(local_root)/check_jni.cc',
        '<(local_root)/class_linker.cc',
        '<(local_root)/common_throws.cc',
        '<(local_root)/debugger.cc',
        '<(local_root)/dex_file.cc',
        '<(local_root)/dex_file_verifier.cc',
        '<(local_root)/dex_instruction.cc',
        '<(local_root)/elf_file.cc',
        '<(local_root)/entrypoints/entrypoint_utils.cc',
        '<(local_root)/entrypoints/interpreter/interpreter_entrypoints.cc',
        '<(local_root)/entrypoints/jni/jni_entrypoints.cc',
        '<(local_root)/entrypoints/math_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_alloc_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_cast_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_deoptimization_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_dexcache_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_field_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_fillarray_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_instrumentation_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_jni_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_lock_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_math_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_thread_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_throw_entrypoints.cc',
        '<(local_root)/entrypoints/quick/quick_trampoline_entrypoints.cc',
        '<(local_root)/fault_handler.cc',
        '<(local_root)/field_helper.cc',
        '<(local_root)/gc/accounting/card_table.cc',
        '<(local_root)/gc/accounting/heap_bitmap.cc',
        '<(local_root)/gc/accounting/mod_union_table.cc',
        '<(local_root)/gc/accounting/remembered_set.cc',
        '<(local_root)/gc/accounting/space_bitmap.cc',
        '<(local_root)/gc/allocator/rosalloc.cc',
        '<(local_root)/gc/collector/concurrent_copying.cc',
        '<(local_root)/gc/collector/garbage_collector.cc',
        '<(local_root)/gc/collector/immune_region.cc',
        '<(local_root)/gc/collector/mark_compact.cc',
        '<(local_root)/gc/collector/mark_sweep.cc',
        '<(local_root)/gc/collector/partial_mark_sweep.cc',
        '<(local_root)/gc/collector/semi_space.cc',
        '<(local_root)/gc/collector/sticky_mark_sweep.cc',
        '<(local_root)/gc/gc_cause.cc',
        '<(local_root)/gc/heap.cc',
        '<(local_root)/gc/reference_processor.cc',
        '<(local_root)/gc/reference_queue.cc',
        '<(local_root)/gc/space/bump_pointer_space.cc',
        '<(local_root)/gc/space/image_space.cc',
        '<(local_root)/gc/space/large_object_space.cc',
        '<(local_root)/gc/space/malloc_space.cc',
        '<(local_root)/gc/space/rosalloc_space.cc',
        '<(local_root)/gc/space/space.cc',
        '<(local_root)/gc/space/zygote_space.cc',
        '<(local_root)/hprof/hprof.cc',
        '<(local_root)/image.cc',
        '<(local_root)/indirect_reference_table.cc',
        '<(local_root)/instruction_set.cc',
        '<(local_root)/instrumentation.cc',
        '<(local_root)/intern_table.cc',
        '<(local_root)/interpreter/interpreter.cc',
        '<(local_root)/interpreter/interpreter_common.cc',
        '<(local_root)/interpreter/interpreter_goto_table_impl.cc',
        '<(local_root)/interpreter/interpreter_switch_impl.cc',
        '<(local_root)/jdwp/jdwp_adb.cc',
        '<(local_root)/jdwp/jdwp_event.cc',
        '<(local_root)/jdwp/jdwp_expand_buf.cc',
        '<(local_root)/jdwp/jdwp_handler.cc',
        '<(local_root)/jdwp/jdwp_main.cc',
        '<(local_root)/jdwp/jdwp_request.cc',
        '<(local_root)/jdwp/jdwp_socket.cc',
        '<(local_root)/jdwp/object_registry.cc',
        '<(local_root)/jni_internal.cc',
        '<(local_root)/jobject_comparator.cc',
        '<(local_root)/mem_map.cc',
        '<(local_root)/memory_region.cc',
        '<(local_root)/method_helper.cc',
        '<(local_root)/mirror/array.cc',
        '<(local_root)/mirror/art_field.cc',
        '<(local_root)/mirror/art_method.cc',
        '<(local_root)/mirror/class.cc',
        '<(local_root)/mirror/dex_cache.cc',
        '<(local_root)/mirror/object.cc',
        '<(local_root)/mirror/reference.cc',
        '<(local_root)/mirror/stack_trace_element.cc',
        '<(local_root)/mirror/string.cc',
        '<(local_root)/mirror/throwable.cc',
        '<(local_root)/monitor.cc',
        '<(local_root)/monitor_android.cc',
        '<(local_root)/native/dalvik_system_DexFile.cc',
        '<(local_root)/native/dalvik_system_VMDebug.cc',
        '<(local_root)/native/dalvik_system_VMRuntime.cc',
        '<(local_root)/native/dalvik_system_VMStack.cc',
        '<(local_root)/native/dalvik_system_ZygoteHooks.cc',
        '<(local_root)/native/java_lang_Class.cc',
        '<(local_root)/native/java_lang_DexCache.cc',
        '<(local_root)/native/java_lang_Object.cc',
        '<(local_root)/native/java_lang_Runtime.cc',
        '<(local_root)/native/java_lang_String.cc',
        '<(local_root)/native/java_lang_System.cc',
        '<(local_root)/native/java_lang_Thread.cc',
        '<(local_root)/native/java_lang_Throwable.cc',
        '<(local_root)/native/java_lang_VMClassLoader.cc',
        '<(local_root)/native/java_lang_ref_FinalizerReference.cc',
        '<(local_root)/native/java_lang_ref_Reference.cc',
        '<(local_root)/native/java_lang_reflect_Array.cc',
        '<(local_root)/native/java_lang_reflect_Constructor.cc',
        '<(local_root)/native/java_lang_reflect_Field.cc',
        '<(local_root)/native/java_lang_reflect_Method.cc',
        '<(local_root)/native/java_lang_reflect_Proxy.cc',
        '<(local_root)/native/java_util_concurrent_atomic_AtomicLong.cc',
        '<(local_root)/native/org_apache_harmony_dalvik_ddmc_DdmServer.cc',
        '<(local_root)/native/org_apache_harmony_dalvik_ddmc_DdmVmInternal.cc',
        '<(local_root)/native/sun_misc_Unsafe.cc',
        '<(local_root)/native_bridge_art_interface.cc',
        '<(local_root)/oat.cc',
        '<(local_root)/oat_file.cc',
        '<(local_root)/object_lock.cc',
        '<(local_root)/offsets.cc',
        '<(local_root)/os_linux.cc',
        '<(local_root)/parsed_options.cc',
        '<(local_root)/primitive.cc',
        '<(local_root)/profiler.cc',
        '<(local_root)/quick/inline_method_analyser.cc',
        '<(local_root)/quick_exception_handler.cc',
        '<(local_root)/reference_table.cc',
        '<(local_root)/reflection.cc',
        '<(local_root)/runtime.cc',
        '<(local_root)/runtime_android.cc',
        '<(local_root)/signal_catcher.cc',
        '<(local_root)/stack.cc',
        '<(local_root)/thread.cc',
        '<(local_root)/thread_android.cc',
        '<(local_root)/thread_list.cc',
        '<(local_root)/thread_pool.cc',
        '<(local_root)/throw_location.cc',
        '<(local_root)/trace.cc',
        '<(local_root)/transaction.cc',
        '<(local_root)/utf.cc',
        '<(local_root)/utils.cc',
        '<(local_root)/verifier/dex_gc_map.cc',
        '<(local_root)/verifier/instruction_flags.cc',
        '<(local_root)/verifier/method_verifier.cc',
        '<(local_root)/verifier/reg_type.cc',
        '<(local_root)/verifier/reg_type_cache.cc',
        '<(local_root)/verifier/register_line.cc',
        '<(local_root)/well_known_classes.cc',
        '<(local_root)/zip_archive.cc',

        # ART_USE_DLMALLOC_ALLOCATOR
        #'<(local_root)/gc/allocator/dlmalloc.cc',
        #'<(local_root)/gc/space/dlmalloc_space.cc',

        # ART_USE_X86_INSTRUCTION_SET
        '<(local_root)/arch/x86/context_x86.cc',
        '<(local_root)/arch/x86/entrypoints_init_x86.cc',
        '<(local_root)/arch/x86/fault_handler_x86.cc',
        '<(local_root)/arch/x86/registers_x86.cc',
        '<(local_root)/arch/x86/thread_x86.cc',
        '<(local_root)/arch/x86/asm_support_x86.S',
        '<(local_root)/arch/x86/jni_entrypoints_x86.S',
        '<(local_root)/arch/x86/memcmp16_x86.S',
        '<(local_root)/arch/x86/quick_entrypoints_x86.S',
      ],
    },
  ],
}