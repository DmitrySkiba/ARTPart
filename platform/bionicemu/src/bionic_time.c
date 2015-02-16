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

#include "bionic_time.h"
#include <assert.h>

size_t strftime_tz(char* s, size_t max, const char* format, const struct tm* tm, const struct strftime_locale* lc) {
    assert(0);
    return 0;
}

time_t mktime_tz(struct tm* const tmp, char const* tz) {
    assert(0);
    return 0;
}

void localtime_tz(const time_t* const timep, struct tm* tmp, const char* tz) {
    assert(0);
}

