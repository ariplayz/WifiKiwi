/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "ft6336.h"
#include "esp_log.h"
static const char *TAG = "ft6336";
esp_err_t ft6336_init(const ft6336_config_t *cfg)
{
    (void)cfg;
    ESP_LOGI(TAG, "init (stub)");
    return ESP_OK;
}
esp_err_t ft6336_read(ft6336_point_t *out)
{
    if (!out) return ESP_ERR_INVALID_ARG;
    out->pressed = false;
    out->x = out->y = 0;
    return ESP_OK;
}
