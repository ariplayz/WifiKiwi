/* SPDX-License-Identifier: GPL-3.0-or-later */
#include "pe4259.h"
#include "esp_log.h"
static const char *TAG = "pe4259";

esp_err_t pe4259_init(pe4259_id_t id, int gpio_ctl)
{
    ESP_LOGI(TAG, "init id=%d gpio=%d (stub)", id, gpio_ctl);
    return ESP_OK;
}

esp_err_t pe4259_select(pe4259_id_t id, pe4259_port_t port)
{
    ESP_LOGI(TAG, "switch %d -> port %d (stub)", id, port);
    return ESP_OK;
}
