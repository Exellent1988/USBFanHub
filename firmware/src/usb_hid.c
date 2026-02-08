#include "usb_hid.h"
#include "config.h"
#include "pwm_control.h"
#include "tachometer.h"
#include "rgb_control.h"
#include "tusb.h"
#include "hardware/watchdog.h"
#include <string.h>

// Watchdog-Timer
static uint32_t last_usb_activity = 0;

// Status-Variablen
static uint8_t current_error_code = ERROR_NONE;

void usb_hid_init(void) {
    // TinyUSB initialisieren
    tusb_init();
    
    last_usb_activity = to_ms_since_boot(get_absolute_time());
}

void usb_hid_task(void) {
    // TinyUSB Task
    tud_task();
    
    // Watchdog-Prüfung
    #if ENABLE_WATCHDOG
    uint32_t now = to_ms_since_boot(get_absolute_time());
    if (now - last_usb_activity > WATCHDOG_TIMEOUT_MS) {
        // Keine USB-Kommunikation seit Timeout → Safe Mode
        pwm_control_set_safe_mode();
        // Timer zurücksetzen um nicht dauerhaft zu triggern
        last_usb_activity = now - WATCHDOG_TIMEOUT_MS + 1000;
    }
    #endif
}

void usb_hid_reset_watchdog(void) {
    last_usb_activity = to_ms_since_boot(get_absolute_time());
}

bool usb_hid_ready(void) {
    return tud_hid_ready();
}

// TinyUSB Callback: GET_REPORT
uint16_t tud_hid_get_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t *buffer, uint16_t reqlen) {
    (void)instance;
    
    usb_hid_reset_watchdog();
    
    if (report_type != HID_REPORT_TYPE_FEATURE) {
        return 0;
    }
    
    switch (report_id) {
        case HID_REPORT_ID_FAN_PWM: {
            // PWM-Werte zurückgeben
            hid_report_fan_pwm_t *report = (hid_report_fan_pwm_t *)buffer;
            report->report_id = HID_REPORT_ID_FAN_PWM;
            pwm_control_get_all(report->fan_pwm);
            report->reserved = 0;
            return sizeof(hid_report_fan_pwm_t);
        }
        
        case HID_REPORT_ID_FAN_RPM: {
            // RPM-Werte zurückgeben
            hid_report_fan_rpm_t *report = (hid_report_fan_rpm_t *)buffer;
            report->report_id = HID_REPORT_ID_FAN_RPM;
            tachometer_get_all_rpm(report->fan_rpm);
            return sizeof(hid_report_fan_rpm_t);
        }
        
        case HID_REPORT_ID_CONFIG: {
            // Konfigurations-Informationen zurückgeben
            hid_report_config_t *report = (hid_report_config_t *)buffer;
            report->report_id = HID_REPORT_ID_CONFIG;
            report->version_major = PICO_FAN_HUB_VERSION_MAJOR;
            report->version_minor = PICO_FAN_HUB_VERSION_MINOR;
            report->version_patch = PICO_FAN_HUB_VERSION_PATCH;
            report->num_fans = NUM_FANS;
            report->num_rgb_leds = NUM_RGB_LEDS;
            report->pwm_frequency_khz = FAN_PWM_FREQUENCY / 1000;
            report->features = FEATURE_PWM_CONTROL | FEATURE_RPM_READING | FEATURE_RGB_CONTROL;
            memset(report->reserved, 0, sizeof(report->reserved));
            return sizeof(hid_report_config_t);
        }
        
        default:
            return 0;
    }
}

// TinyUSB Callback: SET_REPORT
void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t const *buffer, uint16_t bufsize) {
    (void)instance;
    
    usb_hid_reset_watchdog();
    
    if (report_type != HID_REPORT_TYPE_FEATURE) {
        return;
    }
    
    switch (report_id) {
        case HID_REPORT_ID_FAN_PWM: {
            // PWM-Werte setzen
            if (bufsize >= sizeof(hid_report_fan_pwm_t)) {
                const hid_report_fan_pwm_t *report = (const hid_report_fan_pwm_t *)buffer;
                pwm_control_set_all(report->fan_pwm);
            }
            break;
        }
        
        case HID_REPORT_ID_RGB_CONTROL: {
            // RGB-Steuerung
            if (bufsize >= sizeof(hid_report_rgb_control_t)) {
                const hid_report_rgb_control_t *report = (const hid_report_rgb_control_t *)buffer;
                
                switch (report->mode) {
                    case RGB_MODE_DIRECT: {
                        // Direkte RGB-Werte setzen
                        rgb_control_set_mode(RGB_MODE_DIRECT);
                        
                        uint8_t led_count = report->led_count;
                        if (led_count > 20) led_count = 20;  // Max 20 LEDs pro Paket
                        
                        for (int i = 0; i < led_count; i++) {
                            rgb_color_t color;
                            color.r = report->data[i * 3 + 0];
                            color.g = report->data[i * 3 + 1];
                            color.b = report->data[i * 3 + 2];
                            rgb_control_set_led(report->led_start_index + i, color);
                        }
                        rgb_control_update();
                        break;
                    }
                    
                    case RGB_MODE_RAINBOW: {
                        rgb_control_set_mode(RGB_MODE_RAINBOW);
                        if (bufsize > 4) {
                            rgb_control_set_rainbow_speed(report->data[0]);
                        }
                        break;
                    }
                    
                    case RGB_MODE_BREATHING: {
                        rgb_control_set_mode(RGB_MODE_BREATHING);
                        if (bufsize >= 7) {
                            rgb_color_t color = {
                                report->data[0],
                                report->data[1],
                                report->data[2]
                            };
                            rgb_control_set_breathing(color, report->data[3]);
                        }
                        break;
                    }
                    
                    case RGB_MODE_STATIC: {
                        rgb_control_set_mode(RGB_MODE_STATIC);
                        if (bufsize >= 7) {
                            rgb_color_t color = {
                                report->data[0],
                                report->data[1],
                                report->data[2]
                            };
                            rgb_control_set_static_color(color);
                        }
                        break;
                    }
                    
                    case RGB_MODE_OFF: {
                        rgb_control_set_mode(RGB_MODE_OFF);
                        rgb_control_clear();
                        break;
                    }
                }
            }
            break;
        }
    }
}

void usb_hid_send_status_report(void) {
    if (!tud_hid_ready()) {
        return;
    }
    
    hid_report_status_t report;
    report.report_id = HID_REPORT_ID_STATUS;
    report.status_flags = tachometer_get_connection_status();
    report.error_code = current_error_code;
    tachometer_get_all_rpm(report.fan_status);
    report.reserved = 0;
    
    // Status-Report senden (Input Report)
    tud_hid_report(HID_REPORT_ID_STATUS, &report, sizeof(report));
}
