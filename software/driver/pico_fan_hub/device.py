"""
USB HID Kommunikation mit dem Pico Fan Hub
"""

import struct
import time
from typing import List, Optional, Tuple
import hid

# HID Report IDs
REPORT_ID_FAN_PWM = 0x01
REPORT_ID_FAN_RPM = 0x02
REPORT_ID_RGB_CONTROL = 0x03
REPORT_ID_CONFIG = 0x04
REPORT_ID_STATUS = 0x10

# USB VID/PID
USB_VID = 0x2E8A
USB_PID = 0x1001


class PicoFanHub:
    """Interface zum Pico Fan Hub via USB HID"""

    def __init__(self, vendor_id: int = USB_VID, product_id: int = USB_PID):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device: Optional[hid.device] = None
        self.num_fans = 6

    def connect(self) -> bool:
        """Verbindung zum Device herstellen"""
        try:
            self.device = hid.device()
            self.device.open(self.vendor_id, self.product_id)
            self.device.set_nonblocking(True)

            # Konfiguration auslesen
            config = self.get_config()
            if config:
                self.num_fans = config["num_fans"]
                return True
            return False

        except Exception as e:
            print(f"Fehler beim Verbinden: {e}")
            return False

    def disconnect(self):
        """Verbindung trennen"""
        if self.device:
            self.device.close()
            self.device = None

    def is_connected(self) -> bool:
        """Prüfen ob verbunden"""
        return self.device is not None

    def get_feature_report(self, report_id: int, length: int) -> Optional[bytes]:
        """Feature Report vom Device lesen"""
        if not self.device:
            return None

        try:
            # Report mit ID vorbereiten
            data = bytes([report_id] + [0] * (length - 1))
            result = self.device.get_feature_report(report_id, length)
            return bytes(result)
        except Exception as e:
            print(f"Fehler beim Lesen von Report {report_id}: {e}")
            return None

    def send_feature_report(self, data: bytes) -> bool:
        """Feature Report an Device senden"""
        if not self.device:
            return False

        try:
            self.device.send_feature_report(data)
            return True
        except Exception as e:
            print(f"Fehler beim Senden von Report: {e}")
            return False

    def set_fan_pwm(self, fan_index: int, duty_cycle: int) -> bool:
        """
        PWM für einen Lüfter setzen

        Args:
            fan_index: 0-5 (Lüfter 1-6)
            duty_cycle: 0-255 (0% - 100%)
        """
        if fan_index < 0 or fan_index >= self.num_fans:
            return False

        if duty_cycle < 0 or duty_cycle > 255:
            return False

        # Aktuelle Werte auslesen
        current = self.get_all_fan_pwm()
        if current is None:
            return False

        # Wert ändern
        current[fan_index] = duty_cycle

        # Zurückschreiben
        return self.set_all_fan_pwm(current)

    def set_all_fan_pwm(self, duty_cycles: List[int]) -> bool:
        """
        PWM für alle Lüfter setzen

        Args:
            duty_cycles: Liste mit 6 Werten (0-255)
        """
        if len(duty_cycles) != self.num_fans:
            return False

        # Report erstellen (8 Bytes)
        data = struct.pack("B6BB", REPORT_ID_FAN_PWM, *duty_cycles[:6], 0)
        return self.send_feature_report(data)

    def get_all_fan_pwm(self) -> Optional[List[int]]:
        """Alle PWM-Werte auslesen"""
        data = self.get_feature_report(REPORT_ID_FAN_PWM, 8)
        if not data or len(data) < 8:
            return None

        # Report parsen
        values = struct.unpack("B6BB", data)
        return list(values[1:7])

    def get_all_fan_rpm(self) -> Optional[List[int]]:
        """Alle RPM-Werte auslesen"""
        data = self.get_feature_report(REPORT_ID_FAN_RPM, 13)
        if not data or len(data) < 13:
            return None

        # Report parsen (Little Endian uint16)
        values = struct.unpack("<B6H", data)
        return list(values[1:7])

    def get_config(self) -> Optional[dict]:
        """Konfiguration auslesen"""
        data = self.get_feature_report(REPORT_ID_CONFIG, 16)
        if not data or len(data) < 16:
            return None

        # Report parsen
        values = struct.unpack("<BBBBBBBB8s", data)
        return {
            "version": (values[1], values[2], values[3]),
            "num_fans": values[4],
            "num_rgb_leds": values[5],
            "pwm_frequency_khz": values[6],
            "features": values[7],
        }

    def set_rgb_direct(
        self, start_index: int, colors: List[Tuple[int, int, int]]
    ) -> bool:
        """
        RGB LEDs direkt setzen

        Args:
            start_index: Index der ersten LED
            colors: Liste von (R, G, B) Tupeln (max 20)
        """
        if len(colors) > 20:
            colors = colors[:20]

        # Report erstellen (64 Bytes)
        data = bytearray([REPORT_ID_RGB_CONTROL, start_index, len(colors), 0x00])

        for r, g, b in colors:
            data.extend([r, g, b])

        # Rest mit 0 füllen
        while len(data) < 64:
            data.append(0)

        return self.send_feature_report(bytes(data))

    def set_rgb_mode_rainbow(self, speed: int = 50) -> bool:
        """Rainbow-Effekt aktivieren"""
        data = bytearray([REPORT_ID_RGB_CONTROL, 0, 0, 0x01, speed])
        while len(data) < 64:
            data.append(0)
        return self.send_feature_report(bytes(data))

    def set_rgb_mode_breathing(self, r: int, g: int, b: int, speed: int = 30) -> bool:
        """Breathing-Effekt aktivieren"""
        data = bytearray([REPORT_ID_RGB_CONTROL, 0, 0, 0x02, r, g, b, speed])
        while len(data) < 64:
            data.append(0)
        return self.send_feature_report(bytes(data))

    def set_rgb_mode_static(self, r: int, g: int, b: int) -> bool:
        """Statische Farbe setzen"""
        data = bytearray([REPORT_ID_RGB_CONTROL, 0, 0, 0x03, r, g, b])
        while len(data) < 64:
            data.append(0)
        return self.send_feature_report(bytes(data))

    def set_rgb_off(self) -> bool:
        """RGB LEDs ausschalten"""
        data = bytearray([REPORT_ID_RGB_CONTROL, 0, 0, 0x04])
        while len(data) < 64:
            data.append(0)
        return self.send_feature_report(bytes(data))


def find_devices() -> List[dict]:
    """Alle Pico Fan Hub Devices finden"""
    devices = []
    for device_info in hid.enumerate(USB_VID, USB_PID):
        devices.append(device_info)
    return devices
