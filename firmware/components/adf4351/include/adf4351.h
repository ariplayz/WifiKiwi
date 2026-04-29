/* SPDX-License-Identifier: GPL-3.0-or-later
 * ADF4351 PLL/VCO driver stub (35 MHz - 4.4 GHz, single-tone CW).
 * SPI mode 0, max 20 MHz, 32-bit register writes (R0-R5).
 */
#pragma once

#include <stdbool.h>
#include <stdint.h>
#include "esp_err.h"

typedef enum {
    ADF4351_PWR_M4_DBM = 0,
    ADF4351_PWR_M1_DBM = 1,
    ADF4351_PWR_P2_DBM = 2,
    ADF4351_PWR_P5_DBM = 3,
} adf4351_power_t;

typedef struct {
    int spi_host;
    int gpio_le;
    int gpio_ce;
    int gpio_ld;
    uint32_t ref_clk_hz;
} adf4351_config_t;

esp_err_t adf4351_init(const adf4351_config_t *cfg);
esp_err_t adf4351_set_freq_hz(uint64_t freq_hz);
esp_err_t adf4351_set_power(adf4351_power_t pwr);
esp_err_t adf4351_output_enable(bool on);
bool      adf4351_locked(void);
