cmake_minimum_required(VERSION 3.16)

# ESP-IDF top-level project for WifiKiwi firmware.
# Targets ESP32-C5 (RISC-V, dual-band Wi-Fi 6 + BLE 5.3).
# Requires ESP-IDF v5.4 or newer.

set(EXTRA_COMPONENT_DIRS
    "${CMAKE_CURRENT_LIST_DIR}/components"
    "${CMAKE_CURRENT_LIST_DIR}/ui"
)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(wifikiwi)
