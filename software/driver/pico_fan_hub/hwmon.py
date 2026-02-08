"""
hwmon-Bridge: Stellt sysfs-Interface bereit
"""

import os
import time
import threading
from pathlib import Path
from typing import Optional

from .device import PicoFanHub


class HwmonBridge:
    """
    Erstellt ein hwmon-kompatibles sysfs-Interface
    
    Verwendet /sys/class/hwmon/hwmonX/ Struktur:
    - fanN_input: RPM-Werte (read-only)
    - pwmN: PWM-Werte 0-255 (read-write)
    - pwmN_enable: PWM-Modus (1=manual, 2=auto)
    - name: Device-Name
    """
    
    def __init__(self, device: PicoFanHub, sysfs_path: str = "/sys/class/hwmon/pico_fan_hub"):
        self.device = device
        self.sysfs_path = Path(sysfs_path)
        self.update_interval = 2.0  # Sekunden
        self.running = False
        self.update_thread: Optional[threading.Thread] = None
        
        # Cache für Werte
        self.cached_rpms = [0] * 6
        self.cached_pwms = [255] * 6
        
    def create_sysfs_structure(self) -> bool:
        """Erstellt die sysfs-Verzeichnisstruktur"""
        try:
            self.sysfs_path.mkdir(parents=True, exist_ok=True)
            
            # Device-Name
            (self.sysfs_path / "name").write_text("pico_fan_hub\n")
            
            # Für jeden Lüfter
            for i in range(1, 7):
                # Fan RPM (read-only)
                (self.sysfs_path / f"fan{i}_input").write_text("0\n")
                (self.sysfs_path / f"fan{i}_label").write_text(f"Fan {i}\n")
                
                # PWM (read-write)
                (self.sysfs_path / f"pwm{i}").write_text("255\n")
                (self.sysfs_path / f"pwm{i}_enable").write_text("1\n")  # 1=manual
                
            return True
            
        except Exception as e:
            print(f"Fehler beim Erstellen der sysfs-Struktur: {e}")
            return False
    
    def update_sysfs_values(self):
        """Aktualisiert die sysfs-Werte aus dem Device"""
        if not self.device.is_connected():
            return
        
        # RPM-Werte auslesen
        rpms = self.device.get_all_fan_rpm()
        if rpms:
            self.cached_rpms = rpms
            for i, rpm in enumerate(rpms, start=1):
                try:
                    (self.sysfs_path / f"fan{i}_input").write_text(f"{rpm}\n")
                except Exception:
                    pass
        
        # PWM-Werte auslesen
        pwms = self.device.get_all_fan_pwm()
        if pwms:
            self.cached_pwms = pwms
            for i, pwm in enumerate(pwms, start=1):
                try:
                    (self.sysfs_path / f"pwm{i}").write_text(f"{pwm}\n")
                except Exception:
                    pass
    
    def read_pwm_from_sysfs(self, fan_index: int) -> int:
        """Liest PWM-Wert aus sysfs"""
        try:
            value = (self.sysfs_path / f"pwm{fan_index + 1}").read_text().strip()
            return int(value)
        except Exception:
            return self.cached_pwms[fan_index]
    
    def write_pwm_to_device(self, fan_index: int, value: int):
        """Schreibt PWM-Wert zum Device"""
        if self.device.is_connected():
            self.device.set_fan_pwm(fan_index, value)
            self.cached_pwms[fan_index] = value
    
    def monitor_sysfs_changes(self):
        """Überwacht sysfs auf Änderungen und schreibt zum Device"""
        while self.running:
            for i in range(6):
                try:
                    # Aktuellen Wert aus sysfs lesen
                    current = self.read_pwm_from_sysfs(i)
                    
                    # Wenn geändert, zum Device schreiben
                    if current != self.cached_pwms[i]:
                        self.write_pwm_to_device(i, current)
                        
                except Exception:
                    pass
            
            time.sleep(0.1)  # 10 Hz Polling
    
    def update_loop(self):
        """Haupt-Update-Loop"""
        while self.running:
            self.update_sysfs_values()
            time.sleep(self.update_interval)
    
    def start(self):
        """Startet die Bridge"""
        if not self.device.is_connected():
            if not self.device.connect():
                return False
        
        if not self.create_sysfs_structure():
            return False
        
        self.running = True
        
        # Update-Thread starten
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
        # Monitor-Thread starten
        self.monitor_thread = threading.Thread(target=self.monitor_sysfs_changes, daemon=True)
        self.monitor_thread.start()
        
        return True
    
    def stop(self):
        """Stoppt die Bridge"""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=5.0)
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5.0)
