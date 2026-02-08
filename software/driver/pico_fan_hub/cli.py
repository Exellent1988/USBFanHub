"""
CLI-Tool für direkten Zugriff auf Pico Fan Hub
"""

import sys
import argparse
from typing import Optional

from .device import PicoFanHub, find_devices


def cmd_list(args):
    """Liste alle Devices auf"""
    devices = find_devices()

    if not devices:
        print("Keine Pico Fan Hub Devices gefunden.")
        return 1

    print(f"Gefundene Devices: {len(devices)}")
    for i, dev in enumerate(devices):
        print(f"  [{i}] {dev['product_string']} (S/N: {dev['serial_number']})")
        print(f"      Path: {dev['path']}")

    return 0


def cmd_info(args):
    """Zeige Device-Informationen"""
    hub = PicoFanHub()

    if not hub.connect():
        print("Fehler: Konnte nicht verbinden!")
        return 1

    config = hub.get_config()
    if not config:
        print("Fehler: Konnte Konfiguration nicht lesen!")
        hub.disconnect()
        return 1

    version = ".".join(map(str, config["version"]))

    print("Pico Fan Hub Informationen:")
    print(f"  Firmware-Version: {version}")
    print(f"  Anzahl Lüfter:    {config['num_fans']}")
    print(f"  Anzahl RGB LEDs:  {config['num_rgb_leds']}")
    print(f"  PWM-Frequenz:     {config['pwm_frequency_khz']} kHz")
    print(f"  Features:         0x{config['features']:02X}")

    hub.disconnect()
    return 0


def cmd_status(args):
    """Zeige aktuellen Status"""
    hub = PicoFanHub()

    if not hub.connect():
        print("Fehler: Konnte nicht verbinden!")
        return 1

    # RPM-Werte
    rpms = hub.get_all_fan_rpm()
    pwms = hub.get_all_fan_pwm()

    if not rpms or not pwms:
        print("Fehler: Konnte Status nicht lesen!")
        hub.disconnect()
        return 1

    print("Lüfter-Status:")
    print("  Fan  | RPM    | PWM   | Duty")
    print("  -----|--------|-------|------")

    for i in range(6):
        duty_percent = (pwms[i] / 255.0) * 100.0
        status = "OK" if rpms[i] > 0 else "--"
        print(
            f"  {i+1}    | {rpms[i]:5d}  | {pwms[i]:3d}   | {duty_percent:5.1f}% {status}"
        )

    hub.disconnect()
    return 0


def cmd_set_pwm(args):
    """Setze PWM für Lüfter"""
    hub = PicoFanHub()

    if not hub.connect():
        print("Fehler: Konnte nicht verbinden!")
        return 1

    fan_index = args.fan - 1
    duty = args.duty

    if duty < 0 or duty > 255:
        print("Fehler: PWM muss zwischen 0 und 255 liegen!")
        hub.disconnect()
        return 1

    if not hub.set_fan_pwm(fan_index, duty):
        print(f"Fehler: Konnte PWM für Lüfter {args.fan} nicht setzen!")
        hub.disconnect()
        return 1

    duty_percent = (duty / 255.0) * 100.0
    print(f"Lüfter {args.fan}: PWM={duty} ({duty_percent:.1f}%)")

    hub.disconnect()
    return 0


def cmd_set_all_pwm(args):
    """Setze PWM für alle Lüfter"""
    hub = PicoFanHub()

    if not hub.connect():
        print("Fehler: Konnte nicht verbinden!")
        return 1

    duty = args.duty

    if duty < 0 or duty > 255:
        print("Fehler: PWM muss zwischen 0 und 255 liegen!")
        hub.disconnect()
        return 1

    duties = [duty] * 6

    if not hub.set_all_fan_pwm(duties):
        print("Fehler: Konnte PWM nicht setzen!")
        hub.disconnect()
        return 1

    duty_percent = (duty / 255.0) * 100.0
    print(f"Alle Lüfter: PWM={duty} ({duty_percent:.1f}%)")

    hub.disconnect()
    return 0


def cmd_rgb(args):
    """RGB-Steuerung"""
    hub = PicoFanHub()

    if not hub.connect():
        print("Fehler: Konnte nicht verbinden!")
        return 1

    mode = args.mode.lower()

    if mode == "off":
        hub.set_rgb_off()
        print("RGB: Aus")

    elif mode == "rainbow":
        speed = args.speed if args.speed else 50
        hub.set_rgb_mode_rainbow(speed)
        print(f"RGB: Rainbow (Speed={speed})")

    elif mode == "breathing":
        if not args.color:
            print("Fehler: --color benötigt für breathing-Modus (z.B. --color 255,0,0)")
            hub.disconnect()
            return 1

        r, g, b = map(int, args.color.split(","))
        speed = args.speed if args.speed else 30
        hub.set_rgb_mode_breathing(r, g, b, speed)
        print(f"RGB: Breathing ({r},{g},{b}) Speed={speed}")

    elif mode == "static":
        if not args.color:
            print(
                "Fehler: --color benötigt für static-Modus (z.B. --color 255,255,255)"
            )
            hub.disconnect()
            return 1

        r, g, b = map(int, args.color.split(","))
        hub.set_rgb_mode_static(r, g, b)
        print(f"RGB: Static ({r},{g},{b})")

    else:
        print(f"Fehler: Unbekannter Modus '{mode}'")
        print("Verfügbare Modi: off, rainbow, breathing, static")
        hub.disconnect()
        return 1

    hub.disconnect()
    return 0


def main():
    """Haupteinstiegspunkt"""
    parser = argparse.ArgumentParser(
        description="Pico Fan Hub CLI-Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  pico-fan-ctl list                      # Devices auflisten
  pico-fan-ctl info                      # Device-Informationen
  pico-fan-ctl status                    # Status anzeigen
  pico-fan-ctl set-pwm 1 128             # Lüfter 1 auf 50%
  pico-fan-ctl set-all-pwm 255           # Alle Lüfter auf 100%
  pico-fan-ctl rgb rainbow               # Rainbow-Effekt
  pico-fan-ctl rgb breathing --color 255,0,0  # Rotes Breathing
  pico-fan-ctl rgb static --color 0,255,0     # Grün statisch
  pico-fan-ctl rgb off                   # RGB aus
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Befehle")

    # list
    subparsers.add_parser("list", help="Liste alle Devices")

    # info
    subparsers.add_parser("info", help="Zeige Device-Informationen")

    # status
    subparsers.add_parser("status", help="Zeige aktuellen Status")

    # set-pwm
    parser_set_pwm = subparsers.add_parser("set-pwm", help="Setze PWM für einen Lüfter")
    parser_set_pwm.add_argument(
        "fan", type=int, choices=range(1, 7), help="Lüfter-Nummer (1-6)"
    )
    parser_set_pwm.add_argument("duty", type=int, help="PWM-Wert (0-255)")

    # set-all-pwm
    parser_set_all = subparsers.add_parser(
        "set-all-pwm", help="Setze PWM für alle Lüfter"
    )
    parser_set_all.add_argument("duty", type=int, help="PWM-Wert (0-255)")

    # rgb
    parser_rgb = subparsers.add_parser("rgb", help="RGB-Steuerung")
    parser_rgb.add_argument(
        "mode", choices=["off", "rainbow", "breathing", "static"], help="RGB-Modus"
    )
    parser_rgb.add_argument("--color", help="RGB-Farbe als R,G,B (z.B. 255,0,0)")
    parser_rgb.add_argument("--speed", type=int, help="Effekt-Geschwindigkeit (0-255)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Befehl ausführen
    commands = {
        "list": cmd_list,
        "info": cmd_info,
        "status": cmd_status,
        "set-pwm": cmd_set_pwm,
        "set-all-pwm": cmd_set_all_pwm,
        "rgb": cmd_rgb,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
