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

#include <pthread.h>
#include <sys/types.h>
#include "private/bionic_pthread.h"
#include <assert.h>
#include <errno.h>

// Must be in sync with gettid()
pid_t __pthread_gettid(pthread_t thid) {
    union {
        pid_t tid;
        __uint64_t threadid;
    } value;
    int error = pthread_threadid_np(thid, &value.threadid);
    assert(!error);
    assert(value.tid == value.threadid);
    return value.tid;
}

int __pthread_settid(pthread_t thid, pid_t tid) {
    assert(0);
    return ENOSYS;
}
