/* SPDX-License-Identifier: GPL-3.0-or-later
 * CC1101 sub-GHz transceiver driver — stub implementation.
 * Real register layout: see TI CC1101 datasheet (SWRS061I) §29.
 */
#include "cc1101.h"
#include "esp_log.h"

static const char *TAG = "cc1101";

esp_err_t cc1101_init(const cc1101_config_t *cfg)
{
    (void)cfg;
    ESP_LOGI(TAG, "init (stub)");
    return ESP_OK;
}

esp_err_t cc1101_set_freq_hz(uint32_t freq_hz)
{
    ESP_LOGI(TAG, "set_freq %lu Hz (stub)", (unsigned long)freq_hz);
    return ESP_OK;
}

esp_err_t cc1101_set_modulation(cc1101_modulation_t mod)
{
    ESP_LOGI(TAG, "set_modulation %d (stub)", mod);
    return ESP_OK;
}

esp_err_t cc1101_set_tx_power_dbm(int8_t dbm)
{
    ESP_LOGI(TAG, "set_tx_power %d dBm (stub)", dbm);
    return ESP_OK;
}

esp_err_t cc1101_rx_start(void)         { return ESP_OK; }
esp_err_t cc1101_tx_packet(const uint8_t *buf, size_t len)
{
    (void)buf; (void)len; return ESP_OK;
}
int       cc1101_read_rssi_dbm(void)    { return -120; }
esp_err_t cc1101_idle(void)             { return ESP_OK; }
