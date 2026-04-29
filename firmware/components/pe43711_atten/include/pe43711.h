/* SPDX-License-Identifier: GPL-3.0-or-later
 * PE43711 7-bit digital step attenuator (0 - 31.75 dB / 0.25 dB step).
 * 3-wire serial: LE/CLK/DATA.
 */
#pragma once

#include <stdint.h>
#include "esp_err.h"

typedef enum {
    PE43711_TX_LOW_BAND,
    PE43711_TX_HIGH_BAND,
    PE43711__COUNT,
} pe43711_id_t;

typedef struct {
    int gpio_le;
    int gpio_clk;
    int gpio_data;
} pe43711_pins_t;

esp_err_t pe43711_init(pe43711_id_t id, const pe43711_pins_t *pins);
esp_err_t pe43711_set_atten_q025(pe43711_id_t id, uint8_t atten_q025);
esp_err_t pe43711_set_atten_db_x10(pe43711_id_t id, uint16_t db_x10);
