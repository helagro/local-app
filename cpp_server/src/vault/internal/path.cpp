#include "path.hpp"
#include "../../config/env_variables.hpp"
#include "../constants.hpp"

/* ================================ CONSTANTS =============================== */

const path log_path_from_vault =
    path("_") / path("local app") / path("logs.md");

const path config_path_from_vault =
    path("_") / path("local app") / path("config.md");

const path status_path_from_vault =
    path("_") / path("local app") / path("status.md");

/* ================================ FUNCTIONS =============================== */

path get_standard_file(STANDARD_FILES file) {
  const path vault_path = path(getenv("VAULT"));

  switch (file) {
  case LOG_FILE:
    return vault_path / log_path_from_vault;
  case CONFIG_FILE:
    return vault_path / config_path_from_vault;
  case STATUS_FILE:
    return vault_path / status_path_from_vault;
  default:
    throw std::invalid_argument("Invalid STANDARD_FILES value");
  }
}
