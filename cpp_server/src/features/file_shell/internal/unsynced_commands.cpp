#include "unsynced_commands.hpp"
#include "api/python_server/python_server.hpp"
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

void run_unsynced_commands(File shell_file, std::function<void(std::string)> run_command) {
  const std::string shell_file_name = get_shell_file_name(shell_file);
  const std::string shell_file_hashtag = "#" + shell_file_name;

  std::string unsynced_changes_str;
  bool changes_req_success = python_server_get("/note-sync/changes", &unsynced_changes_str);

  if (!changes_req_success) {
    app_log("Failed to fetch unsynced changes");
    return;
  }

  json unsynced_changes = json::parse(unsynced_changes_str);

  for (const std::vector<std::string> &change_entry : unsynced_changes) {
    if (change_entry.size() <= 2) {
      app_log("Invalid unsynced change entry: " + json(change_entry).dump());
      continue;
    }

    const std::string id = change_entry.at(0);
    std::string change_content = change_entry.at(1);

    if (change_content.find(shell_file_hashtag) != std::string::npos) {
      change_content.erase(change_content.find(shell_file_hashtag), shell_file_hashtag.length());

      app_log("Unsynced change: " + change_content);

      run_command(change_content);
      python_server_socket(id);
    }
  }
}
