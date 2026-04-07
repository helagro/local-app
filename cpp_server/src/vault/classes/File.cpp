#include "File.hpp"
#include <fstream>
#include <sstream>
#include <string>

File::File(const path file_path) : file_path(file_path) {}

const char *File::get_path() const { return file_path.c_str(); }

std::string File::read() const {
  std::ifstream file(file_path);
  std::stringstream buffer;

  buffer << file.rdbuf();
  return buffer.str();
}