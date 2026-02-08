#!/bin/bash
# Build-Script für Pico Fan Hub Firmware

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Pico Fan Hub Firmware Build ===${NC}"
echo ""

# Prüfe ob PICO_SDK_PATH gesetzt ist
if [ -z "$PICO_SDK_PATH" ]; then
    echo -e "${YELLOW}PICO_SDK_PATH nicht gesetzt!${NC}"
    
    # Versuche SDK zu finden
    if [ -d "$HOME/pico/pico-sdk" ]; then
        export PICO_SDK_PATH="$HOME/pico/pico-sdk"
        echo -e "${GREEN}Gefunden: $PICO_SDK_PATH${NC}"
    elif [ -d "$HOME/pico-sdk" ]; then
        export PICO_SDK_PATH="$HOME/pico-sdk"
        echo -e "${GREEN}Gefunden: $PICO_SDK_PATH${NC}"
    else
        echo -e "${RED}Pico SDK nicht gefunden!${NC}"
        echo "Bitte installiere das Pico SDK:"
        echo "  cd ~"
        echo "  git clone https://github.com/raspberrypi/pico-sdk.git"
        echo "  cd pico-sdk"
        echo "  git submodule update --init"
        echo ""
        echo "Oder setze PICO_SDK_PATH:"
        echo "  export PICO_SDK_PATH=/pfad/zum/pico-sdk"
        exit 1
    fi
fi

echo "PICO_SDK_PATH: $PICO_SDK_PATH"
echo ""

# Build-Verzeichnis erstellen
mkdir -p build
cd build

# CMake konfigurieren
echo -e "${GREEN}Konfiguriere CMake...${NC}"
cmake .. || {
    echo -e "${RED}CMake-Konfiguration fehlgeschlagen!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}Baue Firmware...${NC}"

# Bauen mit allen CPU-Kernen
make -j$(nproc) || {
    echo -e "${RED}Build fehlgeschlagen!${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}=== Build erfolgreich! ===${NC}"
echo ""
echo "Firmware: $(pwd)/pico_fan_hub.uf2"
echo ""
echo "Zum Flashen:"
echo "  1. Halte BOOTSEL-Taste am Pico gedrückt"
echo "  2. Schließe Pico per USB an"
echo "  3. Kopiere .uf2-Datei:"
echo "     cp $(pwd)/pico_fan_hub.uf2 /media/$USER/RPI-RP2/"
echo ""
