#include "json_config_handler.hpp"
#include "../utils/log.hpp"
#include "../vault/vault.hpp"
#include "json_config.hpp"
#include <iostream>

#include <nlohmann/json.hpp>
using json = nlohmann::json;

namespace {
JsonConfig config;

std::string extract_config_json(const std::string &s) {
  const size_t markdown_json_start = s.find("{");
  if (markdown_json_start == std::string::npos) {
    return "";
  }

  const size_t markdown_json_end = s.rfind("}");
  if (markdown_json_end == std::string::npos || markdown_json_end == markdown_json_start) {
    return "";
  }

  return s.substr(markdown_json_start, markdown_json_end - markdown_json_start + 1);
}
} // namespace

bool load_config(const bool verbose) {
  const File config_file = get_file(CONFIG_FILE);

  if (verbose) {
    app_log("Config file path:", '"');
    app_log(config_file.get_path(), '"', false);
    app_log("", '\n', false);
  }

  const auto config_read_res = config_file.read();
  if (!config_read_res) {
    app_log("Failed to read config file.");
    return false;
  }

  const std::string content = extract_config_json(config_read_res.value());

  try {
    const json j = json::parse(content);
    config = j.get<JsonConfig>();
  } catch (const json::parse_error &e) {
    app_log("Failed to parse config file as JSON.");
    app_log(e.what());
    return false;
  }

  app_log("Sync rate mins:", ' ');
  app_log(std::to_string(config.sync_rate_mins), '\n', false);

  if (verbose) {
    app_log("Python server URL:", ' ');
    app_log(config.python_server_url, '\n', false);
  }

  return true;
}

JsonConfig get_config() { return config; }

/* ================================== UTILS ================================= */

void from_json(const json &j, JsonConfig &config) {
  j.at("sync_rate_mins").get_to(config.sync_rate_mins);
  j.at("python_server_url").get_to(config.python_server_url);

  j.at("feature_toggle").at("master_switch").get_to(config.feature_toggle.master_switch);
  j.at("feature_toggle").at("scheduled_sync").get_to(config.feature_toggle.scheduled_sync);
  j.at("feature_toggle").at("sync_logs").get_to(config.feature_toggle.sync_logs);
  j.at("feature_toggle").at("file_shell").get_to(config.feature_toggle.file_shell);

  j.at("vault_path").at("file_shell").get_to(config.vault_path.file_shell);
}