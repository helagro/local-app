#pragma once

#include "status_template.hpp"

bool write_status();
void to_json(nlohmann::json &j, const Status &status);