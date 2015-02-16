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

#include_next <time.h>

#ifndef LINUXEMU_TIME_H_
#define LINUXEMU_TIME_H_

__BEGIN_DECLS

typedef int clockid_t;

extern int clock_getres(clockid_t, struct timespec *);
extern int clock_gettime(clockid_t, struct timespec *);

extern int clock_nanosleep(clockid_t clock_id, int flags,
                           const struct timespec *request,
                           struct timespec *remain);

#define CLOCK_REALTIME             0
#define CLOCK_MONOTONIC            1
#define CLOCK_PROCESS_CPUTIME_ID   2
#define CLOCK_THREAD_CPUTIME_ID    3
#define CLOCK_MONOTONIC_RAW        4
#define CLOCK_REALTIME_COARSE      5
#define CLOCK_MONOTONIC_COARSE     6
#define CLOCK_BOOTTIME             7
#define CLOCK_REALTIME_ALARM       8
#define CLOCK_BOOTTIME_ALARM       9

#define TIMER_ABSTIME 0x01

__END_DECLS

#endif /* LINUXEMU_TIME_H_ */
