cmake_minimum_required(VERSION 3.13)

# Pico SDK Path - kann über Umgebungsvariable gesetzt werden
if(NOT DEFINED ENV{PICO_SDK_PATH})
    set(PICO_SDK_PATH "${CMAKE_CURRENT_LIST_DIR}/pico-sdk")
endif()

# Pico SDK importieren
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(pico_fan_hub C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Pico SDK initialisieren
pico_sdk_init()

# Hauptprojekt
add_executable(pico_fan_hub
    src/main.c
    src/pwm_control.c
    src/tachometer.c
    src/rgb_control.c
    src/usb_hid.c
    src/usb_descriptors.c
)

# Pico-Libraries einbinden
target_link_libraries(pico_fan_hub
    pico_stdlib
    pico_unique_id
    hardware_pwm
    hardware_gpio
    hardware_irq
    hardware_timer
    hardware_pio
    hardware_dma
    tinyusb_device
    tinyusb_board
)

# PIO-Datei für WS2812B
pico_generate_pio_header(pico_fan_hub 
    ${CMAKE_CURRENT_LIST_DIR}/src/ws2812.pio
)

# USB Output aktivieren, UART deaktivieren
pico_enable_stdio_usb(pico_fan_hub 0)
pico_enable_stdio_uart(pico_fan_hub 0)

# UF2-Datei erstellen
pico_add_extra_outputs(pico_fan_hub)

# Include-Verzeichnisse
target_include_directories(pico_fan_hub PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}/include
)

# Compile-Optionen
target_compile_options(pico_fan_hub PRIVATE
    -Wall
    -Wextra
    -Wno-unused-parameter
)

# Build-Informationen
add_compile_definitions(
    PICO_FAN_HUB_VERSION_MAJOR=1
    PICO_FAN_HUB_VERSION_MINOR=0
    PICO_FAN_HUB_VERSION_PATCH=0
)
