#include "log.hpp"
#include <cstdio>

void log(const char *message)
{
    printf("[LOG] %s\n", message);
}