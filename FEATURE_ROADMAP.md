# Feature Roadmap - Pico Fan Hub

Overview of planned features and enhancements. See GitHub Issues for detailed discussions.

## Core Features (v1.0) ✅ COMPLETED

- [x] 6x 4-Pin PWM fan control (25 kHz)
- [x] Tachometer RPM measurement
- [x] RGB LED control (WS2812B)
- [x] USB HID interface
- [x] Linux hwmon integration
- [x] CLI tool
- [x] Comprehensive documentation
- [x] CI/CD pipeline
- [x] Unit tests

## High Priority Features

### Temperature & Automation
- [ ] **Temperature sensor integration** (#7)
  - I2C sensors (BME280, Si7021, LM75)
  - Multiple sensor zones
  - hwmon exposure
  
- [ ] **Standalone mode** (#8)
  - Autonomous fan control based on temperature
  - No host software required
  - Flash-stored configurations
  
- [ ] **Configurable startup behavior** (#10)
  - Safe mode / Last state / Custom profile
  - Restore settings after power loss

### Safety & Monitoring
- [ ] **Fan failure detection** (#13)
  - Stall detection
  - Alerts and notifications
  - Automatic compensation

## Medium Priority Features

### User Interface
- [ ] **GUI/TUI configuration tool** (#9)
  - Visual fan curve editor
  - Real-time monitoring
  - RGB color picker
  - Profile management

- [ ] **OLED/LCD display** (#11)
  - Status display
  - Local configuration
  - Visual feedback

### Fan Curves & Profiles
- [ ] **Fan curve profiles** (#16)
  - Silent / Balanced / Performance
  - Custom profiles
  - Import/export
  
- [ ] **Pump control support** (#20)
  - Water cooling compatibility
  - Flow rate monitoring
  - Coolant temperature integration

### Integration
- [ ] **OpenRGB integration** (#15)
  - Plugin/driver for OpenRGB
  - Sync with other RGB devices
  
- [ ] **liquidctl integration** (#15)
  - Compatible driver
  - Standard tool support

- [ ] **Windows driver** (#19)
  - HWiNFO plugin or standalone app
  - Cross-platform support

## Low Priority Features

### Advanced Features
- [ ] **Power consumption monitoring** (#14)
  - INA219/INA3221 sensors
  - Energy statistics
  - Cost calculation

- [ ] **PWM frequency per fan** (#12)
  - Individual frequency settings
  - 10-40 kHz range
  - Better compatibility

- [ ] **Multiple RGB channels** (#18)
  - Independent zones
  - Zone-based effects
  - Synchronized mode

- [ ] **Advanced RGB effects** (#17)
  - Gradient, wave, fire effects
  - Audio-reactive (with microphone)
  - Beat detection

- [ ] **Logging & diagnostics** (#21)
  - Event logging
  - Self-test mode
  - Statistics

- [ ] **USB firmware update** (#22)
  - DFU mode
  - No BOOTSEL button needed
  - Safe updates

## Future / Research

### v2.0 Considerations
- [ ] Wireless control (WiFi/Bluetooth)
- [ ] Mobile app (Android/iOS)
- [ ] Cloud integration
- [ ] Machine learning fan curves
- [ ] Voice control integration
- [ ] RGB music visualization
- [ ] Multi-device synchronization

## Implementation Order (Suggested)

### Phase 1: Essential Functionality
1. Temperature sensor integration (#7)
2. Fan failure detection (#13)
3. Standalone mode (#8)

### Phase 2: User Experience
4. Configurable startup (#10)
5. Fan profiles (#16)
6. GUI/TUI tool (#9)

### Phase 3: Advanced Features
7. OLED display (#11)
8. OpenRGB integration (#15)
9. Pump support (#20)

### Phase 4: Polish
10. Windows support (#19)
11. Advanced RGB effects (#17)
12. Remaining features as needed

## Contributing

Want to work on a feature? 
1. Check the issue for details
2. Comment your interest
3. Fork and create a PR
4. See CONTRIBUTING.md for guidelines

## Notes

- Priority may change based on community feedback
- Issues marked with 💰 if sponsorship available
- Hardware features require PCB redesign
- Some features are mutually exclusive (GPIO conflicts)

---

Last updated: 2026-02-08
