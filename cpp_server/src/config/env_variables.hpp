
struct EnvVariables {
  const char* vault;

  explicit EnvVariables(const char* vault) : vault(vault) {}
};

bool load_env_variables();
EnvVariables* get_env_variables();