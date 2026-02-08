# Pico Fan Hub - Firmware

Firmware für den Raspberry Pi Pico USB Fan Hub.

## Voraussetzungen

### Pico SDK installieren

```bash
# SDK herunterladen
cd ~
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init

# Umgebungsvariable setzen
export PICO_SDK_PATH=~/pico-sdk
```

### Build-Tools installieren

```bash
# Ubuntu/Debian
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib

# macOS
brew install cmake
brew tap ArmMbed/homebrew-formulae
brew install arm-none-eabi-gcc
```

## Build

```bash
cd firmware
mkdir build
cd build

# Pico SDK Pfad setzen (falls nicht in Umgebung)
export PICO_SDK_PATH=~/pico-sdk

# CMake konfigurieren
cmake ..

# Bauen
make -j4
```

Die fertige Firmware befindet sich in `build/pico_fan_hub.uf2`.

## Flashen

1. Halte die BOOTSEL-Taste am Pico gedrückt
2. Schließe den Pico per USB an
3. Der Pico erscheint als USB-Laufwerk "RPI-RP2"
4. Kopiere die `.uf2`-Datei auf das Laufwerk:

```bash
cp pico_fan_hub.uf2 /media/$USER/RPI-RP2/
```

Der Pico startet automatisch neu mit der neuen Firmware.

## Konfiguration

Alle Hardware-Konfigurationen sind in `include/config.h` definiert:

- Anzahl der Lüfter
- GPIO Pin-Zuweisungen
- PWM-Frequenz
- RGB LED-Anzahl
- Watchdog-Einstellungen

## Debugging

### UART-Debug aktivieren

In `include/config.h`:
```c
#define DEBUG_ENABLE 1
```

Debug-Ausgabe auf UART (GPIO 0/1, 115200 Baud).

### LED-Status-Codes

**Onboard-LED (GPIO 25):**
- Langsames Blinken (1 Hz): Normal
- Schnelles Blinken (4 Hz): Fehler
- Dauerhaft an: Initialisierung
- Aus: Keine Stromversorgung

## Architektur

```
main.c
  ├── pwm_control.c      - PWM-Ausgänge für Lüfter
  ├── tachometer.c       - RPM-Messung via GPIO-Interrupts
  ├── rgb_control.c      - RGB LED-Steuerung via PIO
  │   └── ws2812.pio     - WS2812B PIO-Programm
  └── usb_hid.c          - USB HID Kommunikation
      └── usb_descriptors.c
```

## Module

### PWM Control
- 6 PWM-Kanäle @ 25 kHz
- 8-Bit Auflösung (0-255)
- Hardware-PWM des RP2040

### Tachometer
- GPIO-Interrupt-basierte Zählung
- RPM-Berechnung alle 500ms
- Erkennung von gestoppten/fehlenden Lüftern

### RGB Control
- PIO-basierte WS2812B-Ansteuerung
- Bis zu 60 LEDs (konfigurierbar)
- Effekte: Rainbow, Breathing, Static

### USB HID
- Custom HID Device
- Feature Reports für bidirektionale Kommunikation
- Input Reports für asynchrone Status-Updates

## Performance

- CPU-Last: ~5% bei voller Funktion
- USB-Latenz: <10ms
- RPM-Update-Rate: 2 Hz (alle 500ms)
- RGB-Update-Rate: 50 Hz

## Troubleshooting

### Build-Fehler: "pico_sdk not found"
Setze `PICO_SDK_PATH` Umgebungsvariable oder passe `CMakeLists.txt` an.

### USB wird nicht erkannt
1. Prüfe USB-Kabel (Daten, nicht nur Ladung)
2. Prüfe ob Pico-LED blinkt
3. `lsusb` sollte Device 2e8a:1001 zeigen

### Lüfter reagiert nicht
1. Prüfe 12V-Versorgung
2. Prüfe PWM-Signal mit Oszilloskop
3. Teste mit anderem Lüfter
4. Prüfe Level-Shifter (3.3V → 5V)

### Tacho zeigt immer 0 RPM
1. Prüfe Pull-up-Widerstände (10kΩ)
2. Prüfe Tacho-Kabel-Verbindung
3. Teste mit langsam laufendem Lüfter
4. Prüfe GPIO-Interrupt-Konfiguration

### RGB LEDs zeigen falsche Farben
1. Prüfe LED-Typ in config.h (GRB vs RGB)
2. Prüfe Level-Shifter (3.3V → 5V)
3. Prüfe 5V-Versorgung für LEDs
4. Reduziere Helligkeit

## Lizenz

Siehe [../LICENSE](../LICENSE)
