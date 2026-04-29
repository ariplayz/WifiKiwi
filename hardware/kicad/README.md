# KiCad project

🚧 **TBD** — KiCad 8 project will live in this directory.

Files (planned):

- `WifiKiwi.kicad_pro`
- `WifiKiwi.kicad_sch` (root sheet)
- `WifiKiwi.kicad_pcb`
- `lib/` — vendored symbols + footprints for parts not in default KiCad
  libraries (ESP32-C5-WROOM-1U, CC1101 module, ADF4351 module, ILI9488,
  PE4259, PE43711, SPF5189Z, FT6336U, etc.)

## Stackup (4 layer, JLC standard)

| Layer | Use |
|---|---|
| 1 (top) | Signal + RF traces (50 Ω microstrip) |
| 2 | Solid GND (RF return, controlled-impedance reference) |
| 3 | 3.3 V plane + select power islands |
| 4 (bottom) | Signal (low-speed digital, button pads) |

Target dielectric: JLC standard FR-4, total board thickness 1.6 mm. 50 Ω
microstrip width on top to layer-2 GND ≈ 0.30 mm. Antenna feeds short and
ground-stitched.
