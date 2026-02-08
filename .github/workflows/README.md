# GitHub Actions Workflows

Dieses Verzeichnis enthält alle CI/CD-Workflows für das Pico Fan Hub Projekt.

## 📋 Übersicht

| Workflow | Trigger | Beschreibung |
|----------|---------|--------------|
| **ci.yml** | Push, PR | Haupt-CI-Pipeline (kombiniert) |
| **firmware-build.yml** | Push, PR, Manual | Baut Pico-Firmware |
| **python-tests.yml** | Push, PR, Manual | Python Tests & Package Build |
| **release.yml** | Git Tag, Manual | Erstellt GitHub Releases |

## 🚀 Workflows im Detail

### CI Workflow (`ci.yml`)

Haupt-Workflow, der alle anderen orchestriert.

**Trigger:**
- Push zu `main`, `develop`, `cursor/**`
- Pull Requests zu `main`, `develop`
- Manuell via GitHub UI

**Jobs:**
- Ruft `firmware-build.yml` auf
- Ruft `python-tests.yml` auf
- Kombiniert Status beider Workflows

**Verwendung:**
```bash
# Automatisch bei Push
git push origin main

# Status prüfen
https://github.com/Exellent1988/USBFanHub/actions
```

### Firmware Build Workflow (`firmware-build.yml`)

Baut die Raspberry Pi Pico Firmware.

**Was wird gebaut:**
- `pico_fan_hub.uf2` - Flashbare UF2-Datei
- `pico_fan_hub.elf` - ELF Binary (mit Debug-Symbolen)
- `pico_fan_hub.bin` - Raw Binary

**Features:**
- ✅ Pico SDK Caching (schnellere Builds)
- ✅ Build-Artefakte als Download
- ✅ Size-Informationen in Summary
- ✅ Versions-Extraktion aus CMakeLists.txt
- ✅ Multi-Format Output (UF2, ELF, BIN)

**Trigger:**
- Änderungen in `firmware/**`
- Push/PR zu main/develop branches
- Manuell

**Artifacts:**
Verfügbar für 90 Tage nach Build:
- Name: `pico-fan-hub-firmware-vX.X.X`
- Enthält: UF2, ELF, BIN Dateien

**Lokal nachbauen:**
```bash
cd firmware
./build.sh
# Oder manuell:
mkdir build && cd build
cmake .. -DPICO_SDK_PATH=~/pico-sdk
make -j$(nproc)
```

### Python Tests Workflow (`python-tests.yml`)

Testet und baut Python-Software.

**Jobs:**

1. **Lint Job:**
   - flake8 (Syntax-Checks)
   - black (Code-Formatierung)
   - mypy (Type-Checking)

2. **Test Job:**
   - Matrix: Python 3.8, 3.9, 3.10, 3.11
   - Unit Tests mit pytest
   - Coverage-Report
   - Installation Test

3. **Build Job:**
   - Erstellt Wheel (`.whl`)
   - Erstellt Source Distribution (`.tar.gz`)

**Features:**
- ✅ Multi-Version Testing
- ✅ Code Coverage
- ✅ Package Build
- ✅ pip Cache für schnellere Builds

**Trigger:**
- Änderungen in `software/**`
- Push/PR zu main/develop branches
- Manuell

**Artifacts:**
- Name: `python-packages`
- Enthält: `.whl` und `.tar.gz` Dateien

**Lokal testen:**
```bash
cd software/driver
pip install -e .
pytest
flake8 pico_fan_hub
black --check pico_fan_hub
```

### Release Workflow (`release.yml`)

Erstellt offizielle GitHub Releases.

**Trigger:**

1. **Automatisch bei Git Tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Manuell via GitHub UI:**
   - Actions → Release → "Run workflow"
   - Version eingeben (z.B. `v1.0.0`)

**Was passiert:**

1. **Build Firmware:**
   - Baut Release-Version
   - Benennt mit Version: `pico_fan_hub_v1.0.0.uf2`

2. **Build Python Package:**
   - Erstellt Wheel und Source Dist
   - Mit korrekter Version aus setup.py

3. **Create Release:**
   - Erstellt GitHub Release
   - Lädt alle Artifacts hoch
   - Generiert Release Notes
   - Veröffentlicht automatisch (kein Draft)

**Release Assets:**
- `pico_fan_hub_vX.X.X.uf2` - Firmware
- `pico_fan_hub_vX.X.X.elf` - Debug Binary
- `pico_fan_hub_vX.X.X.bin` - Raw Binary
- `pico_fan_hub-X.X.X-py3-none-any.whl` - Python Wheel
- `pico-fan-hub-X.X.X.tar.gz` - Python Source

**Release Notes:**
Automatisch generiert mit:
- Version
- Installations-Anleitung
- Feature-Liste
- Changelog-Link
- Bug-Report-Link

**Beispiel Release erstellen:**
```bash
# Version in firmware/CMakeLists.txt und setup.py aktualisieren
git add -u
git commit -m "chore: bump version to 1.0.0"
git tag v1.0.0
git push origin main
git push origin v1.0.0

# Release wird automatisch erstellt
# Assets werden hochgeladen
# Ist sofort verfügbar unter:
# https://github.com/Exellent1988/USBFanHub/releases
```

## 🔧 Konfiguration

### Secrets

Keine Secrets erforderlich für öffentliche Repos!

`GITHUB_TOKEN` wird automatisch bereitgestellt.

Für Private Repos oder zusätzliche Features:
- Settings → Secrets → Actions
- Neue Secrets hinzufügen

### Environment Variables

Alle Workflows nutzen Standard-Environment:
- `PICO_SDK_PATH`: ~/pico-sdk
- `GITHUB_WORKSPACE`: Workspace Root
- `GITHUB_ENV`: Für dynamische Variablen

### Cache-Strategie

**Pico SDK Cache:**
- Key: `${{ runner.os }}-pico-sdk-${{ hashFiles(...) }}`
- Spart ~2-3 Minuten pro Build
- Wird automatisch invalidiert bei SDK-Änderungen

**Python pip Cache:**
- Key: `${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles(...) }}`
- Spart ~1 Minute pro Test-Job
- Pro Python-Version separat

### Matrix Strategy

Python Tests laufen parallel für:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

Jeder Job läuft unabhängig in eigener VM.

## 📊 Status & Badges

Badges für README.md:

```markdown
[![CI](https://github.com/Exellent1988/USBFanHub/actions/workflows/ci.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/ci.yml)
[![Firmware Build](https://github.com/Exellent1988/USBFanHub/actions/workflows/firmware-build.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/firmware-build.yml)
[![Python Tests](https://github.com/Exellent1988/USBFanHub/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Exellent1988/USBFanHub/actions/workflows/python-tests.yml)
```

## 🐛 Troubleshooting

### Build schlägt fehl

**Firmware:**
```
Error: pico_sdk not found
→ Lösung: Cache löschen und neu bauen
```

**Python:**
```
Error: No module named 'hidapi'
→ Lösung: System-Dependencies prüfen (libhidapi)
```

### Artifacts nicht verfügbar

Artifacts werden nach 90 Tagen automatisch gelöscht.
Für längere Aufbewahrung: Release erstellen.

### Workflow läuft nicht

Prüfe:
- [ ] Branch-Name matched Trigger-Pattern?
- [ ] Path-Filter matched geänderte Dateien?
- [ ] Workflow-Datei ist valid YAML?

Validierung:
```bash
# Online YAML Validator
https://www.yamllint.com/

# Oder lokal mit yamllint
yamllint .github/workflows/*.yml
```

## 🔄 Workflow Dependencies

```
ci.yml
  ├── firmware-build.yml
  └── python-tests.yml
      ├── lint
      ├── test (matrix)
      └── build

release.yml
  ├── build-firmware
  ├── build-software
  └── create-release
```

## 📝 Workflow Logs

Logs sind verfügbar unter:
```
https://github.com/Exellent1988/USBFanHub/actions
```

Jeder Job hat:
- Stdout/Stderr Output
- Timing-Informationen
- Annotations bei Fehlern
- Step-by-Step Details

## 🚀 Best Practices

1. **Kleine Commits:** Jeder Push triggert CI
2. **Branch-Protection:** Main-Branch mit CI-Check schützen
3. **Draft PRs:** Für Work-in-Progress ohne CI-Spam
4. **Manual Triggers:** Für Tests ohne Code-Änderung
5. **Artifacts:** Für Testing zwischen Jobs nutzen

## 📚 Weitere Ressourcen

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Pico SDK Docs](https://github.com/raspberrypi/pico-sdk)

## 🤝 Mitwirken

Workflow-Verbesserungen willkommen!

- Neue Test-Cases
- Optimierungen
- Zusätzliche Checks
- Dokumentations-Updates

Siehe [../CONTRIBUTING.md](../CONTRIBUTING.md)
