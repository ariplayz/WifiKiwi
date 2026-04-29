/* SPDX-License-Identifier: GPL-3.0-or-later
 *
 * RF safety arbiter.
 *
 * Single point of authority for whether *anything* on this board is allowed
 * to transmit. Every TX-capable subsystem (CC1101, ESP32-C5 Wi-Fi/BLE,
 * ADF4351, the PE4259 switch matrix that selects them) goes through this
 * module. Default state at boot: everything muted, RF-active LED off.
 *
 * UI policy — modal "are you sure" gates, allowlist enforcement,
 * Faraday-cage banner — must be impossible for an app to bypass by directly
 * poking a driver register, hence the central arbiter.
 *
 * Copyright (c) 2026 The WifiKiwi contributors.
 */

#include "rf_safety.h"

#include "esp_log.h"

static const char *TAG = "rf_safety";

void rf_safety_init(void)
{
    ESP_LOGI(TAG, "RF-safety arbiter initialised; all TX disabled.");
    // TODO: configure GPIO for RF-ACTIVE LED (red), set output low.
    // TODO: assert reset on every TX-capable peripheral.
}

void rf_safety_all_off(void)
{
    // TODO: drive every PE4259 control line to a defined "off" state,
    //       disable CC1101 PA, disable ADF4351 RF output, stop Wi-Fi TX,
    //       stop BLE advertising, clear RF-ACTIVE LED.
}

bool rf_safety_request_tx(rf_path_t path, const char *reason)
{
    ESP_LOGW(TAG, "TX request for path %d (%s) — denied (stub).", path, reason);
    return false;
}

void rf_safety_release_tx(rf_path_t path)
{
    (void)path;
}
