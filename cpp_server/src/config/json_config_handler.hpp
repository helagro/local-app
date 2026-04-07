#pragma once

#include "json_config.hpp"
#include <nlohmann/json.hpp>

void from_json(const nlohmann::json &j, JsonConfig &config);
bool load_config();
