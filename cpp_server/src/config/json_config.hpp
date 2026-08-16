#pragma once
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
  };

  struct VaultPath {
    std::string file_shell;
    std::string trimmable_logs;
    std::string sortable_notes;
    std::string scheduled_commands;
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