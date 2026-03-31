# ============================ PROJECT SETTINGS ============================ #

cmake_minimum_required(VERSION 3.10)
project(main)

# ================================== FLAGS ================================= #

set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")

# =============================== EXECUTABLES ============================== #

add_executable(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.cpp )