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

#include_next <pthread.h>

#ifndef LINUXEMU_PTHREAD_H_
#define LINUXEMU_PTHREAD_H_

#include <time.h>

__BEGIN_DECLS

extern int pthread_getcpuclockid(pthread_t thread, clockid_t *clock_id);

__END_DECLS

#endif /* LINUXEMU_PTHREAD_H_ */
