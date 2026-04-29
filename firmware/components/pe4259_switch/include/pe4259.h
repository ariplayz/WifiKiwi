/* SPDX-License-Identifier: GPL-3.0-or-later
 * PE4259 SPDT RF switch driver (DC - 3 GHz, single GPIO ctrl).
 *
 * Three instances on WifiKiwi:
 *   #1 ESP32-C5 u.FL between SMA-A (2.4G) and SMA-B (5G)
 *   #2 SMA-A high port between ESP32-C5 2.4G and RTL-SDR
 *   #3 SMA-B between ESP32-C5 5G and ADF4351
 */
#pragma once

#include <stdbool.h>
#include "esp_err.h"

typedef enum {
    PE4259_SWITCH_BAND,
    PE4259_SWITCH_SMA_A_HP,
    PE4259_SWITCH_SMA_B,
    PE4259_SWITCH__COUNT,
} pe4259_id_t;

typedef enum { PE4259_PORT_RF1, PE4259_PORT_RF2 } pe4259_port_t;

esp_err_t pe4259_init(pe4259_id_t id, int gpio_ctl);
esp_err_t pe4259_select(pe4259_id_t id, pe4259_port_t port);
