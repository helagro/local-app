#pragma once
#include <string>

struct JsonConfig {
  struct FeatureToggle {
    bool master_switch;

    bool scheduled_sync;
    bool sync_logs;
    bool file_shell;
  };

  struct VaultPath {
    std::string file_shell;
  };

  unsigned int sync_rate_mins;
  std::string python_server_url;
  FeatureToggle feature_toggle;
  VaultPath vault_path;
};