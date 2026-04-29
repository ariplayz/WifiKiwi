## BOM notes

Single-unit cost estimate (USD), 2026 pricing:

| Group | ~USD |
|---|---|
| ESP32-C5-WROOM-1U-N8R8 | 4 |
| CC1101 module | 4 |
| ADF4351 module | 12 |
| RTL-SDR v4 dongle | 30 |
| ILI9488 3.5" + FT6336U touchscreen | 14 |
| 3 × PE4259 + 2 × PE43711 + 2 × SPF5189Z + diplexer | 22 |
| 2 × SMA + USB-C + microSD + internal USB-A + headers | 8 |
| Power tree (TP4056 + MT3608 + AMS1117 + 18650 holder + cell) | 12 |
| Passives, screws, light pipes | 8 |
| 2 × antennas (wideband low + dual-band high) | 12 |
| 4-layer PCB, JLCPCB (5 pcs) | 10 |
| 3D-printed enclosure (filament cost) | 3 |
| **Total** | **~139** |

LCSC part numbers in `bom.csv` will be filled in during schematic capture
when the exact passive values are known and verified-in-stock at order
time.
