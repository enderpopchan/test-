#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char *greet(const char *name) {
    char buf[16];
    strcpy(buf, name);          /* buffer overflow */
    return buf;                 /* returns address of a local */
}

void read_line(void) {
    char line[32];
    gets(line);                 /* unbounded read */
    printf(line);               /* format string vulnerability */
}

int *make(int n) {
    int *p = malloc(n * sizeof(int));   /* n * 4 can overflow, malloc unchecked */
    p[0] = 1;                   /* NULL deref if malloc failed */
    return p;
}

void use_after_free(void) {
    char *s = malloc(8);
    free(s);
    s[0] = 'x';                 /* use after free */
    free(s);                    /* double free */
}

void leak(void) {
    char *s = malloc(100);
    s[0] = 'a';                 /* never freed */
}

int sum(int *a, int n) {
    int total;                  /* uninitialized */
    for (int i = 0; i <= n; i++)
        total += a[i];          /* off-by-one read */
    return total;
}

int compare(int a, unsigned int b) {
    return a < b;               /* signed/unsigned comparison: -1 < 1u is false */
}

size_t len(char *a[]) {
    return sizeof(a) / sizeof(a[0]);   /* sizeof a pointer, not the array */
}

void copy(char *dst, const char *src, size_t n) {
    strncpy(dst, src, n);       /* may not be NUL-terminated */
}

void toctou(const char *path) {
    if (access(path, W_OK) == 0) {      /* check, then use */
        FILE *f = fopen(path, "w");
        fputs("data", f);               /* f may be NULL, never closed */
    }
}

void run(char *arg) {
    char cmd[128];
    sprintf(cmd, "ls %s", arg); /* overflow and command injection */
    system(cmd);
}

int token(void) {
    return rand();              /* predictable, unseeded */
}

int main(void) {
    char *s = greet("a very long name that overflows");
    printf("%s\n", s);
    return 0;
}
