#include "classes/File.hpp"
#include "constants.hpp"
#include <filesystem>
#include <list>

File get_file(STANDARD_FILES std_file);
File get_file(std::string relative_path);
std::list<File> get_files(std::string relative_folder_path);