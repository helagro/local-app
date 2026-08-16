#include "scheduled.hpp"
#include "config/json_config_handler.hpp"
#include "utils/actions.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"

namespace {
u_short last_hour = 26;

File get_scheduling_file() {
  const JsonConfig config = get_config();
  const std::string file_shell_file_path = config.vault_path.scheduled_commands;

  return get_file(file_shell_file_path);
}
} // namespace

void run_scheduled() {
  try {
    File file = get_scheduling_file();
    const std::string content = file.read().value_or("");

    const std::time_t t = std::time(nullptr);
    const std::tm *tm_ptr = std::localtime(&t);
    const u_short current_hour = tm_ptr->tm_hour;

    if (current_hour == last_hour) {
      return;
    }
    last_hour = current_hour;

    size_t hour_end = 0;

    while (true) {
      const size_t line_start = content.find("- [ ] ", hour_end);
      if (line_start == std::string::npos) {
        return;
      }

      const size_t hour_start = line_start + 6; // Length of "- [ ] "
      hour_end = content.find(" ; ", hour_start);
      if (hour_end == std::string::npos) {
        throw std::runtime_error("Failed to find end of command line in scheduled file");
      }

      const std::string hour_str = content.substr(hour_start, hour_end - hour_start);
      if (hour_str.empty()) {
        throw std::runtime_error("Failed to find hour in scheduled file");
      }

      const u_short scheduled_hour = std::stoi(hour_str);
      if (scheduled_hour == current_hour) {
        const size_t command_start = hour_end + 3; // Length of " ; "
        const size_t command_end = content.find("\n", command_start);
        if (command_end == std::string::npos) {
          throw std::runtime_error("Failed to find end of command line in scheduled file");
        }

        const std::string command = content.substr(command_start, command_end - command_start);
        if (command.empty()) {
          throw std::runtime_error("Failed to find command in scheduled file");
        }

        run_command(command);
      }
    }
  } catch (const std::exception &e) {
    app_log(std::string("Error in scheduled: ") + e.what());
  }
}