#pragma once

#include "vault/classes/File.hpp"
#include <functional>
#include <string>

void run_unsynced_commands(File shell_file, std::function<void(std::string)> run_command);