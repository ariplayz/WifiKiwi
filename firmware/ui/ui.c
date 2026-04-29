/* SPDX-License-Identifier: GPL-3.0-or-later
 * UI dispatcher stub. Real LVGL screens land here in fw-ui-home.
 */
#include "ui.h"
#include "esp_log.h"

static const char *TAG = "ui";

esp_err_t ui_init(void)
{
    ESP_LOGI(TAG, "ui_init (stub)");
    return ESP_OK;
}

esp_err_t ui_show_home(void)
{
    ESP_LOGI(TAG, "show_home (stub)");
    return ESP_OK;
}

esp_err_t ui_launch_app(ui_app_id_t app)
{
    ESP_LOGI(TAG, "launch app %d (stub)", app);
    return ESP_OK;
}

bool ui_confirm_tx_gate(const char *human_action)
{
    ESP_LOGW(TAG, "TX gate stub denying: %s", human_action);
    return false;
}
