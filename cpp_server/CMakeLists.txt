# ============================ PROJECT SETTINGS ============================ #

cmake_minimum_required(VERSION 3.10)
project(cpp_server)

# ================================== FLAGS ================================= #


if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")
endif()

# =============================== EXECUTABLES ============================== #

file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE HEADERS "src/*.hpp")

add_executable(main)

target_sources(main PRIVATE ${SOURCES} ${HEADERS})
target_include_directories(main PRIVATE include)