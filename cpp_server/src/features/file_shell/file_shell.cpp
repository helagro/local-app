#include "file_shell.hpp"
#include "api/python_server/python_server.hpp"
#include "config/json_config_handler.hpp"
#include "internal/synced_commands.hpp"
#include "internal/unsynced_commands.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

namespace {
File get_shell_file() {
  const JsonConfig config = get_config();
  const std::string file_shell_file_path = config.vault_path.file_shell;

  return get_file(file_shell_file_path);
}

void run_command(std::string command) {
  replace(command.begin(), command.end(), ' ', '/');

  std::string response;
  python_server_get("/" + command, &response);

  app_log("Command response: " + response);
}
} // namespace

void run_file_shell() {
  try {
    const File shell_file = get_shell_file();

    run_unsynced_commands(shell_file, run_command);
    run_synced_commands(shell_file, run_command);
  } catch (const std::exception &e) {
    app_log(std::string("Error in file shell: ") + e.what());
  }
}
