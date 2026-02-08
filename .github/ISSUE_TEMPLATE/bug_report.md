---
name: Bug Report
about: Melde einen Bug um uns zu helfen besser zu werden
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 Bug-Beschreibung

Eine klare und präzise Beschreibung des Bugs.

## 🔄 Reproduzieren

Schritte um das Verhalten zu reproduzieren:

1. Gehe zu '...'
2. Klicke auf '....'
3. Scrolle runter zu '....'
4. Siehe Fehler

## ✅ Erwartetes Verhalten

Eine klare und präzise Beschreibung was du erwartet hast.

## 📸 Screenshots

Falls relevant, füge Screenshots hinzu um das Problem zu erklären.

## 🖥️ System-Information

**Hardware:**
- Raspberry Pi Pico: [ja/nein]
- Lüfter-Typ: [z.B. Noctua NF-A12x25]
- RGB LEDs: [WS2812B, Anzahl]

**Software:**
- OS: [z.B. Ubuntu 22.04]
- Python Version: [z.B. 3.10.5]
- Firmware Version: [z.B. v1.0.0]
- Driver Version: [z.B. 1.0.0]

**Komponente:**
- [ ] Firmware (Pico)
- [ ] Python Driver
- [ ] CLI Tool
- [ ] Hardware
- [ ] Dokumentation

## 📋 Logs

```
Füge relevante Logs hier ein
```

**Firmware Logs:**
```
# Falls DEBUG aktiviert
```

**Python Logs:**
```bash
# Output von:
pico-fan-ctl status
# oder
python -m pico_fan_hub.cli status
```

**USB Logs:**
```bash
# Output von:
lsusb | grep 2e8a
dmesg | tail -20
```

## 🔍 Zusätzlicher Kontext

Weitere Informationen zum Problem.

## ✅ Checkliste

- [ ] Ich habe die Dokumentation gelesen
- [ ] Ich habe nach ähnlichen Issues gesucht
- [ ] Ich habe die neueste Version getestet
- [ ] Ich kann das Problem reproduzieren
