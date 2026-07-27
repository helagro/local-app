#include "api/python_server/python_server.hpp"
#include "config/json_config_handler.hpp"
#include "unsynced_commands.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

namespace {

void clear_shell_file(File shell_file) {
  const bool write_success = shell_file.write("\tLoc do\n----\n");

  if (!write_success) {
    throw std::runtime_error("Failed to clear file shell file");
  }
}

std::string get_file_shell_content(File shell_file) {
  const std::optional<std::string> shell_file_content = shell_file.read();

  if (!shell_file_content.has_value()) {
    throw std::runtime_error("Failed to read file shell file");
  }

  return shell_file_content.value();
}
} // namespace

void run_synced_commands(const File shell_file, std::function<void(const std::string &)> run_command) {
  const std::string shell_file_content_str = get_file_shell_content(shell_file);
  clear_shell_file(shell_file);

  size_t command_line_end = 0;

  while (true) {
    const size_t command_line_start = shell_file_content_str.find("- [ ] ", command_line_end);
    if (command_line_start == std::string::npos) {
      if (command_line_end == 0) {
        app_log("No commands found in file shell");
        return;
      } else {
        break;
      }
    }

    const size_t command_start = command_line_start + 6; // Length of "- [ ] "
    command_line_end = shell_file_content_str.find('\n', command_start);
    if (command_line_end == std::string::npos) {
      throw std::runtime_error("Failed to find end of command line in file shell");
    }

    const std::string command = shell_file_content_str.substr(command_start, command_line_end - command_start);
    app_log("Command line: \"" + command + "\"");

    run_command(command);
  }
}