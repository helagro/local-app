# ============================ PROJECT SETTINGS ============================ #

cmake_minimum_required(VERSION 3.10)
project(cpp_server)

# ============================== CPP STANDARD ============================== #

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ================================== SET FLAGS ================================= #


if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")
endif()

# =============================== ADD EXECUTABLES ============================== #

file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE HEADERS "src/*.hpp")

add_executable(main)

target_sources(main PRIVATE ${SOURCES} ${HEADERS})
target_include_directories(main PRIVATE include)