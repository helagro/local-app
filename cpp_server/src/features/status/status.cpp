#include "../../api/python_server.hpp"
#include "../../config/json_config_handler.hpp"
#include "../../vault/classes/File.hpp"
#include "../../vault/constants.hpp"
#include "../../vault/vault.hpp"
#include "status_template.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace {
bool is_first_status = true;
std::string first_timestamp;

void get_timestamp(std::string *timestamp) {
  std::time_t t = std::time(nullptr);
  std::tm *tm_ptr = std::localtime(&t);
  char buffer[50];
  std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm_ptr);
  *timestamp = std::string(buffer);
}
} // namespace

/* json conversions --------------------------------------------------------- */

void to_json(json &j, const Status &status) {
  j = json{{"message", status.message},
           {"timestamp", status.timestamp},
           {"first_timestamp", status.first_timestamp},
           {"sync_logs", status.sync_logs},
           {"python_server_health", status.python_server_health}};
}

/* general functions -------------------------------------------------------- */

std::string get_status_json(const int indent = -1) {
  if (is_first_status) {
    get_timestamp(&first_timestamp);
    is_first_status = false;
  }

  Status status;
  status.message = "OK";
  status.first_timestamp = first_timestamp;
  get_timestamp(&status.timestamp);

  // Add python server health
  python_server_get("/health", &status.python_server_health);

  status.sync_logs = get_config().feature_toggle.sync_logs;

  nlohmann::json j = status;
  return j.dump(indent);
}

bool write_status() {
  const File status_file(get_file(STATUS_FILE));

  const std::string status_json = get_status_json(1);

  return status_file.write("```json\n" + status_json + "\n```");
}
