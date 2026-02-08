# Hardware Pinout - Raspberry Pi Pico Fan Hub

## Pin-Zuweisungen

### PWM-Ausgänge für Lüfter (25 kHz)

| Lüfter | GPIO Pin | PWM Slice | PWM Channel |
|--------|----------|-----------|-------------|
| Fan 1  | GPIO 0   | PWM0      | A           |
| Fan 2  | GPIO 1   | PWM0      | B           |
| Fan 3  | GPIO 2   | PWM1      | A           |
| Fan 4  | GPIO 3   | PWM1      | B           |
| Fan 5  | GPIO 4   | PWM2      | A           |
| Fan 6  | GPIO 5   | PWM2      | B           |

### Tachometer-Eingänge

| Lüfter | GPIO Pin | Anmerkungen                          |
|--------|----------|--------------------------------------|
| Fan 1  | GPIO 6   | Pull-up 10kΩ, Interrupt-fähig       |
| Fan 2  | GPIO 7   | Pull-up 10kΩ, Interrupt-fähig       |
| Fan 3  | GPIO 8   | Pull-up 10kΩ, Interrupt-fähig       |
| Fan 4  | GPIO 9   | Pull-up 10kΩ, Interrupt-fähig       |
| Fan 5  | GPIO 10  | Pull-up 10kΩ, Interrupt-fähig       |
| Fan 6  | GPIO 11  | Pull-up 10kΩ, Interrupt-fähig       |

### RGB LED-Ausgang

| Funktion      | GPIO Pin | Anmerkungen                    |
|---------------|----------|--------------------------------|
| RGB Data Out  | GPIO 16  | WS2812B/NeoPixel kompatibel    |

### Status-LEDs (Optional)

| Funktion      | GPIO Pin | Anmerkungen                    |
|---------------|----------|--------------------------------|
| Status LED    | GPIO 25  | Onboard-LED (Pico)             |
| Error LED     | GPIO 15  | Optional für Fehleranzeige     |

## Hardware-Anforderungen und Schaltung

### PWM-Ausgänge

4-Pin-Lüfter erwarten PWM-Signale mit folgenden Eigenschaften:
- **Frequenz**: 25 kHz (Standard), 21-28 kHz akzeptabel
- **Spannung**: 5V oder Open-Drain mit Pull-up zu 5V
- **Duty Cycle**: 0-100% (0% = volle Geschwindigkeit, 100% = gestoppt bei vielen Lüftern)

**Level-Shifter-Schaltung:**
```
Pico GPIO (3.3V) → Level Shifter (3.3V → 5V) → Lüfter PWM-Pin
```

Empfohlene ICs:
- 74LVC245 (8-Bit Transceiver)
- TXS0108E (8-Bit Bi-directional Level Shifter)
- Diskrete MOSFETs (BSS138) für jede Leitung

### Tachometer-Eingänge

Tachometer-Signale sind Open-Collector-Ausgänge:
- **Frequenz**: 2 Impulse pro Umdrehung (typisch)
- **Spannung**: Open-Collector, benötigt Pull-up
- **Pull-up**: 10 kΩ nach 3.3V (Pico-seitig)

**Schaltung pro Lüfter:**
```
Lüfter Tacho-Pin → [Optional: 100nF Filter] → [10kΩ Pull-up zu 3.3V] → Pico GPIO
                                              
Optional: Schmitt-Trigger (74HC14) für bessere Störfestigkeit
```

**Berechnungs-Formel für RPM:**
```
RPM = (Impulse pro Sekunde × 60) / 2
```

### RGB LED-Ausgang

WS2812B/NeoPixel addressierbare LEDs:
- **Spannung**: 5V Versorgung
- **Datenleitung**: 5V Logik-Level (Level-Shifting erforderlich!)
- **Timing**: Präzises Timing erforderlich (350ns ±150ns)

**Schaltung:**
```
Pico GPIO16 → 74LVC1G34 (Buffer/Level Shifter) → WS2812B Data In
                                               
5V Power → [1000µF Kondensator] → WS2812B VDD
```

**Wichtig:**
- 330-470Ω Serienwiderstand am Datenausgang empfohlen
- Großer Kondensator (1000µF+) an 5V-Versorgung für LEDs
- Kurze Leitungen zum ersten LED verwenden (< 15cm)

## Stromversorgung

### 12V-Schiene (Lüfter)
- Externe 12V Stromversorgung erforderlich
- Geschätzte Last: 6 Lüfter × 0.2A = ~1.2A (typisch)
- Empfohlenes Netzteil: 12V, 3A oder höher

### 5V-Schiene (RGB LEDs)
- Kann vom Pico USB-Port kommen (für wenige LEDs)
- Für mehr LEDs: Separate 5V-Versorgung empfohlen
- Geschätzte Last: RGB LEDs variabel (60 LEDs ≈ 3A bei voller Helligkeit)

### 3.3V-Schiene (Pico)
- Direkt vom Pico-USB
- Pico verbraucht ~20-50mA im Betrieb

## Schutz-Schaltungen

### Überspannungsschutz
- TVS-Dioden an allen externen Anschlüssen
- Schottky-Dioden an GPIO-Pins (falls noch nicht intern vorhanden)

### Strombegrenzung
- Widerstände in Serie zu den GPIO-Pins (100-330Ω)
- Sicherung auf 12V-Eingang

### ESD-Schutz
- Alle externen Anschlüsse mit ESD-Schutzdioden

## Mechanische Abmessungen

Standard 4-Pin PWM-Lüfter-Stecker:
- Molex KK 2.54mm Rastermaß
- 4 Pins: GND, +12V, TACH, PWM

WS2812B LED-Anschluss:
- 3 Pins: GND, +5V, DATA
- Standard 2.54mm Header

## KiCad Design-Hinweise

1. **Schaltungs-Design:**
   - Separate Ground-Planes für Digital/Analog wenn möglich
   - Kurze PWM-Leitungen für saubere Signale
   - Bypass-Kondensatoren (100nF) an allen ICs

2. **PCB Layout:**
   - Mindestens 2-Layer Board (4-Layer besser)
   - Dicke Leiterbahnen für 12V-Versorgung (>1mm)
   - Guard Rings um kritische analoge Bereiche

3. **Komponenten:**
   - Molex KK 254 Stecker für Lüfter
   - USB-C oder Micro-USB für Pico-Montage
   - Schraubklemmen für 12V-Eingang
   - 3-Pin Header für RGB-Ausgang

4. **Montage:**
   - Befestigungslöcher für Gehäuse
   - Pico als Steckmodul (mit Pin-Headern) für einfachen Austausch
   - Kühlkörper-Pads für Level-Shifter (falls nötig)

## Testpunkte

Für Debugging und Entwicklung:
- Testpunkte an allen PWM-Ausgängen
- Testpunkte an allen Tacho-Eingängen
- Testpunkt an RGB-Datenleitung
- Testpunkte an Spannungsschienen (12V, 5V, 3.3V)
- Ground-Testpunkte

## Erweiterungsmöglichkeiten

- Temperatursensor (I2C) für Ambient-Temperatur
- Zusätzliche PWM-Ausgänge für Pumpen
- Zusätzliche RGB-Kanäle
- OLED-Display für Status-Anzeige (I2C)
