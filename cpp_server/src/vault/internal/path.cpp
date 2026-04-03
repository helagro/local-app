#include "path.hpp"
#include "../config/env_variables.hpp"
#include "constants.hpp"
#include <filesystem>

using namespace std::filesystem;

const path log_path_from_vault =
    path("_") / path("local app") / path("logs.md");

path get_standard_file(STANDARD_FILES file) {
  const path vault_path = path(getenv("VAULT"));

  switch (file) {
  case LOG_FILE:
    return vault_path / log_path_from_vault;
  }
}
