
#include "config/env_variables.hpp"
#include "config/json_config_handler.hpp"
#include "server/server.h"
#include "utils/log.hpp"

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
  start_server();

  return 0;
}
