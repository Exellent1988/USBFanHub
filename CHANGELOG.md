# Changelog

Alle bedeutenden Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt
- Initiales Projekt-Setup
- Pico-Firmware mit vollständiger Funktionalität:
  - 6x PWM-Ausgänge (25 kHz) für Lüfter-Steuerung
  - 6x Tachometer-Eingänge für RPM-Messung
  - RGB LED-Steuerung via WS2812B/NeoPixel (PIO-basiert)
  - USB HID Interface für Kommunikation
  - Watchdog für Sicherheit
- Linux Software:
  - Python-basierter USB HID Driver
  - hwmon-kompatible sysfs-Bridge
  - CLI-Tool für direkte Steuerung
  - Daemon für hwmon-Integration
- Umfangreiche Dokumentation:
  - Hardware-Pinout und Schaltungsvorschläge
  - USB HID Protokoll-Spezifikation
  - RGB-Steuerungs-Dokumentation
  - Build- und Installations-Anleitungen
  - KiCad Schaltplan-Vorschläge
- Build-Automatisierung:
  - CMake Build-System für Firmware
  - Python setuptools für Software
  - Build-Script mit Fehlerbehandlung
- Git-Infrastruktur:
  - .gitignore für alle Artefakte
  - CONTRIBUTING.md für Entwickler
  - Dieser CHANGELOG

## [1.0.0] - TBD

Erste offizielle Release-Version (geplant nach Hardware-Tests)

### Geplant
- Hardware-Tests mit echten Lüftern
- Performance-Optimierungen
- Erweiterte Fehlerbehandlung
- Zusätzliche RGB-Effekte
- OpenRGB-Integration
- liquidctl-Kompatibilität

## Roadmap

### v1.1.0 (geplant)
- [ ] Temperatursensor-Unterstützung (I2C)
- [ ] OLED-Display für Status-Anzeige
- [ ] Erweiterte Lüfter-Kurven (PID-Regler)
- [ ] Konfigurationsspeicherung im Flash
- [ ] Web-Interface für Konfiguration

### v1.2.0 (geplant)
- [ ] Unterstützung für mehr als 6 Lüfter
- [ ] Mehrere RGB-Kanäle
- [ ] Audio-reaktive RGB-Modi
- [ ] Erweitertes Monitoring (Spannung, Strom)

### v2.0.0 (Zukunft)
- [ ] Drahtlose Steuerung (Bluetooth/WiFi)
- [ ] Mobile App (Android/iOS)
- [ ] Cloud-Integration für Remote-Monitoring
- [ ] Machine Learning für automatische Lüfter-Kurven

---

## Format-Legende

- `Hinzugefügt` für neue Features
- `Geändert` für Änderungen an bestehender Funktionalität
- `Veraltet` für bald zu entfernende Features
- `Entfernt` für entfernte Features
- `Behoben` für Bugfixes
- `Sicherheit` für Sicherheits-Updates
