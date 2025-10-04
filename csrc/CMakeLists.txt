# Sentire Guardian V9 - Native Core Build System
# Rituel de la Forge
#
# Épigraphe Doctrinale:
# Le Rituel de la Forge compile le Corps natif (C) du Vaisseau Guardian V9.
# Bibliothèque partagée (.so/.dll) pour l'interface FFI Python.

cmake_minimum_required(VERSION 3.10)
project(SentireCore C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Options de compilation
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -O2")

# Sources du cœur natif
set(SENTIRE_SOURCES
    sentire_core.c
    resilience_core.c
    statemachine.c
    journal.c
    oracle_integration.c
)

# Bibliothèque partagée pour FFI Python
add_library(sentire_core SHARED ${SENTIRE_SOURCES})

# Installation
install(TARGETS sentire_core
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin)

install(FILES sentire_core.h
        DESTINATION include)

# Tests (optionnel)
option(BUILD_TESTS "Build native tests" OFF)

if(BUILD_TESTS)
    enable_testing()
    add_executable(test_sentire_core test_sentire_core.c)
    target_link_libraries(test_sentire_core sentire_core)
    add_test(NAME test_sentire_core COMMAND test_sentire_core)
endif()

# Affichage de la configuration
message(STATUS "Sentire Core - Native Build Configuration")
message(STATUS "  C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "  C Flags: ${CMAKE_C_FLAGS}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Install Prefix: ${CMAKE_INSTALL_PREFIX}")
