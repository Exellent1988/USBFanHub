# Raspberry Pi Pico USB Fan Hub

Ein USB-basierter Lüfter-Hub mit Raspberry Pi Pico, der 6x 4-Pin PWM-Lüfter steuert und unter Linux hwmon-kompatibel ist.

## Features

- **6x 4-Pin PWM Lüfter-Anschlüsse**
  - PWM-Steuerung (25 kHz Standard)
  - Tachometer-Signal-Auswertung (RPM-Messung)
  - Individuelle Steuerung jedes Lüfters
  
- **RGB LED-Steuerung**
  - Addressierbare RGB LEDs (WS2812B/NeoPixel)
  - Linux-kompatible Standards
  - Programmierbare Effekte

- **Linux hwmon Integration**
  - Standard hwmon Schnittstelle für Systemmonitoring
  - Kompatibel mit lm-sensors und anderen Tools
  - Userspace-Treiber für einfache Integration

- **USB HID Interface**
  - Plug & Play unter Linux
  - Keine Kernel-Module erforderlich
  - Standardisiertes Kommunikationsprotokoll

## Projekt-Struktur

```
├── firmware/           # Raspberry Pi Pico Firmware (C/C++)
│   ├── src/           # Quellcode
│   ├── include/       # Header-Dateien
│   └── CMakeLists.txt # Build-Konfiguration
├── software/          # Linux-Software
│   ├── driver/        # hwmon-kompatibler Treiber
│   └── tools/         # Konfigurations-Tools
├── hardware/          # Hardware-Design-Dokumentation
│   ├── pinout.md      # Pin-Zuweisungen
│   └── schematics/    # Schaltplan-Vorschläge für KiCad
└── docs/              # Zusätzliche Dokumentation
```

## Hardware-Anforderungen

### Raspberry Pi Pico
- RP2040 Mikrocontroller
- USB 2.0 Full Speed
- Ausreichend GPIO-Pins für 6 Lüfter + RGB

### 4-Pin PWM Lüfter
- Pin 1: Ground (GND)
- Pin 2: +12V (Power)
- Pin 3: Tachometer (Tacho) - Open-Collector-Ausgang
- Pin 4: PWM - PWM-Steuerung (25 kHz Standard)

### Zusätzliche Komponenten
- Level-Shifter (3.3V → 5V) für PWM-Signale
- Pull-Up-Widerstände für Tachometer-Eingänge
- Optokoppler oder Schmitt-Trigger für Tachometer-Filterung
- 12V Stromversorgung für Lüfter
- MOSFET oder Logic-Level-Shifter für RGB LEDs

## Quick Start

### Firmware bauen

```bash
cd firmware
mkdir build
cd build
cmake ..
make
```

### Firmware flashen

```bash
# Pico in BOOTSEL-Modus versetzen (BOOTSEL-Taste beim Anschließen gedrückt halten)
# Dann .uf2-Datei auf RPI-RP2 Volume kopieren
cp pico_fan_hub.uf2 /media/$USER/RPI-RP2/
```

### Linux-Software installieren

```bash
cd software/driver
pip install -e .
```

## Verwendung unter Linux

Nach dem Anschließen des Fan Hubs wird er automatisch als hwmon-Device erkannt:

```bash
# Lüfter-Geschwindigkeiten anzeigen
sensors

# Manuell mit sysfs interagieren
cd /sys/class/hwmon/hwmonX/
cat fan1_input  # RPM von Lüfter 1
echo 128 > pwm1 # PWM auf 50% setzen (0-255)
```

## USB HID Protokoll

Details zum USB HID Protokoll siehe [docs/usb_protocol.md](docs/usb_protocol.md)

## RGB Steuerung

Details zur RGB-Steuerung siehe [docs/rgb_control.md](docs/rgb_control.md)

## Lizenz

Siehe [LICENSE](LICENSE)

## Entwicklungsstatus

🚧 Projekt in aktiver Entwicklung
