#include "content_filter.hpp"
#include "config/json_config_handler.hpp"
#include "utils/log.hpp"
#include "vault/vault.hpp"
#include <algorithm>
#include <list>
#include <string>

namespace {

size_t count_lines(const std::string &content) {
  size_t line_count = 0;

  size_t line_pos = content.find("\n- [ ] ");
  while (line_pos != std::string::npos) {
    line_count++;
    line_pos = content.find("\n- [ ] ", line_pos + 7);
  }

  return line_count;
}

void filter_file(File &file) {
  app_log("Filtering content in file:", ' ');
  app_log(file.get_path(), '\n', false);

  const std::optional<std::string> file_read_res = file.read();
  if (!file_read_res) {
    app_log("Failed to read file " + file.get_path() + ".");
    return;
  }
  std::string content = file_read_res.value();
  const size_t content_line_count = count_lines(content);
  bool content_changed = false;

  size_t tag = content.find("^max_");
  while (tag != std::string::npos) {
    const size_t tag_end = content.find(" ", tag);
    const std::string tag_str = content.substr(tag, tag_end - tag);
    const unsigned int max_requirement = std::stoi(tag_str.substr(5));

    if (content_line_count > max_requirement) {
      const size_t line_start = content.rfind("\n", tag);
      const size_t line_end = content.find("\n", tag);

      app_log("Removing line: \"" + content.substr(line_start + 1, line_end - line_start - 1) + "\" from " + file.get_path() + " as " +
              std::to_string(max_requirement) + " > " + std::to_string(content_line_count));

      if (line_start != std::string::npos && line_end != std::string::npos) {
        content.erase(line_start + 1, line_end - line_start);
        content_changed = true;
      } else {
        app_log("Failed to filter " + file.get_path() + " due to invalid line positions.");
      }
    }

    tag = content.find("^max_", tag + 1);
  }

  if (content_changed) {
    if (!file.write(content)) {
      app_log("Failed to write filtered content to " + file.get_path() + ".");
    }
  }
}
} // namespace

void filter_content() {
  const JsonConfig config = get_config();

  try {
    for (const std::string &file_path : config.vault_path.filtered_notes) {
      File file = get_file(file_path);
      filter_file(file);
    }
  } catch (const std::exception &e) {
    app_log("Error filtering content:", ' ');
    app_log(e.what(), '\n', false);
  }
}
