# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Pico firmware with complete functionality:
  - 6x PWM outputs (25 kHz) for fan control
  - 6x Tachometer inputs for RPM measurement
  - RGB LED control via WS2812B/NeoPixel (PIO-based)
  - USB HID interface for communication
  - Watchdog for safety
- Linux software:
  - Python-based USB HID driver
  - hwmon-compatible sysfs bridge
  - CLI tool for direct control
  - Daemon for hwmon integration
- Comprehensive documentation:
  - Hardware pinout and circuit suggestions
  - USB HID protocol specification
  - RGB control documentation
  - Build and installation guides
  - KiCad schematic suggestions
- Build automation:
  - CMake build system for firmware
  - Python setuptools for software
  - Build script with error handling
- Git infrastructure:
  - .gitignore for all artifacts
  - CONTRIBUTING.md for developers
  - This CHANGELOG

## [1.0.0] - TBD

First official release (planned after hardware testing)

### Planned
- Hardware testing with real fans
- Performance optimizations
- Extended error handling
- Additional RGB effects
- OpenRGB integration
- liquidctl compatibility

## Roadmap

### v1.1.0 (planned)
- [ ] Temperature sensor support (I2C)
- [ ] OLED display for status
- [ ] Advanced fan curves (PID controller)
- [ ] Configuration storage in flash
- [ ] Web interface for configuration

### v1.2.0 (planned)
- [ ] Support for more than 6 fans
- [ ] Multiple RGB channels
- [ ] Audio-reactive RGB modes
- [ ] Extended monitoring (voltage, current)

### v2.0.0 (future)
- [ ] Wireless control (Bluetooth/WiFi)
- [ ] Mobile app (Android/iOS)
- [ ] Cloud integration for remote monitoring
- [ ] Machine learning for automatic fan curves

---

## Format Legend

- `Added` for new features
- `Changed` for changes to existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for removed features
- `Fixed` for bugfixes
- `Security` for security updates
