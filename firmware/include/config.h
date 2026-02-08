#ifndef CONFIG_H
#define CONFIG_H

// ============================================================================
// Hardware-Konfiguration
// ============================================================================

// Anzahl der Lüfter
#define NUM_FANS 6

// Anzahl der RGB LEDs
#define NUM_RGB_LEDS 60

// ============================================================================
// GPIO Pin-Definitionen
// ============================================================================

// PWM-Ausgänge für Lüfter (GPIO 0-5)
#define FAN1_PWM_PIN 0
#define FAN2_PWM_PIN 1
#define FAN3_PWM_PIN 2
#define FAN4_PWM_PIN 3
#define FAN5_PWM_PIN 4
#define FAN6_PWM_PIN 5

// Tachometer-Eingänge (GPIO 6-11)
#define FAN1_TACH_PIN 6
#define FAN2_TACH_PIN 7
#define FAN3_TACH_PIN 8
#define FAN4_TACH_PIN 9
#define FAN5_TACH_PIN 10
#define FAN6_TACH_PIN 11

// RGB LED Data-Pin
#define RGB_DATA_PIN 16

// Status-LEDs
#define STATUS_LED_PIN 25  // Onboard-LED
#define ERROR_LED_PIN 15   // Optionale externe LED

// ============================================================================
// PWM-Konfiguration
// ============================================================================

// PWM-Frequenz für Lüfter in Hz (Standard: 25 kHz)
#define FAN_PWM_FREQUENCY 25000

// PWM-Auflösung (berechnet aus Systemtakt)
// Bei 125 MHz Systemtakt und 25 kHz PWM: 125000000 / 25000 = 5000
#define PWM_WRAP_VALUE 5000

// ============================================================================
// Tachometer-Konfiguration
// ============================================================================

// Impulse pro Umdrehung (Standard: 2 bei den meisten Lüftern)
#define TACH_PULSES_PER_REVOLUTION 2

// Messintervall für RPM-Berechnung in ms
#define TACH_MEASUREMENT_INTERVAL_MS 500

// Timeout für "Lüfter gestoppt" Erkennung in ms
#define TACH_TIMEOUT_MS 2000

// Minimale RPM für "Lüfter läuft" Erkennung
#define TACH_MIN_RPM 100

// ============================================================================
// RGB LED-Konfiguration
// ============================================================================

// Maximale Helligkeit (0-255)
#define RGB_MAX_BRIGHTNESS 128  // 50% für Strombegrenzung

// LED-Typ (RGB vs. GRB Byte-Reihenfolge)
#define RGB_LED_TYPE_GRB 1  // WS2812B verwendet GRB

// DMA-Kanal für RGB
#define RGB_DMA_CHANNEL 0

// ============================================================================
// USB HID-Konfiguration
// ============================================================================

// USB Vendor ID (Raspberry Pi)
#define USB_VID 0x2E8A

// USB Product ID (Custom - nur für Entwicklung!)
#define USB_PID 0x1001

// USB Device-Strings
#define USB_MANUFACTURER "Custom"
#define USB_PRODUCT "Pico Fan Hub"

// HID Report Update-Intervall in ms
#define HID_REPORT_INTERVAL_MS 8  // 125 Hz

// ============================================================================
// Sicherheits-Features
// ============================================================================

// Watchdog-Timeout in ms
#define WATCHDOG_TIMEOUT_MS 3000

// Default PWM bei Fehler/Watchdog (0-255)
#define DEFAULT_SAFE_PWM 255  // Volle Geschwindigkeit im Fehlerfall

// Aktiviere Watchdog
#define ENABLE_WATCHDOG 1

// ============================================================================
// Debug-Optionen
// ============================================================================

// Debug-Output via UART (nur für Entwicklung)
#define DEBUG_ENABLE 0

// LED-Blink-Muster für Statusanzeige
#define STATUS_LED_BLINK_NORMAL_MS 1000
#define STATUS_LED_BLINK_ERROR_MS 250

#endif // CONFIG_H
