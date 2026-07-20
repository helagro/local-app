
#include "config/env_variables.hpp"
#include "config/json_config_handler.hpp"
#include "features/file_shell/file_shell.hpp"
#include "features/status/status.hpp"
#include "server/server.h"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/constants.hpp"
#include "vault/vault.hpp"
#include <iostream>
#include <thread>

namespace {
void write_logs() {
  const JsonConfig config = get_config();
  if (!config.feature_toggle.sync_logs) {
    app_log("Syncing logs is disabled");
    return;
  }

  const File logs_file(get_file(LOG_FILE));

  const std::string logs_string = "```c\n" + get_logs_string() + "```\n";
  const bool write_success = logs_file.write(logs_string);

  if (!write_success) {
    app_log("Failed to write logs to file.");
  }
}
} // namespace

/* ================================== MAIN ================================== */

int main() {
  app_log("Application started.");

  const bool env_load_success = load_env_variables();
  if (!env_load_success) {
    return 1;
  }

  const EnvVariables *env = get_env_variables();

  app_log("Environment variable \"VAULT\":", ' ');
  app_log(env->vault, '\n', false);

  load_config(true);

  std::thread server_thread(run_server);

  /* main loop ---------------------------------------------------------------- */

  JsonConfig config = get_config();
  while (config.feature_toggle.master_switch) {
    if (config.feature_toggle.scheduled_sync) {
      if (config.feature_toggle.file_shell) {
        try {
          run_file_shell();
        } catch (const std::exception &e) {
          app_log(std::string("Error in file shell: ") + e.what());
        }
      }

      write_status();
    } else {
      app_log("Scheduled sync is disabled");
    }

    write_logs();

    const unsigned int sync_rate_mins = config.sync_rate_mins > 0 ? config.sync_rate_mins : 1;
    std::this_thread::sleep_for(std::chrono::minutes(sync_rate_mins));

    if (config.feature_toggle.scheduled_sync) {
      app_log("", '\n', false);
    }

    load_config();
    config = get_config();
  }

  /* exiting ------------------------------------------------------------------ */

  const std::string master_switch_status = config.feature_toggle.master_switch ? "ON" : "OFF";
  app_log("Master switch is: " + master_switch_status);
  app_log("Exiting application");

  write_logs();

  return 0;
}
