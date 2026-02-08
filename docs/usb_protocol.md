# USB HID Protokoll

## Übersicht

Der Pico Fan Hub nutzt USB HID (Human Interface Device) für die Kommunikation mit dem Host-System. Dies ermöglicht eine treiberlose Kommunikation unter Linux und anderen Betriebssystemen.

## HID Report Descriptor

Der Fan Hub definiert ein Custom HID Device mit folgenden Reports:

### Feature Reports (bidirektional)

#### Report ID 0x01: Fan PWM Control
**Länge**: 8 Bytes

| Byte | Beschreibung                  | Werte       |
|------|-------------------------------|-------------|
| 0    | Report ID                     | 0x01        |
| 1    | Fan 1 PWM                     | 0-255       |
| 2    | Fan 2 PWM                     | 0-255       |
| 3    | Fan 3 PWM                     | 0-255       |
| 4    | Fan 4 PWM                     | 0-255       |
| 5    | Fan 5 PWM                     | 0-255       |
| 6    | Fan 6 PWM                     | 0-255       |
| 7    | Reserved                      | 0x00        |

**PWM-Werte:**
- 0 = 0% Duty Cycle (Lüfter aus/minimal)
- 255 = 100% Duty Cycle (volle Geschwindigkeit)

#### Report ID 0x02: Fan RPM Reading
**Länge**: 13 Bytes

| Byte  | Beschreibung                  | Werte       |
|-------|-------------------------------|-------------|
| 0     | Report ID                     | 0x02        |
| 1-2   | Fan 1 RPM (Little Endian)     | 0-65535     |
| 3-4   | Fan 2 RPM (Little Endian)     | 0-65535     |
| 5-6   | Fan 3 RPM (Little Endian)     | 0-65535     |
| 7-8   | Fan 4 RPM (Little Endian)     | 0-65535     |
| 9-10  | Fan 5 RPM (Little Endian)     | 0-65535     |
| 11-12 | Fan 6 RPM (Little Endian)     | 0-65535     |

**Hinweis:** RPM-Werte werden automatisch alle 500ms aktualisiert.

#### Report ID 0x03: RGB LED Control
**Länge**: 64 Bytes

| Byte   | Beschreibung                  | Werte       |
|--------|-------------------------------|-------------|
| 0      | Report ID                     | 0x03        |
| 1      | LED Start Index               | 0-255       |
| 2      | LED Count                     | 1-20        |
| 3      | Mode                          | Siehe unten |
| 4-63   | LED Data (RGB × 20 LEDs max)  | RGB-Werte   |

**RGB Mode-Werte:**
- 0x00 = Direct (Direkt RGB-Werte setzen)
- 0x01 = Rainbow
- 0x02 = Breathing
- 0x03 = Static Color
- 0x04 = Off

**LED Data Format:**
Für Mode 0x00 (Direct): Sequenz von RGB-Tripeln
- Byte 4: LED[start] Red
- Byte 5: LED[start] Green
- Byte 6: LED[start] Blue
- Byte 7: LED[start+1] Red
- ...

#### Report ID 0x04: Configuration
**Länge**: 16 Bytes

| Byte  | Beschreibung                  | Werte       |
|-------|-------------------------------|-------------|
| 0     | Report ID                     | 0x04        |
| 1     | Firmware Version Major        | 0-255       |
| 2     | Firmware Version Minor        | 0-255       |
| 3     | Firmware Version Patch        | 0-255       |
| 4     | Number of Fans                | 6           |
| 5     | Number of RGB LEDs            | 0-255       |
| 6     | PWM Frequency (kHz)           | 25          |
| 7     | Features Flags                | Bitfeld     |
| 8-15  | Reserved                      | 0x00        |

**Feature Flags (Byte 7):**
- Bit 0: PWM Control verfügbar
- Bit 1: RPM Reading verfügbar
- Bit 2: RGB Control verfügbar
- Bit 3: Temperature Sensor verfügbar (zukünftig)
- Bit 4-7: Reserved

### Input Reports (Device → Host)

#### Report ID 0x10: Async Status Update
**Länge**: 16 Bytes

Wird automatisch gesendet bei Änderungen oder auf Anfrage.

| Byte  | Beschreibung                  | Werte       |
|-------|-------------------------------|-------------|
| 0     | Report ID                     | 0x10        |
| 1     | Status Flags                  | Bitfeld     |
| 2     | Error Code                    | 0-255       |
| 3-14  | Fan Status (2 Bytes pro Fan)  | RPM         |
| 15    | Reserved                      | 0x00        |

**Status Flags (Byte 1):**
- Bit 0: Fan 1 connected
- Bit 1: Fan 2 connected
- Bit 2: Fan 3 connected
- Bit 3: Fan 4 connected
- Bit 4: Fan 5 connected
- Bit 5: Fan 6 connected
- Bit 6: USB Power OK
- Bit 7: Error condition

**Error Codes (Byte 2):**
- 0x00: No error
- 0x01: Fan 1 stalled
- 0x02: Fan 2 stalled
- 0x03: Fan 3 stalled
- 0x04: Fan 4 stalled
- 0x05: Fan 5 stalled
- 0x06: Fan 6 stalled
- 0x10: Overvoltage
- 0x11: Undervoltage
- 0xFF: Unknown error

## Linux Userspace Zugriff

### HID Device Pfad
```
/dev/hidrawX
```

### Beispiel: PWM setzen mit Python

```python
import struct

# Öffne HID Device
with open('/dev/hidraw0', 'wb+') as dev:
    # Setze alle Lüfter auf 50% (128/255)
    report = struct.pack('BBBBBBBB', 
        0x01,  # Report ID
        128,   # Fan 1
        128,   # Fan 2
        128,   # Fan 3
        128,   # Fan 4
        128,   # Fan 5
        128,   # Fan 6
        0      # Reserved
    )
    dev.write(report)
```

### Beispiel: RPM auslesen mit Python

```python
import struct
import fcntl
import os

# HID Get Feature Request
HIDIOCGFEATURE = 0xC0404807

with open('/dev/hidraw0', 'rb') as dev:
    # Buffer für Report vorbereiten
    buf = bytearray([0x02] + [0]*12)  # Report ID 0x02
    
    # Feature Report lesen
    fcntl.ioctl(dev, HIDIOCGFEATURE, buf)
    
    # RPM-Werte extrahieren
    fan_rpms = struct.unpack('<6H', buf[1:13])
    
    for i, rpm in enumerate(fan_rpms, 1):
        print(f"Fan {i}: {rpm} RPM")
```

## hidraw vs. hwmon

Der Fan Hub kann auf zwei Arten angesprochen werden:

### 1. Direkt via hidraw
- Volle Kontrolle über alle Features
- Direkter Zugriff auf RGB-Steuerung
- Erfordert Root-Rechte oder udev-Regeln

### 2. Via hwmon-Interface (empfohlen)
- Standard Linux-Schnittstelle
- Integration mit lm-sensors
- Automatische Erkennung durch Monitoring-Tools

Die hwmon-Brücke wird durch den Userspace-Treiber bereitgestellt, der hidraw-Zugriff in hwmon-sysfs übersetzt.

## USB Vendor/Product IDs

**Wichtig:** Für Produktion müssen offizielle USB IDs verwendet werden!

**Entwicklung/Test:**
- Vendor ID: 0x2E8A (Raspberry Pi)
- Product ID: 0x1001 (Custom - nicht für Produktion!)
- Device Class: HID (0x03)

Siehe [USB IDs for Free](http://pid.codes/) für Open-Source-freundliche PIDs.

## Polling-Rate

- **Input Reports**: 125 Hz (8ms Intervall)
- **Feature Reports**: On-Demand
- **RPM Update Rate**: 500ms intern

## Power Management

Der Fan Hub unterstützt USB Suspend/Resume:
- Bei Suspend: Alle Lüfter gehen in gespeicherten Zustand
- Bei Resume: Letzter Zustand wird wiederhergestellt
- Default bei Cold-Start: Alle Lüfter auf 100%

## Error Handling

Bei Kommunikationsfehlern:
1. Device sendet Error Report (0x10)
2. Error LED blinkt (falls vorhanden)
3. Lüfter gehen in Safe-Mode (100% oder letzter bekannter guter Zustand)
4. Nach 3 Sekunden ohne Kommunikation: Watchdog aktiviert Safe-Mode
