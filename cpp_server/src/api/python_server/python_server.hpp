#pragma once

#include <string>

bool python_server_get(std::string path, std::string *response);
bool python_server_socket(std::string message);