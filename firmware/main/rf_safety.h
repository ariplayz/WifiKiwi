/* SPDX-License-Identifier: GPL-3.0-or-later
 *
 * RF safety arbiter — public API. See rf_safety.c for rationale.
 *
 * Copyright (c) 2026 The WifiKiwi contributors.
 */

#pragma once

#include <stdbool.h>

typedef enum {
    RF_PATH_CC1101_TX,
    RF_PATH_ESP32_WIFI_2G,
    RF_PATH_ESP32_WIFI_5G,
    RF_PATH_ESP32_BLE,
    RF_PATH_ADF4351,
    RF_PATH__COUNT,
} rf_path_t;

void rf_safety_init(void);
void rf_safety_all_off(void);

/* Returns true on success (TX permitted, RF-ACTIVE LED latched on),
 * false if denied by policy. The caller must call rf_safety_release_tx()
 * when finished. */
bool rf_safety_request_tx(rf_path_t path, const char *reason);
void rf_safety_release_tx(rf_path_t path);
