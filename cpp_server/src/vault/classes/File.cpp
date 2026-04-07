#include "File.hpp"
#include <fstream>
#include <sstream>
#include <string>

File::File(const path file_path) : file_path(file_path) {}

const char *File::get_path() const { return file_path.c_str(); }

std::optional<std::string> File::read() const {
  std::ifstream file(file_path);
  if (!file) {
    return std::nullopt;
  }

  std::stringstream buffer;
  buffer << file.rdbuf();

  if (file.bad()) {
    return std::nullopt;
  }

  return buffer.str();
}