
#include "config/env_variables.hpp"
#include "config/json_config_handler.hpp"
#include "features/status/status.hpp"
#include "server/server.h"
#include "utils/log.hpp"
#include <iostream>
#include <thread>

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

  load_config();

  app_log("Current logs:");
  std::string logs = get_logs_string();
  app_log(logs.c_str());

  std::thread server_thread(run_server);

  while (true) {
    std::this_thread::sleep_for(std::chrono::seconds(15));
    write_status();
  }

  return 0;
}
