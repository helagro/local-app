#pragma once

#include "../constants.hpp"
#include <filesystem>

using namespace std::filesystem;

path get_standard_file(STANDARD_FILES file);
path get_vault_file(std::string relative_path);