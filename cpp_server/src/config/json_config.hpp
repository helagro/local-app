#pragma once
#include <list>
#include <string>

struct JsonConfig {
  struct FeatureToggle {
    bool master_switch;

    bool scheduled_sync;
    bool sync_logs;
    bool file_shell;
    bool log_trimmer;
    bool content_sorter;
    bool scheduled_commands;
    bool content_filter;
  };

  struct VaultPath {
    std::string trimmable_logs;
    std::string sortable_notes;
    std::string scheduled_commands;
    std::list<std::string> filtered_notes;

    std::string file_shell;
    std::string file_shell_output;
  };

  struct TrimOption {
    unsigned int trim_from;
    unsigned int trim_to;
    unsigned int trim_frequency;
  };

  unsigned int sync_rate_mins;
  std::string python_server_url;

  FeatureToggle feature_toggle;
  VaultPath vault_path;
  TrimOption trim_option;
};