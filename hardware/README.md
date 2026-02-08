# Hardware-Design: Pico Fan Hub

Komplettes Hardware-Design für einen USB-basierten Fan Controller mit Raspberry Pi Pico.

## 📁 Verzeichnis-Übersicht

```
hardware/
├── README.md                    # Diese Datei
├── pinout.md                    # GPIO Pin-Zuweisungen
├── schematic_suggestions.md     # Detaillierte Schaltungsvorschläge
├── BLOCK_DIAGRAM.md            # System-Architektur & Signal-Flow
└── kicad/                      # KiCad-Projektdateien
    ├── pico_fan_hub.kicad_pro      # Hauptprojekt
    ├── pico_fan_hub.kicad_sch      # Schaltplan
    ├── pico_fan_hub.kicad_pcb      # PCB-Layout
    ├── pico_fan_hub_symbols.kicad_sym  # Custom Symbole
    ├── README.md                   # KiCad-Dokumentation
    └── QUICK_START.md             # Schnelleinstieg
```

## 🎯 Projekt-Status

| Bereich | Status | Beschreibung |
|---------|--------|--------------|
| **Pinout** | ✅ Fertig | Vollständige GPIO-Zuweisungen dokumentiert |
| **Schaltplan-Design** | ✅ Dokumentiert | Detaillierte Schaltungen mit Komponenten-Werten |
| **KiCad-Projekt** | 🟡 Basis vorhanden | Projekt-Setup, Custom-Symbole erstellt |
| **Schaltplan (KiCad)** | 🔴 In Arbeit | Komponenten müssen noch platziert werden |
| **PCB-Layout** | 🔴 In Arbeit | Board-Outline vorhanden, Routing offen |
| **Prototyping** | ⚪ Ausstehend | Wartet auf PCB-Fertigung |
| **Testing** | ⚪ Ausstehend | Nach Hardware-Bau |

## 📋 Hauptkomponenten

### Controller
- **Raspberry Pi Pico** (RP2040)
  - USB 2.0 Full Speed
  - 6x PWM-Ausgänge (Hardware PWM @ 25 kHz)
  - 6x GPIO-Eingänge mit Interrupt (Tachometer)
  - 1x PIO für RGB (WS2812B)
  - 264 KB SRAM, 2 MB Flash

### Power Supply
- **12V DC Eingang**
  - Schraubklemme oder DC-Barrel-Jack
  - 3A PTC Resettable Fuse
  - Verpolschutz (SS34 Schottky)
  - Überspannungsschutz (P6KE15A TVS)

- **LM2596 Buck Converter**
  - Input: 12V
  - Output: 5V @ 3A
  - Für RGB LEDs und Level-Shifter

### Level-Shifter
- **74LVC245A** (PWM: 3.3V → 5V)
  - 8-Bit Transceiver
  - 6 Kanäle für Lüfter-PWM
  
- **74LVC1G34** (RGB: 3.3V → 5V)
  - Single Buffer
  - Für WS2812B Data

### Fan Connectors
- **6x Molex KK 254** (4-Pin)
  - Pin 1: GND
  - Pin 2: +12V (direkt von 12V Rail)
  - Pin 3: TACH (zu Pico GPIO)
  - Pin 4: PWM (von Level-Shifter)

### RGB Output
- **3-Pin Header** (2.54mm)
  - Pin 1: GND
  - Pin 2: +5V
  - Pin 3: DATA (WS2812B)
  - Bis zu 60 LEDs unterstützt

### Schutzschaltungen
- 6x **10kΩ Pull-up** (Tachometer)
- 6x **100nF Filter** (Entstörung)
- 1x **330Ω Series** (RGB Data)
- Optional: **74HC14** Schmitt-Trigger

## 🔌 Pin-Zuweisungen (Raspberry Pi Pico)

### PWM-Ausgänge
```
GP0  (Pin 1)  → Fan 1 PWM
GP1  (Pin 2)  → Fan 2 PWM
GP2  (Pin 4)  → Fan 3 PWM
GP3  (Pin 5)  → Fan 4 PWM
GP4  (Pin 6)  → Fan 5 PWM
GP5  (Pin 7)  → Fan 6 PWM
```

### Tachometer-Eingänge
```
GP6  (Pin 9)  ← Fan 1 TACH
GP7  (Pin 10) ← Fan 2 TACH
GP8  (Pin 11) ← Fan 3 TACH
GP9  (Pin 12) ← Fan 4 TACH
GP10 (Pin 14) ← Fan 5 TACH
GP11 (Pin 15) ← Fan 6 TACH
```

### Sonstige
```
GP16 (Pin 21) → RGB Data Out
GP25 (Pin 25) → Onboard LED (Status)
GP15 (Pin 20) → Optional: Error LED
```

Details siehe: [pinout.md](pinout.md)

## ⚡ Technische Spezifikationen

### PWM
- **Frequenz**: 25 kHz (Standard für 4-Pin Lüfter)
- **Auflösung**: 8-Bit (0-255)
- **Spannung**: 5V (nach Level-Shift)
- **Typ**: Standard PWM (nicht Open-Drain)

### Tachometer
- **Typ**: Open-Collector-Eingang
- **Pull-up**: 10 kΩ zu 3.3V
- **Pulses/Revolution**: 2 (Standard)
- **Update-Rate**: 500 ms
- **Max. RPM**: 65535 (uint16_t)

### RGB LEDs
- **Typ**: WS2812B/SK6812 kompatibel
- **Protokoll**: 800 kHz, GRB Reihenfolge
- **Max. LEDs**: 60 (Standard), 144 (erweitert)
- **Helligkeit**: Max. 50% (default, konfigurierbar)
- **Spannung**: 5V

### Stromversorgung
- **12V Rail**: Max. 3A (6 Lüfter × 0.5A)
- **5V Rail**: Max. 3A (RGB LEDs + Logic)
- **3.3V Rail**: Max. 300mA (vom Pico)
- **USB**: 5V vom PC (nur für Pico)

## 📐 PCB-Spezifikationen

### Empfohlene Parameter
- **Größe**: 120mm × 80mm
- **Layer**: 4-Layer (oder 2-Layer)
- **Material**: FR4, 1.6mm
- **Kupfer**: 35µm (1 oz)
- **Min. Track Width**: 
  - Signal: 0.25mm
  - Power (5V): 1.0mm
  - Power (12V): 1.5mm
- **Min. Clearance**: 0.2mm
- **Via Size**: 0.8mm / 0.4mm
- **Oberfläche**: HASL oder ENIG
- **Lötmaske**: Grün (Standard)

### Montage
- **Befestigungslöcher**: 4x M3 in Ecken
- **Pico-Montage**: Through-Hole Header oder SMD
- **Lüfter-Stecker**: Am Rand für Kabelführung
- **12V-Eingang**: Nahe am Buck-Converter

## 🛠️ Hardware-Design-Workflow

### 1. Schaltplan erstellen (in Arbeit)
```bash
cd hardware/kicad
# KiCad öffnen: pico_fan_hub.kicad_pro
# Schematic Editor → Komponenten platzieren
```

Siehe: [kicad/QUICK_START.md](kicad/QUICK_START.md)

### 2. Footprints zuweisen
- Alle Symbole → Footprints zuordnen
- 3D-Modelle prüfen
- Pad-Größen verifizieren

### 3. PCB-Layout
- Komponenten platzieren
- Critical Signals routen
- Power Planes füllen (GND, +12V, +5V)
- DRC (Design Rules Check)

### 4. Gerber-Export
- Alle Layers exportieren
- Drill-Files generieren
- Zip für Hersteller

### 5. Fertigung
- PCB bestellen (JLCPCB, PCBWay, etc.)
- Bauteile bestellen (siehe BOM)
- Stencil optional (für SMD)

### 6. Bestückung & Test
- Komponenten löten
- Visual Inspection
- Power-On Test (ohne ICs)
- Firmware flashen
- Funktionstest

## 📦 Bill of Materials (BOM)

### ICs
| Ref | Part | Package | Qty | Beschreibung |
|-----|------|---------|-----|--------------|
| U1 | LM2596 | TO-263 | 1 | Buck Regulator 12V→5V |
| U2 | Raspberry Pi Pico | TH Module | 1 | Mikrocontroller |
| U3 | 74LVC245A | TSSOP-20 | 1 | Level Shifter 8-Bit |
| U4 | 74LVC1G34 | SOT-23-5 | 1 | Buffer für RGB |
| U5 | 74HC14 | SOIC-14 | 1 | Schmitt-Trigger (optional) |

### Passive
| Ref | Value | Package | Qty | Beschreibung |
|-----|-------|---------|-----|--------------|
| R1-R6 | 10kΩ | 0805 | 6 | Tachometer Pull-up |
| R7 | 330Ω | 0805 | 1 | RGB Series |
| R8 | 1kΩ | 0805 | 1 | Power LED |
| R9 | 220Ω | 0805 | 1 | Status LED |
| C1 | 470µF 25V | Radial | 1 | 12V Filter |
| C2 | 1000µF 16V | Radial | 1 | 5V Filter |
| C3-C4 | 100µF 16V | Radial | 2 | Decoupling |
| C5-C12 | 100nF | 0805 | 8 | Bypass/Filter |

### Connector
| Ref | Type | Qty | Beschreibung |
|-----|------|-----|--------------|
| J1 | Screw Terminal 2P | 1 | 12V Input |
| J2-J7 | Molex KK 4P | 6 | Fan Connectors |
| J8 | Pin Header 1x3 | 1 | RGB Output |

### Diodes
| Ref | Part | Package | Qty | Beschreibung |
|-----|------|---------|-----|--------------|
| D1 | SS34 | SMA | 1 | Verpolschutz |
| D2 | P6KE15A | SMA | 1 | TVS 12V |
| D3 | P6KE6.8A | SMA | 1 | TVS 5V |
| D4 | LED Green | 0805 | 1 | Power LED |
| D5 | LED Blue | 0805 | 1 | Status LED |

### Protection
| Ref | Part | Qty | Beschreibung |
|-----|------|-----|--------------|
| F1 | PTC 3A | 1 | Resettable Fuse |

**Geschätzte Kosten**: ~25-30€ (PCB + Komponenten, ohne Pico)

Detaillierte BOM siehe: [schematic_suggestions.md](schematic_suggestions.md)

## 🔬 Test-Plan

### Power-On Tests
1. ✓ Visuell inspizieren (Kurzschlüsse, Brücken)
2. ✓ 12V anlegen, Strom messen (< 50mA ohne Last)
3. ✓ 5V Rail messen (4.75-5.25V)
4. ✓ 3.3V Rail messen (3.2-3.4V)
5. ✓ Power LED leuchtet

### Ohne Firmware
6. ✓ Alle Spannungen stabil unter Last
7. ✓ Keine heißen Komponenten

### Mit Firmware
8. ✓ Pico LED blinkt (Status)
9. ✓ USB wird erkannt (`lsusb`)
10. ✓ HID Device erscheint (`ls /dev/hidraw*`)

### Funktions-Tests
11. ✓ PWM-Ausgänge messen (Oszilloskop: 25 kHz)
12. ✓ Lüfter anschließen, PWM testen
13. ✓ Tachometer-Signale verifizieren
14. ✓ RPM-Messung korrekt
15. ✓ RGB LEDs funktionieren
16. ✓ Software-Integration (hwmon)

## 📚 Dokumentation

### Haupt-Dokumente
- **[pinout.md](pinout.md)**: GPIO-Zuweisungen und Hardware-Anforderungen
- **[schematic_suggestions.md](schematic_suggestions.md)**: Detaillierte Schaltungen mit Bauteilen
- **[BLOCK_DIAGRAM.md](BLOCK_DIAGRAM.md)**: System-Architektur und Signal-Fluss
- **[kicad/README.md](kicad/README.md)**: KiCad-spezifische Dokumentation

### Quick-Start Guides
- **[kicad/QUICK_START.md](kicad/QUICK_START.md)**: KiCad in 5 Minuten

### Externe Ressourcen
- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
- [Pico Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- [74LVC245 Datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc245a.pdf)
- [WS2812B Datasheet](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- [Intel 4-Wire PWM Spec](https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/4-wire-pwm-spec-rev1-2.pdf)

## 🚀 Nächste Schritte

1. **Schaltplan detaillieren** ⏳
   - Alle Komponenten in KiCad platzieren
   - Verbindungen zeichnen
   - ERC durchführen

2. **PCB-Layout** 🔜
   - Komponenten optimal platzieren
   - Power-Routing
   - Signal-Routing
   - DRC durchführen

3. **Prototype bestellen** 🔜
   - Gerber-Export
   - Bei PCB-Hersteller bestellen
   - Bauteile bestellen

4. **Hardware-Tests** 🔜
   - Bestücken
   - Funktionstest
   - Firmware-Integration
   - Dokumentation aktualisieren

## 🤝 Mitwirken

Beiträge zum Hardware-Design sind willkommen!

- Verbesserungen an Schaltungen
- KiCad-Layout-Optimierungen
- Test-Ergebnisse teilen
- Alternative Designs vorschlagen

Siehe [../CONTRIBUTING.md](../CONTRIBUTING.md) für Details.

## 📄 Lizenz

Open Hardware - siehe [../LICENSE](../LICENSE)

---

**Status**: Projekt in aktiver Entwicklung  
**Version**: 1.0 (Prototype)  
**Letztes Update**: 2026-02-08
