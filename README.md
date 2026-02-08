# Raspberry Pi Pico USB Fan Hub

[![CI](https://github.com/Exellent1988/USBFanHub/actions/workflows/ci.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/ci.yml)
[![Firmware Build](https://github.com/Exellent1988/USBFanHub/actions/workflows/firmware-build.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/firmware-build.yml)
[![Python Tests](https://github.com/Exellent1988/USBFanHub/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/python-tests.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Exellent1988/USBFanHub)](https://github.com/Exellent1988/USBFanHub/releases)

A USB-based fan hub using Raspberry Pi Pico that controls 6x 4-pin PWM fans and is hwmon-compatible under Linux.

## Features

- **6x 4-Pin PWM Fan Connectors**
  - PWM control (25 kHz standard)
  - Tachometer signal evaluation (RPM measurement)
  - Individual control of each fan
  
- **RGB LED Control**
  - Addressable RGB LEDs (WS2812B/NeoPixel)
  - Linux-compatible standards
  - Programmable effects

- **Linux hwmon Integration**
  - Standard hwmon interface for system monitoring
  - Compatible with lm-sensors and other tools
  - Userspace driver for easy integration

- **USB HID Interface**
  - Plug & Play under Linux
  - No kernel modules required
  - Standardized communication protocol

## Project Structure

```
├── firmware/           # Raspberry Pi Pico Firmware (C/C++)
│   ├── src/           # Source code
│   ├── include/       # Header files
│   └── CMakeLists.txt # Build configuration
├── software/          # Linux software
│   ├── driver/        # hwmon-compatible driver
│   └── tools/         # Configuration tools
├── hardware/          # Hardware design documentation
│   ├── pinout.md      # Pin assignments
│   └── schematics/    # Schematic suggestions for KiCad
└── docs/              # Additional documentation
```

## Hardware Requirements

### Raspberry Pi Pico
- RP2040 microcontroller
- USB 2.0 Full Speed
- Sufficient GPIO pins for 6 fans + RGB

### 4-Pin PWM Fans
- Pin 1: Ground (GND)
- Pin 2: +12V (Power)
- Pin 3: Tachometer (Tacho) - Open-collector output
- Pin 4: PWM - PWM control (25 kHz standard)

### Additional Components
- Level shifter (3.3V → 5V) for PWM signals
- Pull-up resistors for tachometer inputs
- Optocoupler or Schmitt trigger for tachometer filtering
- 12V power supply for fans
- MOSFET or logic-level shifter for RGB LEDs

## CI/CD & Releases

### Automatic Building

This project uses GitHub Actions for automatic building and testing:

- **Firmware Build**: Every push to `main`, `develop`, or `cursor/**` branch automatically builds the firmware
- **Python Tests**: Automatic tests for Python 3.8, 3.9, 3.10, 3.11
- **Releases**: Automatic release creation on Git tags (`v*.*.*`)

### Download Artifacts

After every successful build:
1. Go to [Actions](https://github.com/Exellent1988/USBFanHub/actions)
2. Select a successful workflow run
3. Download artifacts:
   - `pico-fan-hub-firmware-vX.X.X` - Firmware binaries
   - `python-packages` - Python wheel & source distribution

### Create Release

Automatically with tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

Manually via GitHub Actions:
1. Go to Actions → Release
2. "Run workflow" → Enter version
3. Release will be created automatically

## Quick Start

### Build Firmware

```bash
cd firmware
mkdir build
cd build
cmake ..
make
```

### Flash Firmware

```bash
# Put Pico in BOOTSEL mode (hold BOOTSEL button while connecting USB)
# Then copy .uf2 file to RPI-RP2 volume
cp pico_fan_hub.uf2 /media/$USER/RPI-RP2/
```

### Install Linux Software

```bash
cd software/driver
pip install -e .
```

## Usage under Linux

After connecting the fan hub, it will automatically be recognized as an hwmon device:

```bash
# Show fan speeds
sensors

# Manually interact with sysfs
cd /sys/class/hwmon/hwmonX/
cat fan1_input  # RPM of fan 1
echo 128 > pwm1 # Set PWM to 50% (0-255)
```

## USB HID Protocol

For details on the USB HID protocol, see [docs/usb_protocol.md](docs/usb_protocol.md)

## RGB Control

For details on RGB control, see [docs/rgb_control.md](docs/rgb_control.md)

## License

See [LICENSE](LICENSE)

## Development Status

🚧 Project in active development
