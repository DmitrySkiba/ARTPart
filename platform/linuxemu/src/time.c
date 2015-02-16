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

#include <time.h>
#include <assert.h>
#include <sys/time.h>
#include <mach/mach_time.h>
#include <stdbool.h>
#include <errno.h>
#include <checkint.h>
#include <stdint.h>

static bool is_timeofday_clock(clockid_t clock) {
    return  clock == CLOCK_REALTIME ||
            clock == CLOCK_REALTIME_COARSE;
}

static bool is_absolute_clock(clockid_t clock) {
    return  clock == CLOCK_BOOTTIME ||
            clock == CLOCK_MONOTONIC ||
            clock == CLOCK_MONOTONIC_RAW ||
            clock == CLOCK_MONOTONIC_COARSE;
}

static int unknown_clock(clockid_t clock) {
    if (clock == CLOCK_PROCESS_CPUTIME_ID ||
        clock == CLOCK_THREAD_CPUTIME_ID ||
        clock == CLOCK_REALTIME_ALARM ||
        clock == CLOCK_BOOTTIME_ALARM)
    {
        errno = ENOSYS;
        return -1;
    }

    errno = EINVAL;
    return -1;
}

static const mach_timebase_info_t mach_timebase(void) {
    static struct mach_timebase_info timebase = {0};
    if (!timebase.denom) {
        if (mach_timebase_info(&timebase) != KERN_SUCCESS) {
            errno = EAGAIN;
            return NULL;
        }
    }
    return &timebase;
}

/* API */

int clock_getres(clockid_t clock, struct timespec* result) {
    if (is_timeofday_clock(clock)) {
        if (result) {
            result->tv_sec = 0;
            result->tv_nsec = NSEC_PER_MSEC;
        }
        return 0;
    }

    if (is_absolute_clock(clock)) {
        const mach_timebase_info_t timebase = mach_timebase();
        if (!timebase) {
            return -1;
        }
        uint64_t resolution = timebase->numer / timebase->denom;
        if (!resolution) {
            resolution = 1;
        }
        if (result) {
            result->tv_sec = resolution / NSEC_PER_SEC;
            result->tv_nsec = resolution % NSEC_PER_SEC;
        }
        return 0;
    }

    return unknown_clock(clock);
}

int clock_gettime(clockid_t clock, struct timespec* result) {
    if (is_timeofday_clock(clock)) {
        struct timeval tv;
        if (gettimeofday(&tv, NULL) != 0) {
            return -1;
        }
        if (result) {
            result->tv_sec = tv.tv_sec;
            result->tv_nsec= tv.tv_usec * NSEC_PER_USEC;
        }
        return 0;
    }

    if (is_absolute_clock(clock)) {
        const mach_timebase_info_t timebase = mach_timebase();
        if (!timebase) {
            return -1;
        }

        uint64_t absolute_time = mach_absolute_time();

        int32_t check = CHECKINT_NO_ERROR;
        uint64_t time = check_uint64_mul(absolute_time, timebase->numer, &check);
        // Try 'time * numer / denom', fallback to 'time / denom * numer' on overflow.
        if (check & CHECKINT_OVERFLOW_ERROR) {
            check = CHECKINT_NO_ERROR;
            time = check_uint64_div(absolute_time, timebase->denom, &check);
            time = check_uint64_mul(time, timebase->numer, &check);
        } else {
            time = check_uint64_div(time, timebase->denom, &check);
        }
        if (check & CHECKINT_TYPE_ERROR) {
            errno = EDOM;
            return -1;
        }
        if (check & CHECKINT_OVERFLOW_ERROR) {
            errno = ERANGE;
            return -1;
        }

        if (result) {
            result->tv_sec = time / NSEC_PER_SEC;
            result->tv_nsec = time % NSEC_PER_SEC;
        }
        return 0;
    }

    return unknown_clock(clock);
}

int clock_nanosleep(clockid_t clock, int flags,
                    const struct timespec *request,
                    struct timespec *remain)
{
    if (!request) {
        return EINVAL;
    }

    // "CLOCK_THREAD_CPUTIME_ID is not a permitted value"
    if (clock == CLOCK_THREAD_CPUTIME_ID) {
        return EINVAL;
    }

    struct timespec relative;
    if (flags == TIMER_ABSTIME) {
        struct timespec now;
        if (clock_gettime(clock, &now)) {
            return errno;
        }

        if (CMP_MACH_TIMESPEC(&now, request) >= 0) {
            return 0;
        }

        relative = *request;
        SUB_MACH_TIMESPEC(&relative, &now);

        request = &relative;
        remain = NULL;
    }

    if (nanosleep(request, remain)) {
        return errno;
    }

    return 0;
}
