/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "pe43711.h"
#include "esp_log.h"
static const char *TAG = "pe43711";

esp_err_t pe43711_init(pe43711_id_t id, const pe43711_pins_t *pins)
{
    (void)pins;
    ESP_LOGI(TAG, "init id=%d (stub)", id);
    return ESP_OK;
}

esp_err_t pe43711_set_atten_q025(pe43711_id_t id, uint8_t atten_q025)
{
    if (atten_q025 > 127) return ESP_ERR_INVALID_ARG;
    ESP_LOGI(TAG, "atten[%d] = %u.%02u dB (stub)",
             id, atten_q025 / 4, (atten_q025 % 4) * 25);
    return ESP_OK;
}

esp_err_t pe43711_set_atten_db_x10(pe43711_id_t id, uint16_t db_x10)
{
    if (db_x10 > 3175) return ESP_ERR_INVALID_ARG;
    // 0.25 dB step = 2.5 in tenths-of-dB.
    return pe43711_set_atten_q025(id, (uint8_t)(db_x10 / 25 * 10 / 10));
}
