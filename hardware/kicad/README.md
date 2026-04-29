# WifiKiwi KiCad project

KiCad 10.x hierarchical project. Open `WifiKiwi.kicad_pro` from the KiCad
project manager.

## Layout

```
hardware/kicad/
├── WifiKiwi.kicad_pro      Project file
├── WifiKiwi.kicad_sch      Root schematic (hierarchical, 7 sub-sheets)
├── WifiKiwi.kicad_pcb      PCB (100 x 65 mm, 4-layer outline only)
├── sheets/                 Sub-sheet schematics, one per subsystem
│   ├── 01_power.kicad_sch
│   ├── 02_mcu.kicad_sch
│   ├── 03_display.kicad_sch
│   ├── 04_rf_frontend.kicad_sch
│   ├── 05_subghz.kicad_sch
│   ├── 06_siggen.kicad_sch
│   └── 07_io.kicad_sch
├── symbols/                Project-local symbol libraries
│   └── wifikiwi.kicad_sym  (placeholder - symbols TODO, see below)
├── footprints/             Project-local footprint libraries
│   └── wifikiwi.pretty/    (empty - footprints TODO, see below)
├── sym-lib-table           Auto-mounts symbols/wifikiwi.kicad_sym
├── fp-lib-table            Auto-mounts footprints/wifikiwi.pretty
└── gen_sheets.py           Re-generates sheets/* + root from a Python schema
```

## Current state

* The project **opens cleanly** in KiCad 10.0+ and exports to PDF / SVG.
* All 7 sub-sheets are present with their hierarchical pins defined and
  a netlist plan rendered as on-sheet text.
* The PCB has a 100 x 65 mm rectangular outline with four 1.6 mm
  mounting-hole pilots in the corners. No copper or footprints yet.
* `kicad-cli sch erc` reports ~150 violations, all "Pin not connected"
  on hierarchical sheet pins. **This is expected**: the sheets describe
  *what* needs to be wired; the actual symbol placement and wiring is
  still a human-in-the-loop task in the KiCad GUI.

## Regenerating sheets

If you want to add or rename a hierarchical pin, edit the `SHEETS` list
in `gen_sheets.py` and run:

```bash
python3 gen_sheets.py
```

This will re-emit `sheets/*.kicad_sch` and the root `WifiKiwi.kicad_sch`
**from scratch**, clobbering any GUI edits to those files. Use the
generator only while iterating on the sheet structure; once you start
wiring, work in the GUI and treat the generator as deprecated.

## Symbols still to draw

Project-local symbols are needed for the parts that aren't in KiCad's
stock libraries. Draw these in the KiCad Symbol Editor and save into
`symbols/wifikiwi.kicad_sym`:

| Symbol | Footprint hint | Datasheet pinout source |
|---|---|---|
| ESP32-C5-WROOM-1U-N8R8 | RF_Module:ESP32-WROOM-1U (verify keepout) | Espressif ESP32-C5 datasheet |
| CC1101 | Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm | TI CC1101 datasheet |
| ADF4351 | Package_DFN_QFN:LFCSP-32_5x5mm | ADI ADF4351 datasheet |
| PE4259 | Package_TO_SOT_SMD:SOT-363_SC-70-6 | Peregrine PE4259 datasheet |
| PE43711 | Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm | Peregrine PE43711 datasheet |
| SPF5189Z | Package_TO_SOT_SMD:SOT-89-3 | Qorvo SPF5189Z datasheet |
| ILI9488 FFC-40 | Connector_FFC-FPC:Hirose_FH12-40S-0.5SH | Generic ILI9488 panel |
| FT6336U | usually integrated on the LCD FFC | Focaltech FT6336U datasheet |

For each, define pin numbers exactly as on the datasheet and set the
`Footprint` field to a stock KiCad footprint (or add a custom one to
`footprints/wifikiwi.pretty/`).

## Generating gerbers (after layout)

Once the PCB is laid out, generate JLCPCB-compatible production files:

```bash
mkdir -p ../gerbers ../cpl
kicad-cli pcb export gerbers WifiKiwi.kicad_pcb -o ../gerbers \
  --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts \
  --no-x2 --use-drill-file-origin --subtract-soldermask
kicad-cli pcb export drill WifiKiwi.kicad_pcb -o ../gerbers/ \
  --excellon-separate-th --excellon-units mm --drill-origin plot
kicad-cli pcb export pos WifiKiwi.kicad_pcb -o ../cpl/cpl.csv --format csv --units mm
```

The CI workflow under `.github/workflows/hardware.yml` runs ERC + DRC
on every PR.

## Net classes (already configured in WifiKiwi.kicad_pro)

* **Default** -- 0.25 mm track / 0.20 mm clearance.
* **RF50**    -- 0.36 mm track / 0.30 mm clearance (50 ohm CPW on top
  layer with 0.21 mm dielectric to the GND inner). Verify on your
  stackup with KiCad's calculator.
* **Power**   -- 0.50 mm track / 0.25 mm clearance.

## Validating locally

```bash
kicad-cli sch erc WifiKiwi.kicad_sch -o /tmp/erc.json --format json
kicad-cli pcb drc WifiKiwi.kicad_pcb -o /tmp/drc.json --format json
kicad-cli sch export pdf WifiKiwi.kicad_sch -o /tmp/wifikiwi.pdf
```
