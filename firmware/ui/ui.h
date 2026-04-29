/* SPDX-License-Identifier: GPL-3.0-or-later
 * UI dispatcher - LVGL home tile screen + app launch.
 *
 * Tiles map 1:1 to the apps under firmware/apps/. See docs/ui-guide.md.
 */
#pragma once

#include "esp_err.h"

typedef enum {
    UI_APP_WIFI,
    UI_APP_BLE,
    UI_APP_SUBGHZ,
    UI_APP_SDR,
    UI_APP_SIGGEN,
    UI_APP_TOOLS,
    UI_APP_LOGS,
    UI_APP_SETTINGS,
    UI_APP__COUNT,
} ui_app_id_t;

esp_err_t ui_init(void);
esp_err_t ui_show_home(void);
esp_err_t ui_launch_app(ui_app_id_t app);

/* Modal "Faraday-cage confirmation" gate. Returns true on hold-to-confirm,
 * false if cancelled or timed out. Every TX-capable app must call this
 * before requesting TX from rf_safety. */
bool ui_confirm_tx_gate(const char *human_action);
