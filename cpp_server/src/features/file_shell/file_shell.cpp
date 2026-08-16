#include "file_shell.hpp"
#include "config/json_config_handler.hpp"
#include "internal/synced_commands.hpp"
#include "internal/unsynced_commands.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

namespace {
File get_scheduling_file() {
  const JsonConfig config = get_config();
  const std::string file_shell_file_path = config.vault_path.file_shell;

  return get_file(file_shell_file_path);
}

} // namespace

void run_file_shell() {
  try {
    const File shell_file = get_scheduling_file();

    run_unsynced_commands(shell_file);
    run_synced_commands(shell_file);
  } catch (const std::exception &e) {
    app_log(std::string("Error in file shell: ") + e.what());
  }
}
