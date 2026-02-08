#include "tachometer.h"
#include "config.h"
#include "hardware/gpio.h"
#include "hardware/irq.h"
#include "hardware/timer.h"
#include "pico/stdlib.h"
#include <string.h>

// Pin-Mapping
static const uint8_t fan_tach_pins[NUM_FANS] = {
    FAN1_TACH_PIN, FAN2_TACH_PIN, FAN3_TACH_PIN,
    FAN4_TACH_PIN, FAN5_TACH_PIN, FAN6_TACH_PIN
};

// Zähler für Impulse
static volatile uint32_t pulse_counts[NUM_FANS] = {0};

// Zeitstempel für letzte Impulse
static volatile uint32_t last_pulse_time[NUM_FANS] = {0};

// Berechnete RPM-Werte
static uint16_t current_rpms[NUM_FANS] = {0};

// Zeitstempel für letzte Messung
static uint32_t last_measurement_time = 0;

// GPIO-Interrupt-Handler
static void gpio_irq_handler(uint gpio, uint32_t events) {
    // Prüfen welcher Lüfter
    for (int i = 0; i < NUM_FANS; i++) {
        if (gpio == fan_tach_pins[i]) {
            // Nur bei fallender Flanke zählen
            if (events & GPIO_IRQ_EDGE_FALL) {
                pulse_counts[i]++;
                last_pulse_time[i] = to_ms_since_boot(get_absolute_time());
            }
            break;
        }
    }
}

void tachometer_init(void) {
    // Für jeden Lüfter GPIO konfigurieren
    for (int i = 0; i < NUM_FANS; i++) {
        uint8_t pin = fan_tach_pins[i];
        
        // GPIO initialisieren
        gpio_init(pin);
        gpio_set_dir(pin, GPIO_IN);
        
        // Pull-up aktivieren (Tachometer ist Open-Collector)
        gpio_pull_up(pin);
        
        // Interrupt für fallende Flanke aktivieren
        gpio_set_irq_enabled_with_callback(
            pin, 
            GPIO_IRQ_EDGE_FALL, 
            true, 
            &gpio_irq_handler
        );
    }
    
    // Alle Zähler und RPMs auf 0 setzen
    memset((void*)pulse_counts, 0, sizeof(pulse_counts));
    memset((void*)last_pulse_time, 0, sizeof(last_pulse_time));
    memset(current_rpms, 0, sizeof(current_rpms));
    
    last_measurement_time = to_ms_since_boot(get_absolute_time());
}

void tachometer_update(void) {
    uint32_t now = to_ms_since_boot(get_absolute_time());
    uint32_t elapsed = now - last_measurement_time;
    
    if (elapsed < TACH_MEASUREMENT_INTERVAL_MS) {
        return;  // Noch nicht Zeit für Update
    }
    
    // Für jeden Lüfter RPM berechnen
    for (int i = 0; i < NUM_FANS; i++) {
        // Pulse-Count atomar lesen und zurücksetzen
        uint32_t irq_status = save_and_disable_interrupts();
        uint32_t pulses = pulse_counts[i];
        pulse_counts[i] = 0;
        uint32_t last_pulse = last_pulse_time[i];
        restore_interrupts(irq_status);
        
        // Prüfen ob Lüfter aktiv (letzer Puls nicht zu alt)
        if (now - last_pulse > TACH_TIMEOUT_MS) {
            current_rpms[i] = 0;  // Lüfter gestoppt oder nicht verbunden
            continue;
        }
        
        // RPM berechnen
        // RPM = (Impulse / Sekunden / TACH_PULSES_PER_REVOLUTION) * 60
        float seconds = (float)elapsed / 1000.0f;
        float rpm = ((float)pulses / seconds / (float)TACH_PULSES_PER_REVOLUTION) * 60.0f;
        
        // Auf uint16_t begrenzen
        if (rpm > 65535.0f) {
            rpm = 65535.0f;
        }
        
        current_rpms[i] = (uint16_t)rpm;
    }
    
    last_measurement_time = now;
}

uint16_t tachometer_get_rpm(uint8_t fan_index) {
    if (fan_index >= NUM_FANS) {
        return 0;
    }
    return current_rpms[fan_index];
}

void tachometer_get_all_rpm(uint16_t *rpms) {
    memcpy(rpms, current_rpms, sizeof(current_rpms));
}

bool tachometer_is_fan_connected(uint8_t fan_index) {
    if (fan_index >= NUM_FANS) {
        return false;
    }
    
    uint32_t now = to_ms_since_boot(get_absolute_time());
    uint32_t irq_status = save_and_disable_interrupts();
    uint32_t last_pulse = last_pulse_time[fan_index];
    restore_interrupts(irq_status);
    
    // Lüfter ist verbunden wenn letzer Puls nicht zu alt ist
    return (now - last_pulse) < TACH_TIMEOUT_MS && current_rpms[fan_index] > 0;
}

bool tachometer_is_fan_stalled(uint8_t fan_index) {
    if (fan_index >= NUM_FANS) {
        return false;
    }
    
    // Lüfter ist blockiert wenn verbunden aber RPM < Minimum
    // (und PWM vermutlich nicht auf 0)
    return tachometer_is_fan_connected(fan_index) && 
           current_rpms[fan_index] < TACH_MIN_RPM;
}

uint8_t tachometer_get_connection_status(void) {
    uint8_t status = 0;
    for (int i = 0; i < NUM_FANS; i++) {
        if (tachometer_is_fan_connected(i)) {
            status |= (1 << i);
        }
    }
    return status;
}

void tachometer_reset_counter(uint8_t fan_index) {
    if (fan_index >= NUM_FANS) {
        return;
    }
    
    uint32_t irq_status = save_and_disable_interrupts();
    pulse_counts[fan_index] = 0;
    last_pulse_time[fan_index] = 0;
    restore_interrupts(irq_status);
    
    current_rpms[fan_index] = 0;
}
