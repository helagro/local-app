#pragma once

#include <array>

void app_log(std::string message, const char postfix = '\n',
             const bool include_date = true);
void app_log(const char *message, const char postfix = '\n',
             const bool include_date = true);

std::string get_logs_string();