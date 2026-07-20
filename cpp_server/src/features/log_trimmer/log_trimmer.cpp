
#include "log_trimmer.hpp"
#include "../../config/json_config_handler.hpp"
#include "../../utils/log.hpp"
#include "../../vault/classes/File.hpp"
#include "../../vault/vault.hpp"

void trim_logs() {
  app_log("Trimming logs...");

  const JsonConfig config = get_config();
  const std::string logs_path = config.vault_path.trimmable_logs;

  const unsigned int trim_from = config.trim_option.trim_from;
  const unsigned int trim_to = config.trim_option.trim_to;

  std::list<File> files = get_files(logs_path);

  for (const File &file : files) {
    const std::optional<std::string> read_result = file.read();

    if (!read_result.has_value()) {
      app_log("Failed to read file: " + std::string(file.get_path()));
      continue;
    }

    const std::string content = read_result.value();
    unsigned long line_count = 0;
    unsigned long trim_to_index;

    for (long i = content.size() - 1; i >= 0; i--) {
      if (content[i] == '\n') {
        line_count++;
      }

      if (line_count == trim_to) {
        trim_to_index = i;
      }
    }

    if (line_count >= trim_from) {
      const std::string trimmed_content = content.substr(trim_to_index + 1);
      const bool write_success = file.write(trimmed_content);

      if (write_success) {
        app_log("Trimmed content for file: " + std::string(file.get_path()) + " with " + std::to_string(line_count) + " lines");
      } else {
        app_log("Failed to write file: " + std::string(file.get_path()));
      }
    }
  }
}