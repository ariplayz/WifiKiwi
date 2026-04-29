## App stubs

Each subdirectory is one top-level app surfaced as a tile on the LVGL home
screen. See `docs/ui-guide.md` and `docs/plan.md` for the per-app screen
breakdown.

| Dir | App | Status |
|---|---|---|
| `wifi/`   | Wi-Fi 2.4 + 5 GHz (deauth, beacon, probe, monitor)            | stub |
| `ble/`    | BLE scanner / advertiser / GATT                              | stub |
| `subghz/` | CC1101 capture / replay / analyzer                           | stub |
| `sdr/`    | RTL-SDR waterfall + tuning                                   | stub |
| `siggen/` | ADF4351 CW signal generator                                  | stub |
| `tools/`  | File browser, hex viewer, antenna helpers                    | stub |

Every TX-capable app must:
1. Call `ui_confirm_tx_gate()` first (modal hold-to-confirm).
2. Call `rf_safety_request_tx()` to obtain the path.
3. Restrict targets to the user-defined allowlist (see `docs/legal-and-safe-use.md`).
4. Call `rf_safety_release_tx()` on exit (including error paths).
