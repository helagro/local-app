#include "unsynced_commands.hpp"
#include "api/python_server.hpp"
#include "utils/log.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace {

std::string get_shell_file_name(File shell_file) {
  std::string shell_file_path = shell_file.get_path();

  size_t start_of_name = shell_file_path.find_last_of('/');
  if (start_of_name == std::string::npos) {
    start_of_name = 0;
  } else {
    start_of_name += 1;
  }

  size_t end_of_name = shell_file_path.find_last_of('.');
  if (end_of_name == std::string::npos) {
    end_of_name = shell_file_path.length();
  }

  return std::string(shell_file_path).substr(start_of_name, end_of_name - start_of_name);
}

} // namespace

std::string get_unsynced_file_shell_content(File shell_file) {
  const std::string shell_file_name = get_shell_file_name(shell_file);
  app_log("Shell file name: " + shell_file_name);

  std::string unsynced_changes_str;
  bool changes_req_success = python_server_get("/note-sync/changes", &unsynced_changes_str);

  if (!changes_req_success) {
    app_log("Failed to fetch unsynced changes");
    return shell_file_name;
  }

  json unsynced_changes = json::parse(unsynced_changes_str);
  app_log("Unsynced changes: " + unsynced_changes.dump());

  for (const std::vector<std::string> &change_entry : unsynced_changes) {
    app_log("Unsynced change: " + change_entry.at(1));
  }

  return shell_file_name;
}
