/*
 * Copyright (C) 2012 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "disassembler.h"

#include <iostream>

#include "base/logging.h"
#include "base/stringprintf.h"

#ifdef ART_USE_ARM_INSTRUCTION_SET
#include "disassembler_arm.h"
#endif

#ifdef ART_USE_ARM64_INSTRUCTION_SET
#include "disassembler_arm64.h"
#endif

#ifdef ART_USE_MIPS_INSTRUCTION_SET
#include "disassembler_mips.h"
#endif

#ifdef ART_USE_X86_INSTRUCTION_SET
#include "disassembler_x86.h"
#endif


namespace art {

Disassembler* Disassembler::Create(InstructionSet instruction_set, DisassemblerOptions* options) {
  switch (instruction_set) {
#ifdef ART_USE_ARM_INSTRUCTION_SET
    case kArm: case kThumb2:
      return new arm::DisassemblerArm(options);
#endif
#ifdef ART_USE_ARM64_INSTRUCTION_SET
    case kArm64:
      return new arm64::DisassemblerArm64(options);
#endif
#ifdef ART_USE_MIPS_INSTRUCTION_SET
    case kMips:
      return new mips::DisassemblerMips(options);
#endif
#ifdef ART_USE_X86_INSTRUCTION_SET
    case kX86:
      return new x86::DisassemblerX86(options, false);
#endif
#ifdef ART_USE_X86_64_INSTRUCTION_SET
    case kX86_64:
      return new x86::DisassemblerX86(options, true);
#endif
    default:
      UNIMPLEMENTED(FATAL) << "no disassembler for " << instruction_set;
      return NULL;
  }
}

std::string Disassembler::FormatInstructionPointer(const uint8_t* begin) {
  if (disassembler_options_->absolute_addresses_) {
    return StringPrintf("%p", begin);
  } else {
    size_t offset = begin - disassembler_options_->base_address_;
    return StringPrintf("0x%08zx", offset);
  }
}

}  // namespace art
