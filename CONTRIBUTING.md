# Mitwirken am Pico Fan Hub Projekt

Vielen Dank für dein Interesse am Pico Fan Hub Projekt!

## Entwicklungs-Setup

### Firmware-Entwicklung

1. **Pico SDK installieren:**
   ```bash
   cd ~
   git clone https://github.com/raspberrypi/pico-sdk.git
   cd pico-sdk
   git submodule update --init
   export PICO_SDK_PATH=~/pico-sdk
   ```

2. **Build-Tools installieren:**
   ```bash
   sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi
   ```

3. **Firmware bauen:**
   ```bash
   cd firmware
   ./build.sh
   ```

### Linux Software-Entwicklung

1. **Abhängigkeiten installieren:**
   ```bash
   sudo apt install python3-pip python3-hid libhidapi-hidraw0
   ```

2. **Entwicklungs-Installation:**
   ```bash
   cd software/driver
   pip3 install -e .
   ```

3. **Tests ausführen:**
   ```bash
   python3 -m pytest
   ```

## Projekt-Struktur

```
.
├── firmware/               # Pico Firmware (C/C++)
│   ├── src/               # Quellcode
│   ├── include/           # Header-Dateien
│   └── build.sh           # Build-Script
├── software/              # Linux Software
│   └── driver/            # Python hwmon-Driver
├── hardware/              # Hardware-Dokumentation
│   ├── pinout.md          # Pin-Zuweisungen
│   └── schematic_suggestions.md  # KiCad-Vorschläge
├── docs/                  # Dokumentation
└── README.md              # Hauptdokumentation
```

## Code-Richtlinien

### Firmware (C/C++)

- **Stil:** K&R C Style
- **Einrückung:** 4 Spaces
- **Kommentare:** Englisch oder Deutsch
- **Dokumentation:** Doxygen-kompatibel

**Beispiel:**
```c
/**
 * @brief Setzt PWM für einen Lüfter
 * @param fan_index Lüfter-Index (0-5)
 * @param duty_cycle PWM Duty Cycle (0-255)
 */
void pwm_control_set_duty(uint8_t fan_index, uint8_t duty_cycle) {
    if (fan_index >= NUM_FANS) {
        return;
    }
    // Implementierung...
}
```

### Python

- **Stil:** PEP 8
- **Einrückung:** 4 Spaces
- **Type Hints:** Verwenden wo möglich
- **Docstrings:** Google Style

**Beispiel:**
```python
def set_fan_pwm(self, fan_index: int, duty_cycle: int) -> bool:
    """
    Setzt PWM für einen Lüfter.
    
    Args:
        fan_index: Lüfter-Index (0-5)
        duty_cycle: PWM-Wert (0-255)
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if fan_index < 0 or fan_index >= self.num_fans:
        return False
    # Implementierung...
```

## Git Workflow

1. **Fork das Repository**

2. **Erstelle einen Feature-Branch:**
   ```bash
   git checkout -b feature/mein-feature
   ```

3. **Committe deine Änderungen:**
   ```bash
   git add .
   git commit -m "feat(pwm): Neue PWM-Frequenz-Einstellung"
   ```

4. **Push zum Fork:**
   ```bash
   git push origin feature/mein-feature
   ```

5. **Erstelle einen Pull Request**

### Commit-Message-Format

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Neues Feature
- `fix`: Bugfix
- `docs`: Dokumentation
- `style`: Formatierung
- `refactor`: Code-Refactoring
- `test`: Tests
- `chore`: Build-System, Dependencies

**Beispiele:**
```
feat(rgb): Rainbow-Effekt hinzugefügt
fix(tachometer): RPM-Berechnung korrigiert
docs(hardware): Pinout-Dokumentation erweitert
```

## Testing

### Firmware-Tests

Manuelle Tests mit Hardware erforderlich. Test-Checkliste:

- [ ] PWM-Ausgabe mit Oszilloskop messen (25 kHz)
- [ ] Tachometer-Eingang mit verschiedenen Lüftern testen
- [ ] RGB-Ausgabe mit WS2812B-Strip testen
- [ ] USB-Enumeration prüfen (`lsusb`)
- [ ] Alle HID-Reports testen

### Software-Tests

```bash
cd software/driver
python3 -m pytest tests/
```

### Integration-Tests

1. Firmware auf Pico flashen
2. Mit Linux-System verbinden
3. Driver starten
4. Alle CLI-Befehle testen

## Hardware-Tests

Wenn du Hardware-Änderungen vorschlägst:

1. **Simulation:** LTspice oder ähnlich
2. **Breadboard-Prototyp:** Erst testen
3. **Messungen:** Oszilloskop-Screenshots
4. **Dokumentation:** Schaltplan + Erklärung

## Dokumentation

- **Neue Features:** In README.md dokumentieren
- **API-Änderungen:** In docs/usb_protocol.md aktualisieren
- **Hardware:** In hardware/ Ordner dokumentieren
- **Beispiele:** Immer Beispiel-Code bereitstellen

## Pull Request Checklist

Vor dem Einreichen eines Pull Requests:

- [ ] Code kompiliert ohne Warnungen
- [ ] Tests laufen durch
- [ ] Dokumentation aktualisiert
- [ ] Commit-Messages folgen Convention
- [ ] Code-Stil eingehalten
- [ ] Keine unnötigen Dateien committed
- [ ] Feature wurde getestet (Beschreibung im PR)

## Fragen?

Bei Fragen erstelle ein Issue oder kontaktiere die Maintainer.

## Lizenz

Durch deine Beiträge stimmst du zu, dass deine Änderungen unter der gleichen Lizenz wie das Projekt veröffentlicht werden.
