#include <iostream>

#include "utils/log.hpp"

/* =============================== STRUCTURES =============================== */

struct EnvironmentVariables {
  char* vault;
};

/* ================================ NAMESPACE =============================== */

namespace {

EnvironmentVariables env;

bool load_env_variables() {
  char* vault = std::getenv("VAULT");
  if (!vault) {
    app_log("Environment variable VAULT is not set.");
    return false;
  }

  env.vault = vault;

  return true;
}

}  // namespace

/* ================================== MAIN ================================== */

int main() {
  app_log("Application started.");

  if (!load_env_variables()) {
    return 1;
  }

  app_log("Environment variable \"VAULT\":", ' ');
  app_log(env.vault, '\n', false);

  return 0;
}
