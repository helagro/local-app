#pragma once

#include "vault/classes/File.hpp"
#include <functional>

void run_synced_commands(const File shell_file, std::function<void(const std::string &)> run_command);