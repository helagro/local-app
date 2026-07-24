#include "File.hpp"
#include <fstream>
#include <sstream>
#include <string>

File::File(const path file_path) : file_path(file_path) {}

std::string File::get_path() { return file_path; }

std::optional<std::string> File::read() {
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

const bool File::write(std::string content) const {
  std::ofstream file(file_path);
  if (!file) {
    return false;
  }
  file << content;
  return true;
}