#ifndef RGB_CONTROL_H
#define RGB_CONTROL_H

#include <stdint.h>
#include <stdbool.h>

// RGB-Farb-Struktur
typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} rgb_color_t;

// RGB-Modi
typedef enum {
    RGB_MODE_DIRECT = 0,    // Direkte RGB-Werte
    RGB_MODE_RAINBOW = 1,   // Rainbow-Effekt
    RGB_MODE_BREATHING = 2, // Breathing-Effekt
    RGB_MODE_STATIC = 3,    // Statische Farbe
    RGB_MODE_OFF = 4        // Aus
} rgb_mode_t;

// RGB-Modul initialisieren
void rgb_control_init(void);

// Einzelne LED setzen
void rgb_control_set_led(uint16_t index, rgb_color_t color);

// Mehrere LEDs setzen
void rgb_control_set_leds(uint16_t start_index, uint16_t count, const rgb_color_t *colors);

// Alle LEDs auf eine Farbe setzen
void rgb_control_set_all(rgb_color_t color);

// LEDs aktualisieren (auf Hardware ausgeben)
void rgb_control_update(void);

// Modus setzen
void rgb_control_set_mode(rgb_mode_t mode);

// Rainbow-Effekt-Geschwindigkeit setzen (0-255)
void rgb_control_set_rainbow_speed(uint8_t speed);

// Breathing-Effekt konfigurieren
void rgb_control_set_breathing(rgb_color_t color, uint8_t speed);

// Statische Farbe setzen
void rgb_control_set_static_color(rgb_color_t color);

// Alle LEDs ausschalten
void rgb_control_clear(void);

// Maximale Helligkeit setzen (0-255)
void rgb_control_set_max_brightness(uint8_t brightness);

// Effekt-Update (sollte periodisch aufgerufen werden)
void rgb_control_process(void);

#endif // RGB_CONTROL_H
