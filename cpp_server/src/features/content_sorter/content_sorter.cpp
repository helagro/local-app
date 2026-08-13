#include "content_sorter.hpp"
#include "config/json_config_handler.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

#define PREFIX_LENGTH 6 // Length of "- [ ] "

namespace {
enum class Priority { High, Medium, Low, Invalid };

struct InboxItem {
  std::string line;
  Priority priority;
};

bool get_destinations(size_t &high_end, size_t &medium_end, size_t &low_end, std::string &note_str) {
  const size_t high_start = note_str.find("## High\n");
  if (high_start == std::string::npos) {
    return false;
  }
  high_end = high_start + 8; // Length of "## High\n"

  const size_t medium_start = note_str.find("## Mid\n", high_end);
  const bool medium_found = (medium_start != std::string::npos);

  const size_t low_start = note_str.find("## Low\n", medium_found ? medium_start : high_end);
  if (low_start == std::string::npos) {
    return false;
  }
  low_end = low_start + 7; // Length of "## Low\n"

  if (medium_found) {
    medium_end = medium_start + 7; // Length of "## Mid\n"
  } else {
    medium_end = low_end;
  }

  return true;
}

Priority get_priority(const std::string &item) {
  if (item.substr(PREFIX_LENGTH, 2) == "**") {
    return Priority::High;
  } else if (item.substr(PREFIX_LENGTH, 1) == "*") {
    return Priority::Low;
  } else if (item.substr(PREFIX_LENGTH, 1) == "=") {
    return Priority::Medium;
  } else {
    return Priority::Invalid;
  }
}

bool get_inbox(std::string &note_str, std::list<InboxItem> &items) {
  const size_t inbox_start = note_str.find("## In\n");
  if (inbox_start == std::string::npos) {
    return false;
  }

  size_t command_line_start = inbox_start;

  while (true) {
    command_line_start = note_str.find("- [ ] ", command_line_start);
    if (command_line_start == std::string::npos) {
      return items.size() > 0;
    }

    const size_t command_line_end = note_str.find('\n', command_line_start);

    // If note does not end with newline
    if (command_line_end == std::string::npos) {
      return false;
    }

    const std::string line = note_str.substr(command_line_start, command_line_end - command_line_start);
    const Priority priority = get_priority(line);

    if (priority == Priority::Invalid) {
      command_line_start = command_line_end + 1;
    } else {
      items.push_back({line, priority});
      note_str.erase(command_line_start, command_line_end - command_line_start + 1);
    }
  }

  return false;
}

// TODO - Improve performance by calculating updated positions
void sort_note(File note) {
  const std::optional<std::string> note_content = note.read();

  if (!note_content.has_value()) {
    return;
  }
  std::string note_str = note_content.value();

  std::list<InboxItem> inbox;
  if (!get_inbox(note_str, inbox)) {
    return;
  }

  for (const InboxItem &item : inbox) {
    app_log("Sorting line: \"" + item.line + "\" in note: \"" + note.get_path() + "\"");

    size_t high_end, medium_end, low_end;
    if (!get_destinations(high_end, medium_end, low_end, note_str)) {
      return;
    }

    std::string item_tmp;
    std::remove_copy(item.line.begin(), item.line.end(), std::back_inserter(item_tmp), '*');
    std::string item_tmp2;
    std::remove_copy(item_tmp.begin(), item_tmp.end(), std::back_inserter(item_tmp2), '=');

    switch (item.priority) {
    case Priority::High:
      note_str.insert(high_end, item_tmp2 + "\n");
      break;
    case Priority::Medium:
      note_str.insert(medium_end, item_tmp2 + "\n");
      break;
    case Priority::Low:
      note_str.insert(low_end, item_tmp2 + "\n");
      break;
    case Priority::Invalid:
      app_log("Invalid priority for line: \"" + item.line + "\" in note: \"" + note.get_path() + "\"");
      return;
    }
  }

  note.write(note_str);
}
} // namespace

void sort_content() {
  const JsonConfig config = get_config();

  try {
    std::list<File> notes = get_files(config.vault_path.sortable_notes, true);
    for (File &note : notes) {
      sort_note(note);
    }
  } catch (const std::exception &e) {
    app_log("Failed to sort content.");
    app_log(e.what());
  }
}
