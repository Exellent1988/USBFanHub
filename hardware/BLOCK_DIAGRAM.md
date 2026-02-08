# Block-Diagramm: Pico Fan Hub

## System-Übersicht

```
                                    ┌─────────────────────────────────┐
                                    │                                 │
                                    │    12V DC Power Supply          │
                                    │    (External)                   │
                                    │                                 │
                                    └──────────────┬──────────────────┘
                                                   │ 12V
                                                   │
                    ┌──────────────────────────────┼──────────────────────────────┐
                    │                              │                              │
                    │                    ┌─────────▼─────────┐                    │
                    │                    │  F1: 3A Fuse      │                    │
                    │                    │  D1: Verpolschutz │                    │
                    │                    │  D2: TVS Diode    │                    │
                    │                    │  C1: 470µF Filter │                    │
                    │                    └─────────┬─────────┘                    │
                    │                              │                              │
                    │                              ├────────────────┐             │
                    │                              │                │             │
                    │                   ┌──────────▼─────────┐      │             │
                    │                   │  LM2596 Regulator  │      │             │
                    │                   │  12V → 5V @ 3A     │      │             │
                    │                   │  Buck Converter    │      │             │
                    │                   └──────────┬─────────┘      │             │
                    │                              │ 5V             │ 12V         │
                    │                              │                │             │
     ┌──────────────┼──────────────────────────────┼────────────────┤             │
     │              │                              │                │             │
     │              │                   ┌──────────▼─────────┐      │             │
     │              │                   │  Raspberry Pi Pico │      │             │
     │              │                   │  RP2040 MCU        │      │             │
     │   USB ◄──────┤◄─────────────────►│                    │      │             │
     │   Host       │                   │  USB Device Mode   │      │             │
     │              │                   │  HID Interface     │      │             │
     │              │                   │                    │      │             │
     │              │                   │  GPIO 0-5:  PWM    ├──────┤             │
     │              │                   │  GPIO 6-11: TACH   │◄─────┤             │
     │              │                   │  GPIO 16:   RGB    ├──────┤             │
     │              │                   │  GPIO 25:   LED    │      │             │
     │              │                   │                    │      │             │
     │              │                   │  3.3V Output       ├───┐  │             │
     │              │                   └────────────────────┘   │  │             │
     │              │                              │             │  │             │
     │              │                              │             │  │             │
     │              │                   ┌──────────▼─────────┐   │  │             │
     │              │                   │  74LVC245          │   │  │             │
     │              │                   │  Level Shifter     │   │  │             │
     │              │                   │  3.3V → 5V         │   │  │             │
     │              │                   │  (for PWM)         │   │  │             │
     │              │                   │                    │   │  │             │
     │              │                   │  A1-A6 ◄─ GP0-GP5  │   │  │             │
     │              │                   │  B1-B6 ─► PWM Out  ├───┤  │             │
     │              │                   │                    │   │  │             │
     │              │                   │  VccA ◄── 3.3V     │◄──┘  │             │
     │              │                   │  VccB ◄── 5V       │◄─────┤             │
     │              │                   └──────────┬─────────┘      │             │
     │              │                              │ PWM (5V)       │             │
     │              │                              │                │             │
     │              │                   ┌──────────▼─────────┐      │             │
     │              │                   │  Fan Connectors    │      │             │
     │              │                   │  6x Molex KK 4-Pin │      │             │
     │              │                   │                    │      │             │
     │              │                   │  Pin 1: GND        │◄─────┤             │
     │              │                   │  Pin 2: +12V       │◄─────┼─────────────┘
     │              │                   │  Pin 3: TACH       ├──────┤
     │              │                   │  Pin 4: PWM        │◄─────┘
     │              │                   │                    │
     │              │                   │  J2: Fan 1         │
     │              │                   │  J3: Fan 2         │
     │              │                   │  J4: Fan 3         │
     │              │                   │  J5: Fan 4         │
     │              │                   │  J6: Fan 5         │
     │              │                   │  J7: Fan 6         │
     │              │                   └────────────────────┘
     │              │
     │              │                   ┌────────────────────┐
     │              │                   │  Tachometer Input  │
     │              │                   │  Conditioning      │
     │              │                   │                    │
     │              │                   │  R1-R6: 10kΩ       │◄── 3.3V
     │              │                   │  Pull-ups          │
     │              │                   │                    │
     │              │                   │  C5-C10: 100nF     │
     │              │                   │  Filters           │
     │              │                   │                    │
     │              │                   │  Optional:         │
     │              │                   │  74HC14 Schmitt    │
     │              │                   └──────────┬─────────┘
     │              │                              │
     │              └──────────────────────────────┘
     │
     │                                  ┌────────────────────┐
     │                                  │  RGB LED Output    │
     │                                  │                    │
     │                                  │  74LVC1G34         │◄── 3.3V
     │                                  │  Level Shifter     │◄── 5V
     │                                  │  3.3V → 5V         │
     │                                  │                    │
     │                                  │  In  ◄── GPIO16    │
     │                                  │  Out ──► RGB Data  ├──► WS2812B
     │                                  │                    │    LEDs
     │                                  │  R7: 330Ω Series   │
     │                                  │                    │
     │                                  │  J8: 3-Pin Header  │
     │                                  │  Pin 1: GND        │
     └──────────────────────────────────┤  Pin 2: +5V        │
                                        │  Pin 3: DATA       │
                                        └────────────────────┘
```

## Signal-Fluss

### PWM Control Flow

```
Linux Host (sensors, pwm1)
    ↓
USB HID Report (PWM values 0-255)
    ↓
Raspberry Pi Pico (USB HID Handler)
    ↓
PWM Module (25 kHz, Hardware PWM)
    ↓
GPIO 0-5 (3.3V PWM Signal)
    ↓
74LVC245 Level Shifter
    ↓
5V PWM Signal
    ↓
Fan Connector Pin 4
    ↓
PC Fan (4-Pin PWM)
```

### RPM Measurement Flow

```
PC Fan (4-Pin PWM)
    ↓
Fan Connector Pin 3 (Tach Signal)
    ↓
Pull-up Resistor (10kΩ to 3.3V)
    ↓
Filter Capacitor (100nF)
    ↓
Optional: Schmitt Trigger (74HC14)
    ↓
Raspberry Pi Pico GPIO 6-11
    ↓
GPIO Interrupt (Edge Detection)
    ↓
RPM Calculation (every 500ms)
    ↓
USB HID Report (RPM values)
    ↓
Linux Host (sensors, fan1_input)
```

### RGB LED Control Flow

```
Linux Host (pico-fan-ctl rgb rainbow)
    ↓
USB HID Report (RGB Mode & Data)
    ↓
Raspberry Pi Pico (USB HID Handler)
    ↓
RGB Control Module (Effect Processing)
    ↓
PIO State Machine (WS2812 Protocol)
    ↓
GPIO 16 (3.3V Data Signal)
    ↓
74LVC1G34 Level Shifter
    ↓
5V Data Signal
    ↓
330Ω Series Resistor
    ↓
WS2812B LED Strip (Addressable RGB)
```

## Power Distribution

```
External 12V PSU
    │
    ├─► 3A Fuse ─► 12V Rail ─┬─► 6x Fan Connectors (Pin 2)
    │                         │
    │                         └─► LM2596 Buck Converter
    │                                 │
    │                                 ▼
    │                             5V @ 3A ─┬─► RGB LEDs (+5V)
    │                                      │
    │                                      └─► 74LVC245 VccB
    │                                      │
    │                                      └─► 74LVC1G34 VccB
    │
    └─► USB (from PC) ─► Pico VBUS ─► Pico Internal Regulator
                                           │
                                           ▼
                                       3.3V @ 300mA ─┬─► Pico MCU
                                                      │
                                                      ├─► 74LVC245 VccA
                                                      │
                                                      ├─► 74LVC1G34 VccA
                                                      │
                                                      └─► Pull-up Resistors
```

## Data Flow: USB HID Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                       Linux Host                            │
│                                                               │
│  /dev/hidraw0                                                │
│      │                                                        │
│      ├─► Python Driver (pico_fan_hub)                        │
│      │       │                                                │
│      │       ├─► hwmon Bridge (/sys/class/hwmon/hwmonX/)     │
│      │       │       │                                        │
│      │       │       ├─► fan1_input (RPM read-only)          │
│      │       │       ├─► pwm1 (0-255 read/write)             │
│      │       │       └─► ...                                 │
│      │       │                                                │
│      │       └─► CLI Tool (pico-fan-ctl)                     │
│      │               ├─► set-pwm                              │
│      │               ├─► status                               │
│      │               └─► rgb                                  │
│      │                                                        │
│      └─► lm-sensors / fancontrol                             │
│                                                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                        USB Cable
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  Raspberry Pi Pico                           │
│                                                               │
│  USB HID Device (VID:0x2E8A, PID:0x1001)                    │
│      │                                                        │
│      ├─► TinyUSB Stack                                       │
│      │       │                                                │
│      │       ├─► HID Descriptor                              │
│      │       │       ├─► Report 0x01: Fan PWM                │
│      │       │       ├─► Report 0x02: Fan RPM                │
│      │       │       ├─► Report 0x03: RGB Control            │
│      │       │       ├─► Report 0x04: Configuration          │
│      │       │       └─► Report 0x10: Status                 │
│      │       │                                                │
│      │       └─► USB Callbacks                               │
│      │               ├─► GET_REPORT                           │
│      │               └─► SET_REPORT                           │
│      │                                                        │
│      └─► Firmware Modules                                    │
│              ├─► PWM Control (pwm_control.c)                 │
│              ├─► Tachometer (tachometer.c)                   │
│              ├─► RGB Control (rgb_control.c)                 │
│              └─► Main Loop (main.c)                          │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Timing Diagram: PWM Signal

```
25 kHz PWM (40µs period)

Duty Cycle = 0% (Fan Off/Minimum):
PWM ═══════════════════════════════════════

Duty Cycle = 50% (Half Speed):
PWM ████████████████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████████
    |<---- 20µs ---->|<---- 20µs ---->|

Duty Cycle = 100% (Full Speed):
PWM ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁

    |<---------- 40µs period ---------->|
```

## Timing Diagram: Tachometer Signal

```
Fan Speed: 1200 RPM (20 RPS)
Pulses per Revolution: 2

Tachometer Signal (from Fan):
TACH ▁▁██▁▁██▁▁██▁▁██▁▁██▁▁██▁▁██▁▁██▁▁
     |<-- 25ms -->|  (40 pulses/second)

GPIO Interrupt (Rising/Falling Edge):
INT  ↑  ↓  ↑  ↓  ↑  ↓  ↑  ↓  ↑  ↓

RPM Calculation (every 500ms):
  Pulses in 500ms: 20 pulses
  RPM = (20 pulses / 0.5s) / 2 × 60 = 1200 RPM
```

## Timing Diagram: WS2812B RGB Data

```
WS2812B Protocol (800 kHz, 1.25µs per bit)

Bit 0:
DATA █▁▁▁
     |<->| 350ns High
        |<------>| 800ns Low

Bit 1:
DATA ████▁▁
     |<---->| 700ns High
          |<->| 600ns Low

Reset (>50µs Low):
DATA ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁

24-Bit Color (GRB order for WS2812B):
  G[7:0] R[7:0] B[7:0]
  MSB first

Example: Red (255, 0, 0)
  Send: 0x00 (G) → 0xFF (R) → 0x00 (B)
        00000000 11111111 00000000
```

## State Machine: Firmware Main Loop

```
┌──────────────┐
│   INIT       │  Power On / Reset
│              │
│ - GPIO Init  │
│ - PWM Init   │
│ - USB Init   │
│ - Set Safe   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   RUNNING    │◄─────────────────┐
│              │                  │
│ - USB Task   │                  │
│ - Update RPM │                  │
│ - Update RGB │                  │
│ - Watchdog   │                  │
│ - LED Blink  │                  │
└──────┬───────┘                  │
       │                          │
       ├─ USB Activity ───────────┘
       │
       ├─ Timeout (3s) ───┐
       │                  │
       │                  ▼
       │          ┌──────────────┐
       │          │  SAFE MODE   │
       │          │              │
       │          │ - All Fans   │
       │          │   to 100%    │
       │          └──────┬───────┘
       │                 │
       └─────────────────┘
```

## Interrupt Priority

```
Priority 0 (Highest):
  - Watchdog

Priority 1:
  - USB Interrupts

Priority 2:
  - GPIO Interrupts (Tachometer)

Priority 3:
  - PIO Interrupts (RGB)

Priority 4 (Lowest):
  - Timer Interrupts
```

## Memory Map

```
Pico RP2040:
  0x00000000 - 0x00001FFF  Boot ROM (8 KB)
  0x10000000 - 0x1FFFFFFF  Flash (2 MB)
    0x10000000             Firmware Code
    0x10100000             Potential Config Storage
  0x20000000 - 0x20041FFF  SRAM (264 KB)
    0x20000000             Stack
    0x20010000             Heap
    0x20040000             USB Buffers
  0x50000000 - 0x500FFFFF  PIO State Machines
  0x40000000 - 0x4FFFFFFF  Peripherals (GPIO, PWM, etc.)
```

Diese Diagramme helfen beim Verständnis der System-Architektur und können als Referenz beim Hardware-Design in KiCad verwendet werden.
