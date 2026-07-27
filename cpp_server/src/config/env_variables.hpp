
struct EnvVariables {
  const char *vault;
  const char *build_time;

  explicit EnvVariables(const char *vault, const char *build_time) : vault(vault), build_time(build_time) {}
};

bool load_env_variables();
EnvVariables *get_env_variables();