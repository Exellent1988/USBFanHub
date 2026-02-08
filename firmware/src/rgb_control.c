#include "rgb_control.h"
#include "config.h"
#include "hardware/pio.h"
#include "hardware/clocks.h"
#include "ws2812.pio.h"
#include <string.h>
#include <math.h>

// PIO und State Machine
static PIO pio;
static uint sm;

// LED-Puffer
static rgb_color_t led_buffer[NUM_RGB_LEDS];

// Aktueller Modus und Parameter
static rgb_mode_t current_mode = RGB_MODE_OFF;
static uint8_t max_brightness = RGB_MAX_BRIGHTNESS;
static uint8_t rainbow_speed = 50;
static rgb_color_t breathing_color = {255, 0, 0};
static uint8_t breathing_speed = 30;
static rgb_color_t static_color = {255, 255, 255};

// Animation-State
static uint32_t animation_counter = 0;

// Helfer: Farbe mit Helligkeit begrenzen
static rgb_color_t apply_brightness(rgb_color_t color) {
    rgb_color_t result;
    result.r = ((uint32_t)color.r * max_brightness) / 255;
    result.g = ((uint32_t)color.g * max_brightness) / 255;
    result.b = ((uint32_t)color.b * max_brightness) / 255;
    return result;
}

// Helfer: HSV zu RGB
static rgb_color_t hsv_to_rgb(uint16_t hue, uint8_t sat, uint8_t val) {
    rgb_color_t rgb;
    uint8_t region, remainder, p, q, t;

    if (sat == 0) {
        rgb.r = val;
        rgb.g = val;
        rgb.b = val;
        return rgb;
    }

    region = hue / 43;
    remainder = (hue - (region * 43)) * 6;

    p = (val * (255 - sat)) >> 8;
    q = (val * (255 - ((sat * remainder) >> 8))) >> 8;
    t = (val * (255 - ((sat * (255 - remainder)) >> 8))) >> 8;

    switch (region) {
        case 0:  rgb.r = val; rgb.g = t;   rgb.b = p;   break;
        case 1:  rgb.r = q;   rgb.g = val; rgb.b = p;   break;
        case 2:  rgb.r = p;   rgb.g = val; rgb.b = t;   break;
        case 3:  rgb.r = p;   rgb.g = q;   rgb.b = val; break;
        case 4:  rgb.r = t;   rgb.g = p;   rgb.b = val; break;
        default: rgb.r = val; rgb.g = p;   rgb.b = q;   break;
    }

    return rgb;
}

void rgb_control_init(void) {
    // PIO-Programm laden
    pio = pio0;
    uint offset = pio_add_program(pio, &ws2812_program);
    sm = pio_claim_unused_sm(pio, true);
    
    // WS2812 initialisieren (800 kHz)
    ws2812_program_init(pio, sm, offset, RGB_DATA_PIN, 800000);
    
    // LED-Puffer auf 0 initialisieren
    memset(led_buffer, 0, sizeof(led_buffer));
    
    // Initialer Update (alle LEDs aus)
    rgb_control_clear();
}

void rgb_control_set_led(uint16_t index, rgb_color_t color) {
    if (index >= NUM_RGB_LEDS) {
        return;
    }
    led_buffer[index] = color;
}

void rgb_control_set_leds(uint16_t start_index, uint16_t count, const rgb_color_t *colors) {
    if (start_index >= NUM_RGB_LEDS) {
        return;
    }
    
    uint16_t end = start_index + count;
    if (end > NUM_RGB_LEDS) {
        end = NUM_RGB_LEDS;
    }
    
    for (uint16_t i = start_index; i < end; i++) {
        led_buffer[i] = colors[i - start_index];
    }
}

void rgb_control_set_all(rgb_color_t color) {
    for (int i = 0; i < NUM_RGB_LEDS; i++) {
        led_buffer[i] = color;
    }
}

void rgb_control_update(void) {
    // Alle LEDs an PIO senden
    for (int i = 0; i < NUM_RGB_LEDS; i++) {
        rgb_color_t c = apply_brightness(led_buffer[i]);
        
        #if RGB_LED_TYPE_GRB
        // GRB-Reihenfolge für WS2812B
        uint32_t pixel = ((uint32_t)c.g << 16) | ((uint32_t)c.r << 8) | (uint32_t)c.b;
        #else
        // RGB-Reihenfolge
        uint32_t pixel = ((uint32_t)c.r << 16) | ((uint32_t)c.g << 8) | (uint32_t)c.b;
        #endif
        
        pio_sm_put_blocking(pio, sm, pixel << 8u);
    }
}

void rgb_control_set_mode(rgb_mode_t mode) {
    current_mode = mode;
    animation_counter = 0;
}

void rgb_control_set_rainbow_speed(uint8_t speed) {
    rainbow_speed = speed;
}

void rgb_control_set_breathing(rgb_color_t color, uint8_t speed) {
    breathing_color = color;
    breathing_speed = speed;
}

void rgb_control_set_static_color(rgb_color_t color) {
    static_color = color;
    rgb_control_set_all(color);
}

void rgb_control_clear(void) {
    rgb_color_t black = {0, 0, 0};
    rgb_control_set_all(black);
    rgb_control_update();
}

void rgb_control_set_max_brightness(uint8_t brightness) {
    max_brightness = brightness;
}

void rgb_control_process(void) {
    switch (current_mode) {
        case RGB_MODE_DIRECT:
            // Bei Direct-Mode muss der Host rgb_control_update() aufrufen
            break;
            
        case RGB_MODE_RAINBOW: {
            // Rainbow-Effekt
            animation_counter += rainbow_speed;
            uint16_t hue_offset = (animation_counter >> 8) % 256;
            
            for (int i = 0; i < NUM_RGB_LEDS; i++) {
                uint16_t hue = (hue_offset + (i * 256 / NUM_RGB_LEDS)) % 256;
                led_buffer[i] = hsv_to_rgb(hue, 255, 255);
            }
            rgb_control_update();
            break;
        }
        
        case RGB_MODE_BREATHING: {
            // Breathing-Effekt (Sinus-basiert)
            animation_counter += breathing_speed;
            float phase = (animation_counter % 10000) / 10000.0f;
            float brightness = (sinf(phase * 2.0f * 3.14159f) + 1.0f) / 2.0f;
            
            rgb_color_t color;
            color.r = (uint8_t)(breathing_color.r * brightness);
            color.g = (uint8_t)(breathing_color.g * brightness);
            color.b = (uint8_t)(breathing_color.b * brightness);
            
            rgb_control_set_all(color);
            rgb_control_update();
            break;
        }
        
        case RGB_MODE_STATIC:
            // Statische Farbe (nur einmal setzen)
            if (animation_counter == 0) {
                rgb_control_set_all(static_color);
                rgb_control_update();
                animation_counter = 1;
            }
            break;
            
        case RGB_MODE_OFF:
            // Aus (nur einmal setzen)
            if (animation_counter == 0) {
                rgb_control_clear();
                animation_counter = 1;
            }
            break;
    }
}
