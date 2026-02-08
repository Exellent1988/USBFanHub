#ifndef PWM_CONTROL_H
#define PWM_CONTROL_H

#include <stdint.h>
#include <stdbool.h>

// PWM-Modul initialisieren
void pwm_control_init(void);

// PWM für einen spezifischen Lüfter setzen
// fan_index: 0-5 (für Lüfter 1-6)
// duty_cycle: 0-255 (0 = 0%, 255 = 100%)
void pwm_control_set_duty(uint8_t fan_index, uint8_t duty_cycle);

// PWM für alle Lüfter setzen
// duties: Array mit 6 Werten (0-255)
void pwm_control_set_all(const uint8_t *duties);

// Aktuellen PWM-Wert auslesen
uint8_t pwm_control_get_duty(uint8_t fan_index);

// Alle PWM-Werte auslesen
void pwm_control_get_all(uint8_t *duties);

// Alle Lüfter auf Default-Wert setzen (für Watchdog/Fehler)
void pwm_control_set_safe_mode(void);

// PWM-Ausgänge deaktivieren (alle Lüfter aus)
void pwm_control_disable_all(void);

#endif // PWM_CONTROL_H
