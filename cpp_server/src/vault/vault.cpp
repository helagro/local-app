#include "classes/File.hpp"
#include "constants.hpp"
#include "internal/path.hpp"
#include <filesystem>
#include <list>

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

File get_file(std::string relative_path) {
  const path file_path = get_vault_file(relative_path);

  return get_file(file_path);
}

std::list<File> get_files(std::string relative_folder_path, bool recursive) {
  const path file_path = get_vault_file(relative_folder_path);

  std::filesystem::directory_iterator iterator(file_path);
  std::list<File> files;

  for (const auto &entry : iterator) {
    if (entry.is_directory() && recursive) {
      const std::string sub_folder_path = entry.path().string();
      const std::list<File> sub_folder_files = get_files(sub_folder_path, recursive);
      files.insert(files.end(), sub_folder_files.begin(), sub_folder_files.end());
    }

    if (!entry.is_regular_file()) {
      continue;
    }

    const path file_path = entry.path();
    files.push_back(File(file_path));
  }

  return files;
}
