#include "file_shell.hpp"
#include "config/json_config_handler.hpp"
#include "internal/synced_commands.hpp"
#include "internal/unsynced_commands.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

void run_file_shell() {
  try {
    const JsonConfig config = get_config();
    const std::string file_shell_file_path = config.vault_path.file_shell;
    const std::string file_shell_output_path = config.vault_path.file_shell_output;

    const File shell_file = get_file(file_shell_file_path);
    const File shell_output_file = get_file(file_shell_output_path);

    std::string shell_output = run_unsynced_commands(shell_file);
    shell_output += run_synced_commands(shell_file);
    shell_output_file.write(shell_output);

  } catch (const std::exception &e) {
    app_log(std::string("Error in file shell: ") + e.what());
  }
}
