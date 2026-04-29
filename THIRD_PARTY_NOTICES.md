# Third-party notices

WifiKiwi includes or is derived from the following open-source projects.
Each retains its original copyright; their licenses are reproduced or
referenced in `LICENSES/`. This file is the canonical attribution list.

## Firmware

| Project | Upstream | License | Used for | Forked at |
|---|---|---|---|---|
| Bruce | https://github.com/pr3y/Bruce | GPL-3.0-or-later | Base firmware: LVGL UI scaffold, app framework, sub-GHz drivers (CC1101), BLE-spam, RF attack modules | _TBD on first import_ |
| ESP32 Marauder | https://github.com/justcallmekoko/ESP32Marauder | GPL-3.0-or-later | 2.4 GHz Wi-Fi attack suite (deauth, beacon spam, probe, PMKID, evil-twin, packet monitor); reference for menu / modal-confirmation patterns | _TBD on first import_ |
| PortaPack Mayhem | https://github.com/portapack-mayhem/mayhem | GPL-3.0-or-later | UI inspiration (tile home, status bar), FFT/waterfall renderer (ported to LVGL 9 + ESP32-C5), sub-GHz band-plan database | _TBD on first import_ |
| LVGL | https://github.com/lvgl/lvgl | MIT | UI framework | _TBD_ |
| ESP-IDF | https://github.com/espressif/esp-idf | Apache-2.0 + others | SoC SDK | _TBD_ |

## Hardware

| Item | Source | License | Notes |
|---|---|---|---|
| ESP32-C5-WROOM-1U datasheet & reference design | Espressif | Espressif documentation license | Reference design for module integration only; no copied artwork |
| CC1101 reference application circuit | Texas Instruments | TI documentation | Standard application schematic |
| ADF4351 evaluation board | Analog Devices | ADI documentation | Reference for matching network |

## Documentation

This project's documentation may incorporate text or images licensed under
CC-BY or CC-BY-SA from upstream projects, with attribution noted inline.

---

**Adding a new upstream import**: when forking or importing code from a new
upstream, append a row to the relevant table above with the project name,
URL, license SPDX identifier, what it's used for, and the upstream
commit/tag your fork is based on.
