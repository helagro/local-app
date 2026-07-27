#include "env_variables.hpp"

#include <cstdlib>
#include <iostream>

#include "../utils/log.hpp"

namespace {

EnvVariables *env;

} // namespace

bool load_env_variables() {
  char *vault = std::getenv("VAULT");
  if (!vault) {
    app_log("Environment variable VAULT is not set.");
    return false;
  }

  char *build_time = std::getenv("BUILD_TIME");
  if (!build_time) {
    build_time = "unknown";
  }

  env = new EnvVariables(vault, build_time);

  return true;
}

EnvVariables *get_env_variables() { return env; }