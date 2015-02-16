/*
 * Copyright (C) 2015 Dmitry Skiba
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

#include_next <sys/types.h>

#ifndef LINUXEMU_SYS_TYPES_H_
#define LINUXEMU_SYS_TYPES_H_

typedef off_t off64_t;

__BEGIN_DECLS

extern pid_t gettid();

__END_DECLS

#endif // LINUXEMU_SYS_TYPES_H_
