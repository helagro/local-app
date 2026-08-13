#include "content_sorter.hpp"
#include "config/json_config_handler.hpp"
#include "utils/log.hpp"
#include "vault/classes/File.hpp"
#include "vault/vault.hpp"
#include <algorithm>

#define PREFIX_LENGTH 6 // Length of "- [ ] "

namespace {

std::string sort_label;

enum class Priority { High, Medium, Low };

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

bool get_inbox(const std::string &note_str, std::list<std::string> &items) {
  const size_t inbox_start = note_str.find("## In\n");
  if (inbox_start == std::string::npos) {
    return false;
  }

  size_t command_line_end = inbox_start;

  while (true) {
    const size_t command_line_start = note_str.find("- [ ] ", command_line_end);
    if (command_line_start == std::string::npos) {
      return false;
    }

    const size_t command_start = command_line_start;
    command_line_end = note_str.find('\n', command_start);

    // If note does not end with newline
    if (command_line_end == std::string::npos) {
      return false;
    }

    const std::string line = note_str.substr(command_start, command_line_end - command_start);

    // If line is the end label
    if (line.substr(PREFIX_LENGTH, sort_label.length()) == sort_label) {
      return true;
    }

    items.push_back(line);
  }

  return false;
}

Priority get_priority(const std::string &item) {
  if (item.substr(PREFIX_LENGTH, 2) == "**") {
    return Priority::High;
  } else if (item.substr(PREFIX_LENGTH, 1) == "*") {
    return Priority::Low;
  } else {
    return Priority::Medium;
  }
}

bool get_inbox_range(const std::string &note_str, size_t &inbox_start, size_t &inbox_end) {
  const size_t inbox_label_start = note_str.find("## In\n");

  if (inbox_label_start == std::string::npos) {
    return false;
  }
  inbox_start = inbox_label_start + 6; // Length of "## In\n"

  inbox_end = note_str.find(sort_label, inbox_start) - PREFIX_LENGTH;
  if (inbox_end == std::string::npos) {
    return false;
  }

  return true;
}

// TODO - Improve performance by calculating updated positions
void sort_note(File note) {
  const std::optional<std::string> note_content = note.read();

  if (!note_content.has_value()) {
    return;
  }
  std::string note_str = note_content.value();

  std::list<std::string> inbox;
  if (!get_inbox(note_str, inbox)) {
    return;
  }

  for (std::string &item : inbox) {
    app_log("Sorting line: \"" + item + "\" in note: \"" + note.get_path() + "\"");
    const Priority priority = get_priority(item);

    size_t high_end, medium_end, low_end;
    if (!get_destinations(high_end, medium_end, low_end, note_str)) {
      return;
    }

    std::string processed_item;
    std::remove_copy(item.begin(), item.end(), std::back_inserter(processed_item), '*');

    switch (priority) {
    case Priority::High:
      note_str.insert(high_end, processed_item + "\n");
      break;
    case Priority::Medium:
      note_str.insert(medium_end, processed_item + "\n");
      break;
    case Priority::Low:
      note_str.insert(low_end, processed_item + "\n");
      break;
    }
  }

  size_t inbox_start, inbox_end;
  if (get_inbox_range(note_str, inbox_start, inbox_end)) {
    note_str.erase(inbox_start, inbox_end - inbox_start);
    note.write(note_str);
  }
}
} // namespace

void sort_content() {
  const JsonConfig config = get_config();
  sort_label = config.content_sorter_label;

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
