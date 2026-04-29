/* SPDX-License-Identifier: GPL-3.0-or-later
 * FT6336U capacitive touch controller (I2C @ 400 kHz, addr 0x38).
 */
#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "esp_err.h"

typedef struct {
    int i2c_port;
    int gpio_int;
    int gpio_rst;
} ft6336_config_t;

typedef struct {
    bool pressed;
    uint16_t x;
    uint16_t y;
} ft6336_point_t;

esp_err_t ft6336_init(const ft6336_config_t *cfg);
esp_err_t ft6336_read(ft6336_point_t *out);
