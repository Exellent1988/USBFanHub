# Pico Fan Hub - Linux Driver

Userspace-Treiber für hwmon-Integration des Pico Fan Hub.

## Installation

### Abhängigkeiten installieren

```bash
sudo apt install python3-pip python3-hid libhidapi-hidraw0
```

### Driver installieren

```bash
cd software/driver
pip3 install -e .
```

### udev-Regeln einrichten

Erstelle `/etc/udev/rules.d/99-pico-fan-hub.rules`:

```
# Pico Fan Hub
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="1001", MODE="0666", GROUP="plugdev"
```

Regeln neu laden:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Verwendung

### Daemon starten (hwmon-Integration)

```bash
# Testinstallation (kein Root erforderlich)
pico-fan-hub --sysfs-path /tmp/pico_fan_hub_hwmon
```

Der Daemon erstellt ein hwmon-kompatibles Interface:

```bash
cd /tmp/pico_fan_hub_hwmon

# RPM auslesen
cat fan1_input

# PWM setzen (0-255)
echo 128 > pwm1  # 50%
echo 255 > pwm1  # 100%
echo 0 > pwm1    # 0%
```

### CLI-Tool verwenden

#### Device-Informationen

```bash
# Devices auflisten
pico-fan-ctl list

# Konfigurations-Info
pico-fan-ctl info

# Aktuellen Status anzeigen
pico-fan-ctl status
```

Ausgabe-Beispiel:

```
Lüfter-Status:
  Fan  | RPM    | PWM   | Duty
  -----|--------|-------|------
  1    |  1234  | 128   |  50.0% OK
  2    |  1180  | 128   |  50.0% OK
  3    |  1256  | 128   |  50.0% OK
  4    |     0  | 0     |   0.0% --
  5    |     0  | 0     |   0.0% --
  6    |     0  | 0     |   0.0% --
```

#### PWM-Steuerung

```bash
# Einzelnen Lüfter steuern
pico-fan-ctl set-pwm 1 128    # Lüfter 1 auf 50%
pico-fan-ctl set-pwm 1 255    # Lüfter 1 auf 100%
pico-fan-ctl set-pwm 1 64     # Lüfter 1 auf 25%

# Alle Lüfter gleichzeitig
pico-fan-ctl set-all-pwm 128  # Alle auf 50%
```

**PWM-Werte:**
- 0 = 0% (Minimum/Aus)
- 128 = 50%
- 192 = 75%
- 255 = 100% (Maximum)

#### RGB-Steuerung

```bash
# RGB ausschalten
pico-fan-ctl rgb off

# Rainbow-Effekt
pico-fan-ctl rgb rainbow
pico-fan-ctl rgb rainbow --speed 100  # Schneller

# Breathing-Effekt
pico-fan-ctl rgb breathing --color 255,0,0          # Rot
pico-fan-ctl rgb breathing --color 0,0,255 --speed 50  # Blau, langsam

# Statische Farbe
pico-fan-ctl rgb static --color 255,255,255  # Weiß
pico-fan-ctl rgb static --color 255,0,255    # Magenta
pico-fan-ctl rgb static --color 0,255,0      # Grün
```

**Farb-Format:** R,G,B mit Werten 0-255

## Integration mit lm-sensors

Wenn der Daemon in `/sys/class/hwmon` läuft (Root erforderlich):

```bash
# Als Root starten
sudo pico-fan-hub --sysfs-path /sys/class/hwmon/hwmon9
```

Dann mit lm-sensors verwenden:

```bash
sensors pico_fan_hub
```

Ausgabe:

```
pico_fan_hub-hid-0-1
Adapter: HID adapter
Fan 1:       1234 RPM
Fan 2:       1180 RPM
Fan 3:       1256 RPM
Fan 4:          0 RPM
Fan 5:          0 RPM
Fan 6:          0 RPM
```

## Systemd-Service (optional)

Erstelle `/etc/systemd/system/pico-fan-hub.service`:

```ini
[Unit]
Description=Pico Fan Hub Daemon
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/local/bin/pico-fan-hub --sysfs-path /sys/class/hwmon/hwmon9
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Service aktivieren:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pico-fan-hub
sudo systemctl start pico-fan-hub
```

## Python-API

Direkter Zugriff via Python:

```python
from pico_fan_hub import PicoFanHub

# Verbinden
hub = PicoFanHub()
hub.connect()

# Lüfter steuern
hub.set_fan_pwm(0, 128)  # Lüfter 1 auf 50%
hub.set_all_fan_pwm([255, 255, 128, 64, 0, 0])

# Status auslesen
rpms = hub.get_all_fan_rpm()
pwms = hub.get_all_fan_pwm()
config = hub.get_config()

print(f"Lüfter 1: {rpms[0]} RPM @ PWM {pwms[0]}")
print(f"Firmware: {config['version']}")

# RGB steuern
hub.set_rgb_mode_rainbow(speed=50)
hub.set_rgb_mode_breathing(255, 0, 0, speed=30)
hub.set_rgb_mode_static(0, 255, 0)
hub.set_rgb_off()

# Direkte RGB-Kontrolle
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Rot, Grün, Blau
hub.set_rgb_direct(0, colors)

# Trennen
hub.disconnect()
```

## Troubleshooting

### "Kein Pico Fan Hub gefunden"

1. Prüfe USB-Verbindung:
   ```bash
   lsusb | grep 2e8a:1001
   ```

2. Prüfe hidraw-Devices:
   ```bash
   ls -la /dev/hidraw*
   ```

3. Prüfe udev-Regeln:
   ```bash
   sudo udevadm info /dev/hidraw0 | grep ID_VENDOR_ID
   ```

### "Permission denied"

1. Stelle sicher dass udev-Regeln aktiv sind
2. Füge Benutzer zur `plugdev`-Gruppe hinzu:
   ```bash
   sudo usermod -a -G plugdev $USER
   ```
   Dann neu anmelden!

### "Module 'hid' not found"

Installiere hidapi:
```bash
pip3 install hidapi
```

Oder system-weit:
```bash
sudo apt install python3-hid
```

## Lizenz

Siehe [../../LICENSE](../../LICENSE)
