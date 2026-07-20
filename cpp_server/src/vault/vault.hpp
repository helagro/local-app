#include "classes/File.hpp"
#include "constants.hpp"
#include <filesystem>

File get_file(STANDARD_FILES std_file);
File get_file(std::string relative_path);