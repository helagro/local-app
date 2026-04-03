#include "log.hpp"

#include <cstdio>
#include <ctime>

void log_vault(const char *message) { app_log(message); }

void app_log(const char *message, const char postfix, const bool include_date) {
  if (include_date) {
    std::time_t t = std::time(nullptr);
    std::tm *tm_ptr = std::localtime(&t);

    char buffer[50];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d", tm_ptr);

    printf("[%s] %s%c", buffer, message, postfix);
  } else {
    printf("%s%c", message, postfix);
  }
}
