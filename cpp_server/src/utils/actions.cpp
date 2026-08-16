#include "actions.hpp"
#include "api/python_server/python_server.hpp"
#include "utils/log.hpp"
#include <algorithm>
#include <stdexcept>
#include <string>

void run_command(std::string command) {
  std::string response = "No response recorded";

  if (command.empty()) {
    throw std::runtime_error("Command is empty");
  }

  if (command.length() > 2 && command[0] == '+') {
    std::replace(command.begin(), command.end(), ':', '#');

    python_server_socket("ADD " + command.substr(1));
  } else {
    std::replace(command.begin(), command.end(), ' ', '/');

    python_server_get("/" + command, &response);
  }

  app_log("Command: " + command + " | Response: " + response);
}