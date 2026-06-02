#pragma once
#include <string>

struct JsonConfig {
  unsigned int sync_rate_mins;
  std::string python_server_url;
};