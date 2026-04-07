#include "classes/File.hpp"
#include "constants.hpp"
#include "internal/path.hpp"
#include <filesystem>

/* =============================== NAMESPACES =============================== */

using namespace std::filesystem;

namespace {
File get_file(path file_path) { return File(file_path); }
} // namespace

/* ================================ FUNCTIONS =============================== */

File get_file(STANDARD_FILES std_file) {
  const path file_path = get_standard_file(std_file);

  return get_file(file_path);
}
