# Quick Start: KiCad Projekt

## Projekt in 5 Minuten öffnen

### 1. Voraussetzungen

- KiCad 6.0 oder neuer installiert
- Grundkenntnisse in KiCad

### 2. Projekt öffnen

```bash
cd hardware/kicad
# In KiCad: File → Open Project
# Wähle: pico_fan_hub.kicad_pro
```

### 3. Schaltplan ansehen

1. Doppelklick auf `.kicad_sch` Datei
2. Oder in KiCad: Schematic Editor öffnen

**Tastenkürzel:**
- `Z` - Zoom to fit
- `M` - Move component
- `E` - Edit component
- `A` - Add symbol
- `W` - Begin wire

### 4. PCB Layout ansehen

1. Doppelklick auf `.kicad_pcb` Datei  
2. Oder in KiCad: PCB Editor öffnen

**Tastenkürzel:**
- `M` - Move footprint
- `R` - Rotate
- `F` - Flip to back side
- `X` - Start routing
- `B` - Fill zones

### 5. 3D-Ansicht

Im PCB Editor:
- View → 3D Viewer
- Oder `Alt+3`

## Symbol Library einbinden

Die Custom Symbols sind bereits im Projekt:

1. Preferences → Manage Symbol Libraries
2. Project Specific Libraries sollte `pico_fan_hub_symbols` enthalten
3. Falls nicht: Add → Wähle `pico_fan_hub_symbols.kicad_sym`

## Footprint Libraries

Benötigte Standard-Libraries:
- `Connector_Molex` (Lüfter-Stecker)
- `Package_SO` (ICs)
- `Package_TO_SOT_SMD` (Regulatoren)
- `Resistor_SMD` (0805)
- `Capacitor_SMD` (0805)

**Raspberry Pi Pico Footprint:**
Wenn nicht vorhanden:
```
https://github.com/ncarandini/KiCad-RP-Pico
```
Oder manuell erstellen (40-Pin Through-Hole Header).

## Erste Schritte

### A. Schaltplan vervollständigen

1. **Komponenten platzieren:**
   - Press `A` für "Add Symbol"
   - Suche nach Komponente
   - Platziere im Schaltplan

2. **Verbindungen:**
   - Press `W` für "Wire"
   - Klicke Start- und Endpunkt
   - Labels hinzufügen mit `L`

3. **Werte zuweisen:**
   - Klicke Komponente
   - Press `E` für Edit
   - Ändere Value (z.B. "10k" für Widerstand)

### B. ERC (Electrical Rules Check)

```
Tools → Electrical Rules Checker
→ Run ERC
→ Fehler beheben
```

Häufige Fehler:
- Power-Pins nicht verbunden
- Input-Pins floating
- Output-Pins kurzgeschlossen

### C. Footprints zuweisen

1. Tools → Assign Footprints
2. Für jedes Symbol Footprint wählen:
   - Resistor → `Resistor_SMD:R_0805`
   - Capacitor → `Capacitor_SMD:C_0805`
   - Pico → `RPi_Pico:RPi_Pico_TH`
   - etc.

### D. PCB Layout starten

1. Tools → Update PCB from Schematic
2. Import alle Komponenten
3. Platziere Komponenten:
   - Pico zentral
   - Power-Komponenten links
   - Lüfter-Stecker rechts/oben
   - RGB-Ausgang unten

### E. Routing

1. **Auto-Routing vorbereiten:**
   - Design Rules → Track Widths definieren
   - Power: 1.5mm
   - Signal: 0.25mm

2. **Manuelles Routing:**
   - Press `X` für Route Track
   - Power-Leitungen zuerst
   - Dann Signale
   - Via mit `V`

3. **Ground Plane:**
   - Add Filled Zone (rechte Toolbar)
   - Wähle GND net
   - Layer: F.Cu und B.Cu
   - Fill both layers

## Checkliste vor Fertigung

- [ ] ERC im Schaltplan: 0 Fehler
- [ ] Alle Footprints zugewiesen
- [ ] DRC im PCB: 0 Fehler
- [ ] 3D-Ansicht prüfen (Kollisionen?)
- [ ] Silkscreen lesbar
- [ ] Mounting Holes vorhanden
- [ ] Bauteil-Referenzen sinnvoll (R1-R6, etc.)
- [ ] Testpunkte platziert
- [ ] Fiducials für Auto-Placement (optional)

## Gerber-Export

1. PCB Editor → File → Plot
2. **Layers auswählen:**
   - [ ] F.Cu
   - [ ] B.Cu
   - [ ] F.SilkS
   - [ ] B.SilkS
   - [ ] F.Mask
   - [ ] B.Mask
   - [ ] Edge.Cuts
   
3. **Options:**
   - [x] Use Protel filename extensions
   - [x] Generate Gerber job file
   - [x] Subtract soldermask from silkscreen
   
4. **Plot**

5. **Generate Drill Files:**
   - Format: Excellon
   - Units: mm
   - Zeros: Suppress leading
   - Generate

6. **Zip alle Gerber-Dateien:**
   ```bash
   cd gerber_output/
   zip pico_fan_hub_gerbers.zip *
   ```

## Stückliste (BOM) exportieren

1. Schematic → Tools → Generate BOM
2. Plugin wählen oder CSV export
3. Enthält:
   - Reference (R1, C1, etc.)
   - Value (10k, 100nF, etc.)
   - Footprint
   - Quantity

## Häufige Probleme

### "Symbol not found"
→ Symbol Library nicht eingebunden
→ Preferences → Manage Symbol Libraries → Add

### "Footprint not found"  
→ Footprint Library nicht eingebunden
→ Preferences → Manage Footprint Libraries → Add

### "DRC Errors: Clearance"
→ Track zu nah an Pad/Track
→ Vergrößere Clearance oder verschiebe Tracks

### "Keine Verbindung zwischen Pads"
→ Luftlinien (Ratsnest) noch sichtbar
→ Routing unvollständig

### "Zone nicht gefüllt"
→ Tools → Fill All Zones (B)
→ Oder: Edit → Undo to Marker → Fill Zones

## Tipps & Tricks

1. **Shortcuts lernen:**
   - `?` im Editor = Zeigt alle Shortcuts

2. **Grid einstellen:**
   - Schaltplan: 50mil (1.27mm)
   - PCB: 0.5mm oder 0.25mm

3. **Backup:**
   - KiCad erstellt automatisch `.bak` Dateien
   - Nutze Git für Versionierung

4. **Design Rules:**
   - Für JLCPCB: min 0.2mm tracks, 0.2mm clearance
   - Für Prototyping: großzügiger (0.3mm)

5. **Component Values im Schaltplan:**
   - Nutze sinnvolle Werte: "10k" nicht "10000"
   - Unit hinzufügen: "100nF", "10uF"

## Weiterführende Ressourcen

- **KiCad Docs:** https://docs.kicad.org/
- **Getting Started:** https://docs.kicad.org/6.0/en/getting_started_in_kicad/
- **PCB Design Tutorial:** https://www.youtube.com/watch?v=... (suche auf YouTube)
- **KiCad Forum:** https://forum.kicad.info/

## Nächste Schritte

Nach dem Projekt-Setup:

1. **Schaltplan detaillieren:**
   - Alle Komponenten platzieren
   - Werte eintragen
   - Annotations aktualisieren (Tools → Annotate Schematic)

2. **Footprints verifizieren:**
   - 3D-Modelle prüfen
   - Pad-Größen für Hand-Löten anpassen (falls nötig)

3. **PCB layouten:**
   - Placement optimieren
   - Critical signals zuerst routen
   - Power planes füllen

4. **Review:**
   - Von jemand anderem prüfen lassen
   - Checklist durchgehen

5. **Fertigen:**
   - Gerber an Hersteller senden
   - Bauteile bestellen
   - Bestücken & Testen

Viel Erfolg! 🎉
