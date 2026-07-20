#include "../../vault/classes/File.hpp"
#include "../../vault/constants.hpp"
#include "../../vault/vault.hpp"
#include "status_template.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace {} // namespace

/* json conversions --------------------------------------------------------- */

void from_json(const json &j, Status &status) {
  j.at("message").get_to(status.message);
  j.at("timestamp").get_to(status.timestamp);
}

void to_json(json &j, const Status &status) {
  j = json{{"message", status.message}, {"timestamp", status.timestamp}};
}

/* general functions -------------------------------------------------------- */

std::string get_status_json(const int indent = -1) {
  Status status;
  status.message = "OK";

  // Add timestamp
  std::time_t t = std::time(nullptr);
  std::tm *tm_ptr = std::localtime(&t);
  char buffer[50];
  std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", tm_ptr);
  status.timestamp = std::string(buffer);

  nlohmann::json j = status;
  return j.dump(indent);
}

bool write_status() {
  const File status_file(get_file(STATUS_FILE));

  const std::string status_json = get_status_json(1);

  return status_file.write("```json\n" + status_json + "\n```");
}
