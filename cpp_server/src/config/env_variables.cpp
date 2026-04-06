#include "env_variables.hpp"

#include <iostream>

#include "../utils/log.hpp"

namespace {

EnvVariables* env;

}  // namespace

bool load_env_variables() {
  char* vault = std::getenv("VAULT");
  if (!vault) {
    app_log("Environment variable VAULT is not set.");
    return false;
  }

  env = new EnvVariables(vault);

  return true;
}

EnvVariables* get_env_variables() { return env; }