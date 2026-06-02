#pragma once

#include "json_config.hpp"
#include <nlohmann/json.hpp>

JsonConfig get_config();
bool load_config();

void from_json(const nlohmann::json &j, JsonConfig &config);