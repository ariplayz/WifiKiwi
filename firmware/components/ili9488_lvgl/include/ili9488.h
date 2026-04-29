/* SPDX-License-Identifier: GPL-3.0-or-later
 * ILI9488 480x320 IPS LCD driver, SPI 4-wire.
 */
#pragma once

#include <stdint.h>
#include "esp_err.h"

typedef struct {
    int spi_host;
    int gpio_cs;
    int gpio_dc;
    int gpio_rst;
    int gpio_bl;
    uint32_t spi_clock_hz;
} ili9488_config_t;

esp_err_t ili9488_init(const ili9488_config_t *cfg);
esp_err_t ili9488_set_brightness(uint8_t pct);
