/* SPDX-License-Identifier: GPL-3.0-or-later
 * SPF5189Z LNA bias + bypass control. Two instances (low/high band RX).
 */
#pragma once

#include <stdbool.h>
#include "esp_err.h"

typedef enum {
    SPF5189_RX_LOW_BAND,
    SPF5189_RX_HIGH_BAND,
    SPF5189__COUNT,
} spf5189_id_t;

typedef struct {
    int gpio_bias_en;
    int gpio_bypass_ctl;
} spf5189_pins_t;

esp_err_t spf5189_init(spf5189_id_t id, const spf5189_pins_t *pins);
esp_err_t spf5189_set_enabled(spf5189_id_t id, bool enabled);
esp_err_t spf5189_set_bypass(spf5189_id_t id, bool bypass);
