#ifndef USB_HID_H
#define USB_HID_H

#include <stdint.h>
#include <stdbool.h>

// HID Report IDs
#define HID_REPORT_ID_FAN_PWM      0x01
#define HID_REPORT_ID_FAN_RPM      0x02
#define HID_REPORT_ID_RGB_CONTROL  0x03
#define HID_REPORT_ID_CONFIG       0x04
#define HID_REPORT_ID_STATUS       0x10

// Report-Strukturen

// Report 0x01: Fan PWM Control (8 Bytes)
typedef struct __attribute__((packed)) {
    uint8_t report_id;
    uint8_t fan_pwm[6];
    uint8_t reserved;
} hid_report_fan_pwm_t;

// Report 0x02: Fan RPM Reading (13 Bytes)
typedef struct __attribute__((packed)) {
    uint8_t report_id;
    uint16_t fan_rpm[6];
} hid_report_fan_rpm_t;

// Report 0x03: RGB LED Control (64 Bytes)
typedef struct __attribute__((packed)) {
    uint8_t report_id;
    uint8_t led_start_index;
    uint8_t led_count;
    uint8_t mode;
    uint8_t data[60];
} hid_report_rgb_control_t;

// Report 0x04: Configuration (16 Bytes)
typedef struct __attribute__((packed)) {
    uint8_t report_id;
    uint8_t version_major;
    uint8_t version_minor;
    uint8_t version_patch;
    uint8_t num_fans;
    uint8_t num_rgb_leds;
    uint8_t pwm_frequency_khz;
    uint8_t features;
    uint8_t reserved[8];
} hid_report_config_t;

// Report 0x10: Status Update (16 Bytes)
typedef struct __attribute__((packed)) {
    uint8_t report_id;
    uint8_t status_flags;
    uint8_t error_code;
    uint16_t fan_status[6];
    uint8_t reserved;
} hid_report_status_t;

// Feature-Flags für Config-Report
#define FEATURE_PWM_CONTROL     (1 << 0)
#define FEATURE_RPM_READING     (1 << 1)
#define FEATURE_RGB_CONTROL     (1 << 2)
#define FEATURE_TEMP_SENSOR     (1 << 3)

// Error-Codes
#define ERROR_NONE              0x00
#define ERROR_FAN1_STALLED      0x01
#define ERROR_FAN2_STALLED      0x02
#define ERROR_FAN3_STALLED      0x03
#define ERROR_FAN4_STALLED      0x04
#define ERROR_FAN5_STALLED      0x05
#define ERROR_FAN6_STALLED      0x06
#define ERROR_OVERVOLTAGE       0x10
#define ERROR_UNDERVOLTAGE      0x11
#define ERROR_UNKNOWN           0xFF

// USB HID initialisieren
void usb_hid_init(void);

// USB HID Task (muss regelmäßig aufgerufen werden)
void usb_hid_task(void);

// Feature Report empfangen (wird von TinyUSB aufgerufen)
void usb_hid_receive_report(uint8_t report_id, uint8_t const *buffer, uint16_t bufsize);

// Sendet Status-Report an Host (Input Report)
void usb_hid_send_status_report(void);

// Prüft ob USB bereit ist
bool usb_hid_ready(void);

// Watchdog-Reset (wird aufgerufen bei USB-Kommunikation)
void usb_hid_reset_watchdog(void);

#endif // USB_HID_H
