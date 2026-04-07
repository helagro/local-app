# ============================ PROJECT SETTINGS ============================ #

cmake_minimum_required(VERSION 3.11)
cmake_policy(SET CMP0135 NEW)
project(cpp_server)

# ============================== CPP STANDARD ============================== #

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ================================== SET FLAGS ================================= #


if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")
endif()

# =============================== ADD LIBRARIES ============================== #

include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz)
FetchContent_MakeAvailable(json)

# ============================= ADD EXECUTABLE ============================= #

file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE HEADERS "src/*.hpp")

add_executable(main)

target_sources(main PRIVATE ${SOURCES} ${HEADERS})
target_include_directories(main PRIVATE include)

target_link_libraries(main PRIVATE nlohmann_json::nlohmann_json)