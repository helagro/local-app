
#include "config/env_variables.hpp"
#include "utils/log.hpp"
#include "vault/vault.hpp"

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

  const File config_file = get_file(CONFIG_FILE);

  app_log("Config file path:", ' ');
  app_log(config_file.get_path(), '\n', false);

  app_log("Config file content:");
  app_log(config_file.read().c_str());

  return 0;
}
