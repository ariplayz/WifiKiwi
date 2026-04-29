/* SPDX-License-Identifier: GPL-3.0-or-later
 * ADF4351 driver — stub.
 * Real register math: see Analog Devices ADF4351 datasheet (Rev D), §"REGISTER MAPS".
 */
#include "adf4351.h"
#include "esp_log.h"

static const char *TAG = "adf4351";

esp_err_t adf4351_init(const adf4351_config_t *cfg)
{
    (void)cfg;
    ESP_LOGI(TAG, "init (stub)");
    return ESP_OK;
}

esp_err_t adf4351_set_freq_hz(uint64_t freq_hz)
{
    if (freq_hz < 35000000ULL || freq_hz > 4400000000ULL) {
        return ESP_ERR_INVALID_ARG;
    }
    ESP_LOGI(TAG, "set_freq %llu Hz (stub)", (unsigned long long)freq_hz);
    return ESP_OK;
}

esp_err_t adf4351_set_power(adf4351_power_t pwr)
{
    ESP_LOGI(TAG, "set_power %d (stub)", pwr);
    return ESP_OK;
}

esp_err_t adf4351_output_enable(bool on)
{
    ESP_LOGI(TAG, "output %s (stub)", on ? "ON" : "off");
    return ESP_OK;
}

bool adf4351_locked(void) { return false; }
