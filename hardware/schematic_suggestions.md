# KiCad Schaltplan-Vorschläge

Detaillierte Schaltungsvorschläge für das Hardware-Design im KiCad.

## Hauptkomponenten

### 1. Raspberry Pi Pico

**Montage:**
- Als Steckmodul mit 2x 20-Pin Headers (2.54mm Rastermaß)
- Oder direkt auf Board löten für kompaktere Bauform

**Stromversorgung:**
- VSYS (Pin 39): 5V vom USB oder externe Versorgung
- 3V3(OUT) (Pin 36): 3.3V für Logik (max. 300mA)
- GND: Mehrere Pins zur Verfügung

## 2. Lüfter-Anschlüsse (6x)

### 4-Pin Molex KK Stecker

**Pin-Belegung pro Lüfter:**
1. GND (Schwarz)
2. +12V (Gelb)
3. TACH - Tachometer (Grün)
4. PWM - Steuerung (Blau)

### Schaltung pro Lüfter

```
                    +12V (von Netzteil)
                      │
                      │
                      ├─────────── Pin 2 (Lüfter +12V)
                      │
[Pico GPIO PWM]───────┼─────[Level Shifter]─────── Pin 4 (Lüfter PWM)
                      │
                      │
[Pico GPIO TACH]──────┼─────[Pull-up 10kΩ]────┬─── Pin 3 (Lüfter TACH)
                      │                        │
                      │                    [100nF Filter]
                      │                        │
                    [GND]────────────────────┴─── Pin 1 (Lüfter GND)
```

### Level-Shifter für PWM (3.3V → 5V)

**Option A: 74LVC245 (8-Bit Transceiver)**

```
        Pico 3.3V                    5V Rail
            │                            │
            ├─── VCCA (20)      VCCB (10) ───┤
            │                            │
    PWM1 ───┼─── A1 (2)          B1 (18) ───┼─── PWM1 to Fan
    PWM2 ───┼─── A2 (3)          B2 (17) ───┼─── PWM2 to Fan
    PWM3 ───┼─── A3 (4)          B3 (16) ───┼─── PWM3 to Fan
    PWM4 ───┼─── A4 (5)          B4 (15) ───┼─── PWM4 to Fan
    PWM5 ───┼─── A5 (6)          B5 (14) ───┼─── PWM5 to Fan
    PWM6 ───┼─── A6 (7)          B6 (13) ───┼─── PWM6 to Fan
            │                            │
         ───┴─── DIR (1) = VCC      OE (19) ───── GND
            │                            │
          [GND]──────── GND (10) ────────┴──── [GND]
```

**Bauteile:**
- IC1: 74LVC245A
- C1: 100nF Keramik-Kondensator (VCCA)
- C2: 100nF Keramik-Kondensator (VCCB)

**Option B: Diskrete MOSFETs (BSS138)**

Pro PWM-Kanal:

```
    +5V
     │
     ├─── 10kΩ Pull-up ───┬─── To Fan PWM
     │                    │
     │              [D] BSS138 [S]
     │                    │
[Pico GPIO] ─── 10kΩ ───[G]
                         │
                       [GND]
```

**Bauteile pro Kanal:**
- Q1: BSS138 N-Channel MOSFET
- R1: 10kΩ (Gate)
- R2: 10kΩ (Pull-up to 5V)

### Tachometer-Eingang

**Schaltung pro Lüfter:**

```
                      +3.3V
                        │
                        ├─── 10kΩ Pull-up
                        │
                        ├────────────── To Pico GPIO
                        │
    From Fan TACH ──────┼─── 100nF ─── GND
                        │
                        ├─── Optional: 74HC14 Schmitt-Trigger
                        │
                      [GND]
```

**Einfache Version (Bauteile pro Kanal):**
- R1: 10kΩ Pull-up
- C1: 100nF Keramik-Kondensator (Entstörung)

**Erweiterte Version mit Schmitt-Trigger:**
- R1: 10kΩ Pull-up
- C1: 100nF Keramik-Kondensator
- IC: 74HC14 (ein Gate pro Kanal, 6 Gates im Chip)

## 3. RGB LED-Ausgang

### WS2812B Ansteuerung

```
                 +5V (für LEDs)
                   │
                   ├────────── WS2812B VDD
                   │
                 [1000µF
                  Elko]
                   │
[Pico GPIO16] ─────┼─── [Level Shifter] ─── 330Ω ─── WS2812B DATA
                   │
                 [GND]────────── WS2812B GND
```

### Level-Shifter für Data (3.3V → 5V)

**Option A: 74LVC1G34 (Single Buffer)**

```
    Pico 3.3V                    5V Rail
        │                            │
        ├─── VCC (5)         VCCB ───┤
        │                            │
    GPIO16 ──┴─── A (2)    Y (4) ────┴─── 330Ω ─── WS2812B DATA
        │                            │
      [GND]──── GND (3) ───────────[GND]
```

**Bauteile:**
- IC: 74LVC1G34DBV (SOT-23-5)
- R1: 330Ω (Serienwiderstand)
- C1: 100nF (VCC)
- C2: 1000µF Elko (5V für LEDs)

**Option B: Diskret mit MOSFET**

```
    +5V
     │
     ├─── 10kΩ ───┬─── 330Ω ─── To WS2812B DATA
     │            │
     │      [D] BSS138 [S]
     │            │
[GPIO16] ─── 10kΩ ───[G]
                  │
                [GND]
```

### WS2812B LED-Kette

```
5V ────┬─── [1000µF] ───┬─── LED1 VDD ─── LED2 VDD ─── ...
       │                │
DATA ──┼────────────────┼─── LED1 DIN ─╮
       │                │               │
       │                │        LED1 DOUT ─── LED2 DIN ─╮
       │                │                                 │
GND ───┴────────────────┴─── LED1 GND ─── LED2 GND ─── LED2 DOUT ─── ...
```

**Wichtig:**
- Großer Kondensator (1000µF+) nah an der Stromversorgung
- Kurze Leitung vom Level-Shifter zum ersten LED (< 15cm)
- Optional: 1000µF Kondensator alle 30-50 LEDs

## 4. Stromversorgung

### 12V-Eingang (Lüfter)

```
12V DC IN (+) ────┬─── Sicherung 3A ─── Verpolschutz ─── +12V Rail
                  │
                  ├─── P6KE15A TVS Diode
                  │
12V DC IN (-) ────┴─────────────────────────────────────── GND
```

**Bauteile:**
- F1: Sicherung 3A (Resettable Fuse / PTC)
- D1: Verpolschutz-Diode (SS34 Schottky)
- D2: P6KE15A TVS-Diode (Überspannungsschutz)
- C1: 470µF Elko (Pufferung)

**Anschluss:**
- Schraubklemme 2-polig (5.08mm Rastermaß)
- Oder DC-Barrel-Jack (5.5mm × 2.1mm)

### 5V-Eingang (RGB LEDs)

**Option A: Von Pico USB**
```
Pico VBUS (Pin 40) ───── +5V Rail (max. 500mA!)
```

**Option B: Separate 5V-Versorgung**
```
5V DC IN (+) ────┬─── Sicherung 2A ─── +5V Rail
                 │
                 ├─── P6KE6.8A TVS Diode
                 │
5V DC IN (-) ────┴─────────────────────────────── GND
```

**Option C: Buck-Converter von 12V**
```
+12V ─── Buck Converter (LM2596) ─── +5V @ 3A
```

### 3.3V (Pico Logik)

```
Pico 3V3(OUT) ───── +3.3V Rail (max. 300mA)
```

**Hinweis:** Pico erzeugt 3.3V intern aus USB/VSYS

## 5. Schutzschaltungen

### ESD-Schutz an externen Anschlüssen

**Pro Anschluss:**
```
Signal ───┬─── 100Ω ─── To Pico GPIO
          │
       [PRTR5V0U2X]
       ESD Protection
          │
        [GND]
```

### Überstrom-Schutz (Lüfter)

**Optional: MOSFET-Schalter pro Lüfter**

```
+12V ───[D]───┬─── To Fan +12V
          │   │
     [AO3400]│
        MOSFET│
          │   │
        [G]   │
          │   │
    [10kΩ]   │
          │   │
    GPIO ─┴───┘
          │
        [S]
          │
        [GND]
```

Ermöglicht:
- Software-Kontrolle über Lüfter-Stromversorgung
- Überstrom-Erkennung (mit Sense-Widerstand)

## 6. Status-LEDs

### Power-LED

```
+12V ─── 1kΩ ─── LED (Grün) ─── GND
```

### Status-LED (vom Pico gesteuert)

```
GPIO15 ─── 220Ω ─── LED (Blau) ─── GND
```

## 7. Zusätzliche Features (Optional)

### Temperatursensor (I2C)

```
Pico SDA (GPIO4) ───── SDA ───┐
                               │
Pico SCL (GPIO5) ───── SCL ───┤
                               │
+3.3V ─────────────── VCC ─────┤──── [BME280 / Si7021]
                               │
GND ───────────────── GND ─────┘
```

### OLED-Display (I2C)

```
Pico SDA (GPIO4) ───── SDA ───┐
                               │
Pico SCL (GPIO5) ───── SCL ───┤
                               │
+3.3V ─────────────── VCC ─────┤──── [SSD1306 OLED]
                               │      128x64 Pixel
GND ───────────────── GND ─────┘
```

## PCB-Layout-Hinweise

### Layer-Stack (4-Layer empfohlen)

1. **Top Layer**: Signale, Bauteile
2. **Inner Layer 1**: GND Plane
3. **Inner Layer 2**: Power Planes (+12V, +5V, +3.3V)
4. **Bottom Layer**: Signale, Bauteile

### Leiterbahnbreiten

- **12V @ 2A**: Mindestens 1.5mm (besser 2mm)
- **5V @ 3A**: Mindestens 1.5mm
- **3.3V @ 300mA**: Mindestens 0.5mm
- **Signale**: 0.25mm (Standard)
- **PWM**: 0.4mm (für saubere Flanken)

### Placement

```
┌──────────────────────────────────────────┐
│  [12V IN]                      [USB]     │
│                                           │
│  [Sicherung]  [Buck 5V]    [Pico Module] │
│                                           │
│  ┌─────────────────────────────────────┐ │
│  │     [74LVC245 Level Shifter]        │ │
│  └─────────────────────────────────────┘ │
│                                           │
│  [Fan1] [Fan2] [Fan3] [Fan4] [Fan5] [Fan6│]
│   PWM    PWM    PWM    PWM    PWM    PWM  │
│  TACH   TACH   TACH   TACH   TACH   TACH │
│                                           │
│  [RGB Out]    [Status LEDs]               │
│                                           │
└──────────────────────────────────────────┘
```

### Kritische Signale

**PWM-Leitungen:**
- So kurz wie möglich
- Weg von Tachometer-Leitungen (Übersprechen)
- Ground Guard Traces

**Tachometer-Leitungen:**
- Weg von PWM und RGB
- Filter-Kondensatoren nah am Anschluss
- Optional: Differenzielle Führung mit GND

**RGB Data:**
- Sehr kurz vom Level-Shifter zum ersten LED
- 50Ω Impedanz (falls möglich)
- GND-Referenz daneben

### Test-Punkte

Platziere Test-Punkte für:
- Alle Spannungen (+12V, +5V, +3.3V, GND)
- Alle PWM-Ausgänge
- Alle Tachometer-Eingänge
- RGB-Datenleitung

### Montage

**Befestigungslöcher:**
- 4x M3 Schrauben in den Ecken
- Abstand: Raster 5mm

**Abmessungen (Vorschlag):**
- Breite: 120mm
- Tiefe: 80mm
- Höhe: 25mm (mit Pico)

## Bill of Materials (BOM) - Hauptkomponenten

| Referenz | Wert/Typ | Beschreibung | Menge |
|----------|----------|--------------|-------|
| U1 | Raspberry Pi Pico | Mikrocontroller | 1 |
| U2 | 74LVC245A | Level Shifter 8-Bit | 1 |
| U3 | 74LVC1G34 | Buffer für RGB | 1 |
| U4 | LM2596 | Buck Converter 12V→5V | 1 |
| J1-J6 | Molex KK 4-Pin | Lüfter-Anschlüsse | 6 |
| J7 | 3-Pin Header | RGB-Ausgang | 1 |
| J8 | Schraubklemme 2-pol | 12V Eingang | 1 |
| F1 | 3A PTC | Resettable Fuse | 1 |
| D1 | SS34 | Schottky Diode | 1 |
| D2 | P6KE15A | TVS Diode | 1 |
| R1-R6 | 10kΩ | Pull-up Tachometer | 6 |
| R7 | 330Ω | RGB Serienwiderstand | 1 |
| C1-C8 | 100nF | Bypass Kondensatoren | 8 |
| C9 | 1000µF 16V | Power Buffer 5V | 1 |
| C10 | 470µF 25V | Power Buffer 12V | 1 |

## KiCad Libraries

**Footprints benötigt:**
- Raspberry_Pi_Pico:Pico_TH
- Package_SO:TSSOP-20_4.4x6.5mm
- Connector_Molex:Molex_KK-254_1x04
- Diode_SMD:D_SMA
- Capacitor_SMD:C_0805

**Symbols benötigt:**
- MCU_RaspberryPi:Pico
- 74xx:74LVC245
- Logic_LevelTranslator:74LVC1G34
- Regulator_Switching:LM2596

## Referenz-Projekte

Siehe:
- Corsair Commander Pro (ähnliche Funktionalität)
- Aquacomputer Quadro (PWM Fan Controller)
- Open-Source: https://github.com/CalcProgrammer1/OpenRGB
