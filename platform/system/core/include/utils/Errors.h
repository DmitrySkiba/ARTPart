/*
 * Copyright (C) 2007 The Android Open Source Project
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

#ifndef ANDROID_ERRORS_H
#define ANDROID_ERRORS_H

#include <sys/types.h>
#include <errno.h>
#include <stdint.h>

namespace android {

// use this type to return error codes
#ifdef HAVE_MS_C_RUNTIME
typedef int         status_t;
#else
typedef int32_t     status_t;
#endif

/* the MS C runtime lacks a few error codes */

/*
 * Error codes. 
 * All error codes are negative values.
 */

// Win32 #defines NO_ERROR as well.  It has the same value, so there's no
// real conflict, though it's a bit awkward.
#ifdef _WIN32
# undef NO_ERROR
#endif
 
enum {
    OK                = 0,    // Everything's swell.
    NO_ERROR          = 0,    // No errors.
    
    UNKNOWN_ERROR       = INT32_MIN + 0,

    NO_MEMORY           = -ENOMEM,
    INVALID_OPERATION   = -ENOSYS,
    BAD_VALUE           = -EINVAL,
    BAD_TYPE            = INT32_MIN + 1,
    NAME_NOT_FOUND      = -ENOENT,
    PERMISSION_DENIED   = -EPERM,
    NO_INIT             = -ENODEV,
    ALREADY_EXISTS      = -EEXIST,
    DEAD_OBJECT         = -EPIPE,
    FAILED_TRANSACTION  = INT32_MIN + 2,
    JPARKS_BROKE_IT     = -EPIPE,
#if !defined(HAVE_MS_C_RUNTIME)
    BAD_INDEX           = -EOVERFLOW,
    NOT_ENOUGH_DATA     = -ENODATA,
    WOULD_BLOCK         = -EWOULDBLOCK, 
    TIMED_OUT           = -ETIMEDOUT,
    UNKNOWN_TRANSACTION = -EBADMSG,
#else    
    BAD_INDEX           = -E2BIG,
    NOT_ENOUGH_DATA     = INT32_MIN + 3,
    WOULD_BLOCK         = INT32_MIN + 4,
    TIMED_OUT           = INT32_MIN + 5,
    UNKNOWN_TRANSACTION = INT32_MIN + 6,
#endif    
    FDS_NOT_ALLOWED     = INT32_MIN + 7,
};

// Restore define; enumeration is in "android" namespace, so the value defined
// there won't work for Win32 code in a different namespace.
#ifdef _WIN32
# define NO_ERROR 0L
#endif

}; // namespace android
    
// ---------------------------------------------------------------------------
    
#endif // ANDROID_ERRORS_H
