# WifiKiwi

A handheld, open-source, multi-radio Wi-Fi / RF research tool for use **inside
a Faraday cage against access points and devices you own**.

> ⚠️ **Legal & safety notice.** This device is intended for cybersecurity
> research on equipment you own, in a properly shielded enclosure, where
> permitted by your local regulator. In Mexico the relevant authority is the
> [IFT](https://www.ift.org.mx/). Operating any RF transmitter outside its
> authorized bands or power limits is illegal almost everywhere, and using
> this device against networks or devices you do not own is illegal almost
> everywhere. **You are solely responsible for how you use it.**

## Overview

WifiKiwi is built around the [Espressif ESP32-C5](https://www.espressif.com/en/products/socs/esp32-c5),
the first sub-$5 SoC with native dual-band 2.4 GHz **and** 5 GHz Wi-Fi 6,
plus BLE 5.3. It pairs the C5 with discrete radios for sub-GHz work
(CC1101), wideband signal generation (ADF4351), and wideband receive
(socketed RTL-SDR v4), all under a 3.5" capacitive touchscreen UI built on
LVGL 9.

### Capabilities

| Band | Hardware | TX | RX |
|---|---|---|---|
| Sub-GHz (300 – 928 MHz) | TI CC1101 | ✅ OOK / 2-FSK / GFSK / MSK | ✅ |
| 2.4 GHz Wi-Fi (802.11 b/g/n/ax) | ESP32-C5 | ✅ | ✅ monitor mode |
| **5 GHz Wi-Fi (802.11 a/n/ac/ax)** | ESP32-C5 | ✅ | ✅ monitor mode |
| Bluetooth LE 5.3 | ESP32-C5 | ✅ | ✅ |
| 35 MHz – 4.4 GHz CW (single tone) | ADF4351 | ✅ test signal only | — |
| 500 kHz – 1.75 GHz IQ wideband | RTL-SDR v4 (USB) | — | ✅ |

### What it does **not** do

- No broadband jamming. No high-power PA. No reserved board area for adding
  one. (See the project [non-goals](docs/legal-and-safe-use.md).)
- No 6 GHz Wi-Fi 6E/7 — no microcontroller-class chip exists for it.
- No continuous wideband TX. The wideband path is RX-only plus a single-tone
  CW signal generator.

## Repository layout

```
docs/        documentation, build guides, schematics PDF (CC-BY-SA 4.0)
hardware/    KiCad project, gerbers, BOM, CPL, FreeCAD enclosure (CERN-OHL-S v2)
firmware/    ESP-IDF / PlatformIO project (GPLv3)
LICENSES/    full text of all three licenses used
.github/     issue templates and CI workflows
```

## Licensing

This is a multi-license project — see [LICENSES/](LICENSES/) for full texts.

| Component | License | Why |
|---|---|---|
| Firmware (`firmware/`) | **GPL-3.0-or-later** | Forks code from Bruce, Marauder, and PortaPack/Mayhem (all GPLv3) |
| Hardware (`hardware/`) | **CERN-OHL-S v2** | Hardware equivalent of GPL — strongly reciprocal |
| Documentation (`docs/`) | **CC-BY-SA 4.0** | Standard open-content license |

Upstream attribution lives in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Status

🚧 Early design phase. Schematic and PCB are in active development; firmware
is being scaffolded from a fork of [Bruce](https://github.com/pr3y/Bruce).
The current implementation plan lives at
`~/.copilot/session-state/.../plan.md` (in development) and will be moved to
`docs/plan.md` once stable.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before opening a PR. Contributions
require a [Developer Certificate of Origin](https://developercertificate.org/)
sign-off (`git commit -s`).

## Acknowledgements

WifiKiwi stands on the shoulders of:

- [Bruce](https://github.com/pr3y/Bruce) — LVGL-based ESP32 RF tool we fork
- [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder) — Wi-Fi attack suite we port
- [PortaPack Mayhem](https://github.com/portapack-mayhem/mayhem) — UI and waterfall inspiration
- [Espressif](https://www.espressif.com/) for the ESP32-C5
