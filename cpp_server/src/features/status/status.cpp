#include "../../vault/classes/File.hpp"
#include "../../vault/constants.hpp"
#include "../../vault/vault.hpp"
#include "status_template.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace {} // namespace

std::string get_status_json() {
  Status status;
  status.message = "OK";

  nlohmann::json j = status;
  return j.dump();
}

bool write_status() {
  const File status_file(get_file(STATUS_FILE));

  const std::string status_json = get_status_json();

  return status_file.write("```json\n" + status_json + "\n```");
}

void from_json(const json &j, Status &status) {
  j.at("message").get_to(status.message);
}

void to_json(json &j, const Status &status) {
  j = json{{"message", status.message}};
}