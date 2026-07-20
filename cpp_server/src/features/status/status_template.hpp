#pragma once
#include <string>

struct Status {
  std::string message;
  std::string timestamp;
  std::string first_timestamp;
  std::string python_server_health;

  bool sync_logs;
};
