# CMakeLists.txt
# Artefact: Le Système de Build.
# Doctrine: Le processus de compilation du Corps Natif doit être simple,
# déclaratif et reproductible. Ce manifeste CMake décrit comment forger
# les fichiers source C en une bibliothèque partagée, l'artefact final
# que l'Esprit Python pourra charger.

cmake_minimum_required(VERSION 3.10)

project(sentire_core C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_library(sentire_core SHARED
    sentire_core.c
    resilience_core.c
    statemachine.c
    journal.c
)

# Sur Linux/macOS, cela créera libsentire_core.so/.dylib
# Sur Windows, cela créera sentire_core.dll