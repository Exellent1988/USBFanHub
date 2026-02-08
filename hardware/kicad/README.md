# KiCad Hardware-Design für Pico Fan Hub

Dieses Verzeichnis enthält die KiCad-Projektdateien für den Pico Fan Hub.

## Dateien

- `pico_fan_hub.kicad_pro` - Hauptprojektdatei
- `pico_fan_hub.kicad_sch` - Schaltplan
- `pico_fan_hub_symbols.kicad_sym` - Custom Symbol Library
- `pico_fan_hub.kicad_pcb` - PCB Layout (in Arbeit)

## KiCad Version

Erstellt mit KiCad 6.0 / 7.0. Kompatibel mit neueren Versionen.

## Projekt öffnen

1. KiCad starten
2. Projekt öffnen: `pico_fan_hub.kicad_pro`
3. Schaltplan-Editor öffnen (Schematic Editor)

## Hauptkomponenten im Schaltplan

### 1. Stromversorgung
- **J1**: 12V DC Eingang (Schraubklemme oder DC-Barrel)
- **U1**: LM2596 Buck Converter (12V → 5V @ 3A)
- **C1-C4**: Filterkondensatoren

### 2. Raspberry Pi Pico
- **U2**: Raspberry Pi Pico Modul
- Pin-Zuweisungen:
  - GP0-GP5: PWM-Ausgänge
  - GP6-GP11: Tachometer-Eingänge
  - GP16: RGB Data Out

### 3. Level-Shifter (PWM)
- **U3**: 74LVC245A (8-Bit Transceiver)
- Konvertiert 3.3V PWM → 5V PWM für Lüfter
- DIR Pin fest auf VCC (A→B Richtung)
- OE Pin auf GND (Output Enable)

### 4. Lüfter-Anschlüsse
- **J2-J7**: 6x Molex KK 254 4-Pin Stecker
- Pin-Belegung:
  1. GND
  2. +12V
  3. TACH (zu Pico GPIO)
  4. PWM (von Level-Shifter)

### 5. Tachometer-Schaltungen
- **R1-R6**: 10kΩ Pull-up Widerstände (zu 3.3V)
- **C5-C10**: 100nF Filter-Kondensatoren
- Optional: **U4** 74HC14 Schmitt-Trigger für bessere Entstörung

### 6. RGB LED-Ausgang
- **U5**: 74LVC1G34 Level-Shifter (3.3V → 5V)
- **R7**: 330Ω Serienwiderstand
- **J8**: 3-Pin Header für WS2812B
  1. GND
  2. +5V
  3. DATA

### 7. Schutzschaltungen
- **F1**: 3A PTC Resettable Fuse (12V Eingang)
- **D1**: SS34 Schottky Diode (Verpolschutz)
- **D2**: P6KE15A TVS Diode (Überspannungsschutz)
- **D3**: P6KE6.8A TVS Diode (5V Schutz)

### 8. Status-LEDs
- **D4**: Grüne Power-LED (12V aktiv)
- **D5**: Blaue Status-LED (GPIO15 gesteuert)

## Symbol Libraries

### Standard KiCad Libraries (benötigt):
```
- Device (R, C, LED, etc.)
- Connector (Headers, Schraubklemmen)
- power (GND, +12V, +5V, +3V3)
- 74xx (Logic ICs)
- Regulator_Switching (LM2596)
```

### Custom Symbols (in pico_fan_hub_symbols.kicad_sym):
- `RPi_Pico` - Raspberry Pi Pico Modul
- `74LVC245` - Level Shifter
- `FAN_4Pin` - 4-Pin Lüfter-Anschluss mit Fan-Symbol

## Footprint Libraries

### Benötigte Footprints:
```
- RPi_Pico:RPi_Pico_TH (Through-Hole Montage)
- Package_SO:TSSOP-20_4.4x6.5mm (74LVC245)
- Package_TO_SOT_SMD:SOT-23-5 (74LVC1G34)
- Connector_Molex:Molex_KK-254_1x04_P2.54mm (Lüfter)
- Connector_PinHeader:PinHeader_1x03_P2.54mm (RGB)
- TerminalBlock_Phoenix:PhoenixContact_MKDS_2pol (12V Eingang)
- Package_TO_SOT_SMD:TO-263-5 (LM2596)
- Diode_SMD:D_SMA (Dioden)
- Resistor_SMD:R_0805
- Capacitor_SMD:C_0805
- Capacitor_THT:CP_Radial_D10.0mm_P5.0mm (Elkos)
```

## Schaltplan-Hierarchie

```
pico_fan_hub.kicad_sch (Main Sheet)
├── Power Supply Section
│   ├── 12V Input & Protection
│   └── 5V Buck Converter
├── Raspberry Pi Pico
├── PWM Level Shifter
├── Fan Connectors (6x)
├── Tachometer Inputs (6x)
├── RGB Output
└── Status LEDs
```

## Design Rules Check (DRC)

Vor der PCB-Fertigung:

1. **Electrical Rules Check (ERC) im Schaltplan:**
   - Tools → Electrical Rules Checker
   - Alle Fehler beheben
   - Warnungen prüfen

2. **PCB Design Rules Check:**
   - Mindestens 0.2mm Leiterbahnbreite für Signale
   - Mindestens 1.5mm für 12V/5V Power
   - Mindestens 0.2mm Clearance
   - Via Größe: 0.8mm / 0.4mm (Durchmesser/Bohrdurchmesser)

## PCB Spezifikationen (empfohlen)

- **Layer**: 4-Layer (oder 2-Layer für einfache Version)
- **Material**: FR4, 1.6mm
- **Kupfer**: 35µm (1 oz)
- **Oberfläche**: HASL oder ENIG
- **Lötmaske**: Grün (oder nach Wahl)
- **Bestückungsdruck**: Weiß
- **Abmessungen**: ~120mm × 80mm

## Layout-Hinweise

1. **Power Planes:**
   - GND Plane auf Layer 2
   - +12V / +5V Planes auf Layer 3
   - Dicke Via-Stitching für gute Kühlung

2. **Critical Traces:**
   - PWM-Signale: Kurz halten, weg von Tachometer
   - RGB Data: So kurz wie möglich, 50Ω wenn möglich
   - Tachometer: Guard mit GND, Filter nah am Eingang

3. **Komponenten-Platzierung:**
   - Pico zentral
   - Level-Shifter zwischen Pico und Lüfter-Anschlüssen
   - Buck Converter nahe am 12V Eingang
   - Lüfter-Stecker am Rand
   - RGB-Ausgang nahe am Pico

4. **Thermal Management:**
   - Thermal Vias unter LM2596
   - Große Kupferflächen für 12V/5V
   - Optional: Kühlkörper-Pads

## BOM (Bill of Materials)

Eine detaillierte Stückliste wird automatisch aus dem Schaltplan generiert:
- Tools → Generate BOM

Oder verwende das CSV-Export-Plugin.

Hauptkomponenten siehe auch: `../schematic_suggestions.md`

## Fertigung

### Gerber-Export:

1. PCB Editor öffnen
2. File → Plot
3. Einstellungen:
   - Format: Gerber
   - Include Layers: All necessary
   - Use Protel filename extensions
4. Plot
5. Generate Drill Files

### PCB-Hersteller:

Empfohlene Anbieter:
- JLCPCB (China, günstig)
- PCBWay (China)
- Aisler (Europa)
- Beta Layout (Deutschland)

## 3D-Ansicht

KiCad kann eine 3D-Vorschau generieren:
- View → 3D Viewer
- Prüfe Komponenten-Clearance
- Export für mechanisches Design möglich

## Version Control

Wichtig für Git:
- `.kicad_pcb-bak` und `.kicad_sch-bak` sind in .gitignore
- Nur Quell-Dateien committen (.kicad_pro, .kicad_sch, .kicad_pcb)
- Gerber-Files optional in separatem Branch

## Erweiterungen

Mögliche Erweiterungen (neue Sheets):
- Temperatursensor (I2C)
- OLED-Display
- Zusätzliche PWM-Kanäle
- Spannungs-/Strom-Monitoring

## Support

Bei Fragen zum Hardware-Design:
- KiCad Dokumentation: https://docs.kicad.org/
- KiCad Forum: https://forum.kicad.info/
- Siehe auch: `../schematic_suggestions.md` für detaillierte Schaltungen

## Lizenz

Open Hardware - siehe Hauptprojekt LICENSE
