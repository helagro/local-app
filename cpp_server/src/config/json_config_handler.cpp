#include "json_config_handler.hpp"
#include "../utils/log.hpp"
#include "../vault/vault.hpp"
#include "json_config.hpp"

#include <nlohmann/json.hpp>
using json = nlohmann::json;

namespace {
JsonConfig config;

// TODO - Handle edge cases
std::string extract_config_json(const std::string &s) {
  const size_t first = s.find('\n');
  if (first == std::string::npos) {
    return "";
  }

  const size_t last = s.rfind('\n');
  const size_t second_last = s.rfind('\n', last - 1);
  if (second_last == first) {
    return "";
  }

  return s.substr(first + 1, second_last - first - 1);
}
} // namespace

bool load_config() {
  const File config_file = get_file(CONFIG_FILE);

  app_log("Config file path:", ' ');
  app_log(config_file.get_path(), '\n', false);

  const auto config_read_res = config_file.read();
  if (!config_read_res) {
    app_log("Failed to read config file.");
    return false;
  }

  const std::string content = extract_config_json(config_read_res.value());
  const json j = json::parse(content);
  config = j.get<JsonConfig>();

  app_log("Sync rate mins:", ' ');
  app_log(std::to_string(config.sync_rate_mins).c_str(), '\n', false);

  return true;
}

void from_json(const json &j, JsonConfig &config) {
  j.at("sync_rate_mins").get_to(config.sync_rate_mins);
}