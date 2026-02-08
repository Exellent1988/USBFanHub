#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/bootrom.h"
#include "hardware/watchdog.h"
#include "config.h"
#include "pwm_control.h"
#include "tachometer.h"
#include "rgb_control.h"
#include "usb_hid.h"

// Globale Variablen
static uint32_t last_status_led_toggle = 0;
static bool status_led_state = false;
static uint32_t last_tach_update = 0;
static uint32_t last_rgb_update = 0;

// Initialisierung
static void init_hardware(void) {
    // Standard-Initialisierung
    stdio_init_all();
    
    // Status-LED initialisieren
    gpio_init(STATUS_LED_PIN);
    gpio_set_dir(STATUS_LED_PIN, GPIO_OUT);
    gpio_put(STATUS_LED_PIN, 0);
    
    #ifdef ERROR_LED_PIN
    gpio_init(ERROR_LED_PIN);
    gpio_set_dir(ERROR_LED_PIN, GPIO_OUT);
    gpio_put(ERROR_LED_PIN, 0);
    #endif
    
    // Module initialisieren
    pwm_control_init();
    tachometer_init();
    rgb_control_init();
    usb_hid_init();
    
    // Watchdog aktivieren (falls konfiguriert)
    #if ENABLE_WATCHDOG
    watchdog_enable(WATCHDOG_TIMEOUT_MS, 1);
    #endif
}

// Status-LED blinken lassen
static void update_status_led(void) {
    uint32_t now = to_ms_since_boot(get_absolute_time());
    
    if (now - last_status_led_toggle >= STATUS_LED_BLINK_NORMAL_MS) {
        status_led_state = !status_led_state;
        gpio_put(STATUS_LED_PIN, status_led_state);
        last_status_led_toggle = now;
    }
}

// Periodische Updates
static void update_periodic_tasks(void) {
    uint32_t now = to_ms_since_boot(get_absolute_time());
    
    // Tachometer-Update alle 500ms
    if (now - last_tach_update >= TACH_MEASUREMENT_INTERVAL_MS) {
        tachometer_update();
        last_tach_update = now;
    }
    
    // RGB-Effekte Update alle 20ms (50 Hz)
    if (now - last_rgb_update >= 20) {
        rgb_control_process();
        last_rgb_update = now;
    }
}

int main(void) {
    // Hardware initialisieren
    init_hardware();
    
    // Kurze Pause für USB-Enumeration
    sleep_ms(100);
    
    // Alle Lüfter auf 100% starten (sicherer Zustand)
    pwm_control_set_safe_mode();
    
    // Status-LED einmal blinken zur Bestätigung
    gpio_put(STATUS_LED_PIN, 1);
    sleep_ms(200);
    gpio_put(STATUS_LED_PIN, 0);
    sleep_ms(200);
    gpio_put(STATUS_LED_PIN, 1);
    sleep_ms(200);
    gpio_put(STATUS_LED_PIN, 0);
    
    // Hauptschleife
    while (1) {
        // USB HID Task
        usb_hid_task();
        
        // Periodische Updates
        update_periodic_tasks();
        
        // Status-LED Update
        update_status_led();
        
        // Watchdog füttern
        #if ENABLE_WATCHDOG
        watchdog_update();
        #endif
        
        // Kleine Pause um CPU-Last zu reduzieren
        tight_loop_contents();
    }
    
    return 0;
}
