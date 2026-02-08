# RGB LED-Steuerung

## Übersicht

Der Pico Fan Hub unterstützt addressierbare RGB LEDs (WS2812B/NeoPixel) für RGB-Lüfter oder externe LED-Strips.

## Hardware

### Unterstützte LED-Typen
- WS2812B (NeoPixel)
- WS2813
- SK6812
- Kompatible addressierbare RGB LEDs

### Maximale Anzahl
- **Standard**: 60 LEDs
- **Erweitert**: Bis zu 144 LEDs (mit Leistungseinschränkungen)

### Anschluss
3-Pin Header:
1. GND
2. +5V (externe Versorgung empfohlen für >10 LEDs)
3. Data (GPIO16)

## Steuerung via USB HID

### Direkte Farb-Steuerung

```python
import struct

def set_rgb_leds(device, start_led, colors):
    """
    Setze RGB LEDs direkt
    
    Args:
        device: HID device handle
        start_led: Index der ersten LED (0-basiert)
        colors: Liste von (R, G, B) Tupeln
    """
    report = bytearray([0x03])  # Report ID
    report.append(start_led)
    report.append(len(colors))
    report.append(0x00)  # Mode: Direct
    
    for r, g, b in colors[:20]:  # Max 20 LEDs pro Paket
        report.extend([r, g, b])
    
    # Fülle Rest mit 0
    while len(report) < 64:
        report.append(0)
    
    device.write(bytes(report))

# Beispiel: Erste 3 LEDs setzen
colors = [
    (255, 0, 0),    # Rot
    (0, 255, 0),    # Grün
    (0, 0, 255),    # Blau
]
set_rgb_leds(dev, 0, colors)
```

### Effekt-Modi

#### Rainbow-Effekt
```python
def set_rainbow_effect(device, speed=50):
    """
    Aktiviert Rainbow-Effekt
    
    Args:
        device: HID device handle
        speed: Geschwindigkeit 0-255 (höher = schneller)
    """
    report = bytearray([0x03, 0, 0, 0x01])  # Mode: Rainbow
    report.append(speed)
    while len(report) < 64:
        report.append(0)
    device.write(bytes(report))
```

#### Breathing-Effekt
```python
def set_breathing_effect(device, r, g, b, speed=30):
    """
    Aktiviert Breathing-Effekt mit Farbe
    
    Args:
        device: HID device handle
        r, g, b: Farbwerte 0-255
        speed: Geschwindigkeit 0-255
    """
    report = bytearray([0x03, 0, 0, 0x02])  # Mode: Breathing
    report.extend([r, g, b, speed])
    while len(report) < 64:
        report.append(0)
    device.write(bytes(report))
```

#### Statische Farbe
```python
def set_static_color(device, r, g, b):
    """
    Setzt alle LEDs auf eine statische Farbe
    
    Args:
        device: HID device handle
        r, g, b: Farbwerte 0-255
    """
    report = bytearray([0x03, 0, 0, 0x03])  # Mode: Static
    report.extend([r, g, b])
    while len(report) < 64:
        report.append(0)
    device.write(bytes(report))
```

## Integration mit bestehenden Tools

### OpenRGB Unterstützung

Der Fan Hub kann mit OpenRGB integriert werden durch ein Plugin oder Profil.

**OpenRGB Device Definition** (beispielhaft):
```json
{
  "name": "Pico Fan Hub",
  "type": "LED Strip",
  "leds": 60,
  "modes": [
    {
      "name": "Direct",
      "value": 0,
      "flags": ["HAS_PER_LED_COLOR"]
    },
    {
      "name": "Rainbow",
      "value": 1,
      "flags": ["HAS_SPEED"]
    },
    {
      "name": "Breathing",
      "value": 2,
      "flags": ["HAS_MODE_SPECIFIC_COLOR", "HAS_SPEED"]
    }
  ]
}
```

### liquidctl Unterstützung

Für liquidctl-Kompatibilität kann ein Custom-Driver erstellt werden:

```python
# liquidctl driver (vereinfacht)
from liquidctl.driver.usb import UsbHidDriver

class PicoFanHubDriver(UsbHidDriver):
    SUPPORTED_DEVICES = [
        (0x2E8A, 0x1001, 'Pico Fan Hub', {}),
    ]
    
    def set_color(self, channel, mode, colors, speed=50):
        # Implementierung der RGB-Steuerung
        pass
```

## RGB-Lüfter-Spezifikationen

### Standard RGB-Header
- 4-Pin 12V RGB (nicht addressierbar) - **Nicht unterstützt**
- 3-Pin 5V ARGB (addressierbar) - **Unterstützt**

### Pin-Belegung (ARGB)
1. +5V
2. Data
3. GND

### Verkabelung
```
Pico Fan Hub → RGB-Verteiler → Mehrere RGB-Lüfter
```

## Timing-Anforderungen

WS2812B Timing:
- **T0H**: 350ns ± 150ns (0-Bit High-Zeit)
- **T0L**: 800ns ± 150ns (0-Bit Low-Zeit)
- **T1H**: 700ns ± 150ns (1-Bit High-Zeit)
- **T1L**: 600ns ± 150ns (1-Bit Low-Zeit)
- **Reset**: >50µs Low

**Implementierung:**
Die Firmware nutzt PIO (Programmable I/O) des RP2040 für präzises Timing.

## Leistungsbetrachtung

### Stromverbrauch pro LED
- Maximum (Weiß, volle Helligkeit): ~60mA
- Typisch (Farbe, 50%): ~20mA

### Beispiel-Rechnungen

**10 RGB-Lüfter mit je 6 LEDs:**
- LEDs gesamt: 60
- Maximaler Strom: 60 × 60mA = 3.6A @ 5V
- Leistung: 18W

**Empfehlung:**
- Für >10 LEDs: Externe 5V-Versorgung verwenden
- USB kann max. 500mA (USB 2.0) oder 900mA (USB 3.0) liefern
- Helligkeitsbegrenzung in Firmware implementiert (Standard: 50%)

## Firmware-Konfiguration

### Maximale Helligkeit begrenzen
```c
// In firmware/src/rgb.h
#define RGB_MAX_BRIGHTNESS 128  // 0-255, default: 128 (50%)
```

### LED-Anzahl konfigurieren
```c
// In firmware/src/config.h
#define NUM_RGB_LEDS 60  // Anpassen an tatsächliche Anzahl
```

### Effekt-Geschwindigkeit
```c
// In firmware/src/rgb.c
#define RAINBOW_SPEED_DEFAULT 50      // 0-255
#define BREATHING_SPEED_DEFAULT 30    // 0-255
```

## Troubleshooting

### LEDs flackern
- Kürzere Datenleitungen verwenden (< 15cm zum ersten LED)
- Kondensator an 5V-Versorgung erhöhen (1000µF+)
- Serienwiderstand (330-470Ω) am Data-Pin prüfen

### Falsche Farben
- Prüfe LED-Typ (WS2812B vs. SK6812 haben unterschiedliche Farbreihenfolge)
- RGB vs. GRB Order in Firmware konfigurieren

### Keine Reaktion
- Level-Shifter prüfen (3.3V → 5V)
- Verkabelung prüfen (GND, 5V, Data)
- Firmware-Log überprüfen

### Erste LED funktioniert, Rest nicht
- Datenleitung unterbrochen
- Erste LED defekt (überbrücken)
- Stromversorgung unzureichend (Spannungsabfall)

## Erweiterte Features (zukünftig)

- **Temperatur-basierte Farbsteuerung**: LEDs ändern Farbe basierend auf Lüfter-Last
- **Synchronisation**: Sync mit anderen RGB-Geräten
- **Audio-Reaktiv**: LEDs reagieren auf Audio (via zusätzliches Mikrofon)
- **Zonen**: Verschiedene Zonen mit unterschiedlichen Effekten
