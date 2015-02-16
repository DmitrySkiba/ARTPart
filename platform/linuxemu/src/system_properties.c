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

#include <stddef.h>
#include <sys/system_properties.h>
#include <assert.h>

int __system_property_get(const char *name, char *value) {
    if (value) {
        *value = 0;
    }
    return 0;
}

int __system_property_set(const char *key, const char *value) {
    assert(0 && "__system_property_set not implemented");
    return 0;
}

const prop_info *__system_property_find(const char *name) {
    assert(0 && "__system_property_find not implemented");
    return NULL;
}

int __system_property_read(const prop_info *pi, char *name, char *value) {
    assert(0 && "__system_property_read not implemented");
    return 0;
}

const prop_info *__system_property_find_nth(unsigned n) {
    assert(0 && "__system_property_find_nth not implemented");
    return NULL;
}

int __system_property_foreach(void (*propfn)(const prop_info *pi, void *cookie), void *cookie) {
    assert(0 && "__system_property_foreach not implemented");
    return NULL;
}
