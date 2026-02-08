"""
Daemon für hwmon-Integration
"""

import sys
import os
import signal
import time
import argparse
from pathlib import Path

from .device import PicoFanHub, find_devices
from .hwmon import HwmonBridge


class FanHubDaemon:
    """Daemon für Pico Fan Hub hwmon-Integration"""

    def __init__(self, sysfs_path: str = "/tmp/pico_fan_hub_hwmon"):
        self.device = PicoFanHub()
        self.bridge = HwmonBridge(self.device, sysfs_path)
        self.running = False

    def start(self):
        """Daemon starten"""
        print("Suche nach Pico Fan Hub...")
        devices = find_devices()

        if not devices:
            print("Kein Pico Fan Hub gefunden!")
            print("Prüfe:")
            print("  - USB-Verbindung")
            print("  - udev-Regeln (siehe README)")
            print("  - lsusb | grep 2e8a:1001")
            return False

        print(f"Gefunden: {len(devices)} Device(s)")

        # Mit erstem Device verbinden
        if not self.device.connect():
            print("Fehler beim Verbinden!")
            return False

        print("Verbunden!")

        # Konfigurations-Info anzeigen
        config = self.device.get_config()
        if config:
            version = ".".join(map(str, config["version"]))
            print(f"Firmware-Version: {version}")
            print(f"Lüfter: {config['num_fans']}")
            print(f"RGB LEDs: {config['num_rgb_leds']}")
            print(f"PWM-Frequenz: {config['pwm_frequency_khz']} kHz")

        # hwmon-Bridge starten
        print(f"Starte hwmon-Bridge in: {self.bridge.sysfs_path}")
        if not self.bridge.start():
            print("Fehler beim Starten der Bridge!")
            return False

        print("hwmon-Bridge läuft!")
        print("")
        print("Verwendung:")
        print(f"  cd {self.bridge.sysfs_path}")
        print("  cat fan1_input       # RPM von Lüfter 1")
        print("  echo 128 > pwm1      # PWM auf 50% setzen")
        print("")
        print("Oder mit lm-sensors:")
        print("  sensors pico_fan_hub")
        print("")
        print("Drücke Ctrl+C zum Beenden...")

        self.running = True
        return True

    def stop(self):
        """Daemon stoppen"""
        print("\nStoppe Daemon...")
        self.running = False
        self.bridge.stop()
        self.device.disconnect()
        print("Beendet.")

    def run(self):
        """Hauptschleife"""
        if not self.start():
            return 1

        # Signal-Handler für sauberes Beenden
        def signal_handler(sig, frame):
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Hauptschleife
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

        return 0


def main():
    """Haupteinstiegspunkt"""
    parser = argparse.ArgumentParser(description="Pico Fan Hub hwmon Daemon")
    parser.add_argument(
        "--sysfs-path",
        default="/tmp/pico_fan_hub_hwmon",
        help="Pfad für sysfs-Interface (Standard: /tmp/pico_fan_hub_hwmon)",
    )
    parser.add_argument("--version", action="version", version="pico-fan-hub 1.0.0")

    args = parser.parse_args()

    # Prüfe ob als Root ausgeführt (für /sys/class/hwmon)
    if args.sysfs_path.startswith("/sys/") and os.geteuid() != 0:
        print("WARNUNG: Für /sys/class/hwmon werden Root-Rechte benötigt!")
        print("Verwende --sysfs-path für Test-Installation oder starte als Root.")
        return 1

    daemon = FanHubDaemon(args.sysfs_path)
    return daemon.run()


if __name__ == "__main__":
    sys.exit(main())
