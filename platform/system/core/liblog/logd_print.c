#include <android/log.h>
#include <log/logd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define LOG_BUF_SIZE 1024

int __android_log_write(int prio, const char *tag, const char *text) {
    if (prio == ANDROID_LOG_VERBOSE) {
        return 0;
    }
    const char* prioString = NULL;
    char prioStringBuffer[6];
    switch (prio) {
        case ANDROID_LOG_VERBOSE:   prioString = "....V"; break;
        case ANDROID_LOG_DEBUG:     prioString = "DEBUG"; break;
        case ANDROID_LOG_INFO:      prioString = ".INFO"; break;
        case ANDROID_LOG_WARN:      prioString = ".WARN"; break;
        case ANDROID_LOG_ERROR:     prioString = "ERROR"; break;
        case ANDROID_LOG_FATAL:     prioString = "FATAL"; break;
        default:
            snprintf(prioStringBuffer, sizeof(prioStringBuffer), "?% 3d?", prio);
            prioString = prioStringBuffer;
            break;
    }

    static bool stdoutBufferingDisabled = false;
    if (!stdoutBufferingDisabled) {
      stdoutBufferingDisabled = true;
      setvbuf(stdout, NULL, _IONBF, 0);
    }

    return printf("%s/%s: %s\n", prioString, tag, text);
}

int __android_log_print(int prio, const char *tag,  const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    __android_log_vprint(prio, tag, fmt, args);
    va_end(args);
    return 0;
}

int __android_log_vprint(int prio, const char *tag, const char *fmt, va_list args) {
    char msg[LOG_BUF_SIZE];
    vsnprintf(msg, LOG_BUF_SIZE, fmt, args);
    return __android_log_write(prio, tag, msg);
}

void __android_log_assert(const char *cond, const char *tag, const char *fmt, ...) {
    va_list ap;
    char buf[LOG_BUF_SIZE];

    va_start(ap, fmt);
    vsnprintf(buf, LOG_BUF_SIZE, fmt, ap);
    va_end(ap);

    __android_log_write(ANDROID_LOG_FATAL, tag, buf);

    exit(1);
}

int __android_log_bwrite(int32_t tag, const void *payload, size_t len) {
    __android_log_write(ANDROID_LOG_ERROR, "android_log", "__android_log_bwrite is not implemented!");
    return -1;
}

int __android_log_btwrite(int32_t tag, char type, const void *payload, size_t len) {
    __android_log_write(ANDROID_LOG_ERROR, "android_log", "__android_log_btwrite is not implemented!");
    return -1;
}

int __android_log_buf_write(int bufID, int prio, const char *tag, const char *text) {
    return __android_log_write(prio, tag, text);
}

int __android_log_buf_print(int bufID, int prio, const char *tag, const char *fmt, ...) {
    va_list ap;
    char buf[LOG_BUF_SIZE];

    va_start(ap, fmt);
    vsnprintf(buf, LOG_BUF_SIZE, fmt, ap);
    va_end(ap);

    return __android_log_buf_write(bufID, prio, tag, buf);
}
