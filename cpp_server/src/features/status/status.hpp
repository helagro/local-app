#pragma once

#include "status_template.hpp"

bool write_status();
void from_json(const nlohmann::json &j, Status &status);
void to_json(nlohmann::json &j, const Status &status);