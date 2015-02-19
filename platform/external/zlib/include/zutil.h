#ifndef ZLIB_ZUTIL_H_
#define ZLIB_ZUTIL_H_

#include <zlib.h>

#if !defined(__APPLE__)
#error Unsupported platform
#else
#ifndef DEF_WBITS
#  define DEF_WBITS MAX_WBITS
#endif
#if MAX_MEM_LEVEL >= 8
#  define DEF_MEM_LEVEL 8
#else
#  define DEF_MEM_LEVEL MAX_MEM_LEVEL
#endif
#endif

#endif // ZLIB_ZUTIL_H_
