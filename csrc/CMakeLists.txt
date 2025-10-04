# --- START OF FILE: csrc/CMakeLists.txt ---
cmake_minimum_required(VERSION 3.15)
project(sentire_core C)

# Définir le standard C
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Ajout de la définition pour l'exportation des symboles sur Windows
add_definitions(-DSENTIRE_CORE_EXPORTS)

# Création de la librairie partagée (DLL)
add_library(sentire_core SHARED
    statemachine.c
    journal.c
)

# Assurer que les en-têtes sont trouvables
target_include_directories(sentire_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Spécifier le nom de sortie et le répertoire
set_target_properties(sentire_core PROPERTIES
    OUTPUT_NAME "sentire_core"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)

# Pour les builds multi-configuration (comme Visual Studio),
# spécifier le répertoire de sortie pour chaque configuration.
foreach(config ${CMAKE_CONFIGURATION_TYPES})
    string(TOUPPER ${config} config_upper)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${config_upper} "${CMAKE_BINARY_DIR}/${config}")
endforeach()
# --- END OF FILE: csrc/CMakeLists.txt ---