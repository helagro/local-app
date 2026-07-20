#include "log.hpp"

#include <array>
#include <cstdio>
#include <ctime>
#include <iostream>
#include <string>

#define LOGS_MAX 500

unsigned int log_index = 0;
std::array<std::string, LOGS_MAX> logs;

void log_vault(const char *message) { app_log(message); }

void app_log(std::string message, const char postfix, const bool include_date) { app_log(message.c_str(), postfix, include_date); }

void app_log(const char *message, const char postfix, const bool include_date) {
  std::string log_entry;

  if (include_date) {
    std::time_t t = std::time(nullptr);
    std::tm *tm_ptr = std::localtime(&t);

    char buffer[50];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm_ptr);

    log_entry = "[" + std::string(buffer) + "] " + std::string(message) + postfix;
  } else {
    log_entry = std::string(message) + postfix;
  }

  printf("%s", log_entry.c_str());

  logs[log_index] = log_entry;
  log_index = (log_index + 1) % LOGS_MAX;
}

std::string get_logs_string() {
  std::string logs_string;
  unsigned int print_index = (log_index + 1) % LOGS_MAX;

  for (unsigned int i = 0; i < LOGS_MAX; ++i) {
    const std::string &log_entry = logs[print_index];
    if (!log_entry.empty()) {
      logs_string += log_entry;
    }
    print_index = (print_index + 1) % LOGS_MAX;
  }

  return logs_string;
}
