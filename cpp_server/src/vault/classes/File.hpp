#pragma once

#include <filesystem>
#include <optional>

using namespace std::filesystem;

class File {
public:
  File(const path file_path);

  const char *get_path() const;

  std::optional<std::string> read() const;
  bool write(std::string content) const;

private:
  path file_path;
};