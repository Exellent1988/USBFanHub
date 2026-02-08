#include "pwm_control.h"
#include "config.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"
#include "hardware/clocks.h"
#include <string.h>

// Pin-Mapping
static const uint8_t fan_pwm_pins[NUM_FANS] = {
    FAN1_PWM_PIN, FAN2_PWM_PIN, FAN3_PWM_PIN,
    FAN4_PWM_PIN, FAN5_PWM_PIN, FAN6_PWM_PIN
};

// Aktuelle PWM-Werte (0-255)
static uint8_t current_duty_cycles[NUM_FANS] = {0};

// PWM Slice-Nummern für jeden Lüfter
static uint pwm_slices[NUM_FANS];

void pwm_control_init(void) {
    // Für jeden Lüfter PWM konfigurieren
    for (int i = 0; i < NUM_FANS; i++) {
        uint8_t pin = fan_pwm_pins[i];
        
        // GPIO als PWM konfigurieren
        gpio_set_function(pin, GPIO_FUNC_PWM);
        
        // PWM-Slice für diesen Pin ermitteln
        uint slice_num = pwm_gpio_to_slice_num(pin);
        pwm_slices[i] = slice_num;
        
        // PWM-Konfiguration
        pwm_config config = pwm_get_default_config();
        
        // Frequenz berechnen
        // PWM-Frequenz = Systemtakt / (wrap + 1) / divider
        // Für 25 kHz bei 125 MHz Systemtakt:
        // 125000000 / 25000 = 5000
        float clock_freq = (float)clock_get_hz(clk_sys);
        float divider = clock_freq / (FAN_PWM_FREQUENCY * PWM_WRAP_VALUE);
        
        pwm_config_set_clkdiv(&config, divider);
        pwm_config_set_wrap(&config, PWM_WRAP_VALUE - 1);
        
        // Konfiguration anwenden
        pwm_init(slice_num, &config, false);
        
        // Initial auf 0 setzen
        pwm_set_gpio_level(pin, 0);
        
        // PWM aktivieren
        pwm_set_enabled(slice_num, true);
    }
    
    // Alle Duty Cycles auf 0 initialisieren
    memset(current_duty_cycles, 0, sizeof(current_duty_cycles));
}

void pwm_control_set_duty(uint8_t fan_index, uint8_t duty_cycle) {
    if (fan_index >= NUM_FANS) {
        return;
    }
    
    // Duty Cycle speichern
    current_duty_cycles[fan_index] = duty_cycle;
    
    // Duty Cycle auf PWM-Level umrechnen
    // duty_cycle: 0-255 → level: 0-PWM_WRAP_VALUE
    uint16_t level = ((uint32_t)duty_cycle * PWM_WRAP_VALUE) / 255;
    
    // PWM-Level setzen
    uint8_t pin = fan_pwm_pins[fan_index];
    pwm_set_gpio_level(pin, level);
}

void pwm_control_set_all(const uint8_t *duties) {
    for (int i = 0; i < NUM_FANS; i++) {
        pwm_control_set_duty(i, duties[i]);
    }
}

uint8_t pwm_control_get_duty(uint8_t fan_index) {
    if (fan_index >= NUM_FANS) {
        return 0;
    }
    return current_duty_cycles[fan_index];
}

void pwm_control_get_all(uint8_t *duties) {
    memcpy(duties, current_duty_cycles, NUM_FANS);
}

void pwm_control_set_safe_mode(void) {
    // Alle Lüfter auf DEFAULT_SAFE_PWM setzen
    for (int i = 0; i < NUM_FANS; i++) {
        pwm_control_set_duty(i, DEFAULT_SAFE_PWM);
    }
}

void pwm_control_disable_all(void) {
    // Alle Lüfter stoppen
    for (int i = 0; i < NUM_FANS; i++) {
        pwm_control_set_duty(i, 0);
    }
}
