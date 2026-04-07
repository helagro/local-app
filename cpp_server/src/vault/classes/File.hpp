#pragma once

#include <filesystem>

using namespace std::filesystem;

class File {
public:
  File(const path file_path);

  const char *get_path() const;

  std::optional<std::string> read() const;

private:
  path file_path;
};