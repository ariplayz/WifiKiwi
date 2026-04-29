/* SPDX-License-Identifier: GPL-3.0-or-later
 * CC1101 sub-GHz transceiver driver stub.
 * Frequency ranges: 300-348, 387-464, 779-928 MHz.
 * Modulations: OOK, 2-FSK, GFSK, MSK. SPI mode 0, max 6.5 MHz.
 */
#pragma once

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"

typedef enum {
    CC1101_MOD_OOK,
    CC1101_MOD_2FSK,
    CC1101_MOD_GFSK,
    CC1101_MOD_MSK,
} cc1101_modulation_t;

typedef struct {
    int spi_host;
    int gpio_cs;
    int gpio_gdo0;
    int gpio_gdo2;
} cc1101_config_t;

esp_err_t cc1101_init(const cc1101_config_t *cfg);
esp_err_t cc1101_set_freq_hz(uint32_t freq_hz);
esp_err_t cc1101_set_modulation(cc1101_modulation_t mod);
esp_err_t cc1101_set_tx_power_dbm(int8_t dbm);
esp_err_t cc1101_rx_start(void);
esp_err_t cc1101_tx_packet(const uint8_t *buf, size_t len);
int       cc1101_read_rssi_dbm(void);
esp_err_t cc1101_idle(void);
