#ifndef TACHOMETER_H
#define TACHOMETER_H

#include <stdint.h>
#include <stdbool.h>

// Tachometer-Modul initialisieren
void tachometer_init(void);

// Aktuelle RPM für einen Lüfter abrufen
// fan_index: 0-5 (für Lüfter 1-6)
// Rückgabe: RPM-Wert (0 = gestoppt oder nicht verbunden)
uint16_t tachometer_get_rpm(uint8_t fan_index);

// Alle RPM-Werte abrufen
// rpms: Array für 6 uint16_t Werte
void tachometer_get_all_rpm(uint16_t *rpms);

// Prüfen ob ein Lüfter angeschlossen ist
bool tachometer_is_fan_connected(uint8_t fan_index);

// Prüfen ob ein Lüfter blockiert ist (stalled)
bool tachometer_is_fan_stalled(uint8_t fan_index);

// Status-Bitfeld für alle Lüfter (Bit 0-5: connected)
uint8_t tachometer_get_connection_status(void);

// Zähler zurücksetzen (z.B. nach Lüfterwechsel)
void tachometer_reset_counter(uint8_t fan_index);

// Periodisches Update (sollte regelmäßig aufgerufen werden)
void tachometer_update(void);

#endif // TACHOMETER_H
