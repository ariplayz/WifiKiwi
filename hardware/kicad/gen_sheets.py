#!/usr/bin/env python3
"""
Generate WifiKiwi KiCad 10 hierarchical schematic sheets.

This emits a root sheet with sheet symbols pointing to per-subsystem
sub-sheets. Each sub-sheet has a title block, a netlist-plan text block,
and the hierarchical labels that match the root sheet pins. Wiring
(symbol placement, junctions, traces) is intentionally left to a human
in the KiCad 10 GUI -- hand-writing those s-expressions is error-prone
and the diff from a real GUI session would be enormous.

Run from anywhere:
    python3 gen_sheets.py

Output: sheets/*.kicad_sch and an updated WifiKiwi.kicad_sch root.
"""
from __future__ import annotations

import os
import textwrap
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHEETS_DIR = HERE / "sheets"
ROOT_SCH = HERE / "WifiKiwi.kicad_sch"

KICAD_VERSION = "20260306"
GENERATOR = "wifikiwi-gen"
GENERATOR_VERSION = "10.0"


# ---------------------------------------------------------------------------
# Subsystem definitions: each sheet's hierarchical pins + a netlist plan.
# Pins are listed in clockwise order starting at the left edge.
# Plan text is rendered as a (text ...) block on the sheet so engineers
# opening the sheet can see what nets need wiring without flipping to a doc.
# ---------------------------------------------------------------------------

SHEETS = [
    {
        "file": "01_power.kicad_sch",
        "title": "Power - USB-C input, charger, regulators",
        "pins": [
            ("VBUS_5V",     "output"),
            ("VSYS",        "output"),
            ("VBAT",        "bidirectional"),
            ("V3P3",        "output"),
            ("V3P3_RF",     "output"),
            ("V5P0_LCD",    "output"),
            ("PWR_EN",      "input"),
            ("CHG_STAT",    "output"),
            ("BAT_LVL",     "output"),
        ],
        "plan": [
            "POWER TREE",
            "==========",
            "USB-C (CC1/CC2 5.1k pulldowns) -> ESD (SP3010) -> VBUS_5V",
            "VBUS_5V -> TP4056 (1A charge, NTC pin -> 10k thermistor) -> VBAT (1S Li-ion 2000-3000mAh, JST-PH 2.0)",
            "ideal-diode OR (DMP2160 / FDN340P) between VBUS_5V and VBAT -> VSYS",
            "VSYS -> TPS61023 boost (5.0V @ 1A) -> V5P0_LCD (display backlight + 5V rail)",
            "VSYS -> AP2112K-3.3 LDO (600mA) -> V3P3 (digital, MCU, logic)",
            "V3P3 -> ferrite bead BLM18PG471 -> V3P3_RF (clean rail to CC1101, ADF4351, LNAs, switches)",
            "VBAT -> resistor divider (200k/100k) -> BAT_LVL (to ESP32 ADC, 0-2.2V range)",
            "TP4056 STAT pin -> CHG_STAT (open-drain, ESP32 GPIO with pullup)",
            "PWR_EN: latching pushbutton -> Pchan FET high-side switch on VSYS",
            "BULK CAPS",
            "----------",
            "VBUS: 10uF X5R 0805 + 100nF",
            "VBAT: 22uF X5R + 100nF",
            "V3P3: 10uF + 100nF + 100nF (one near each IC)",
            "V3P3_RF: 4.7uF + 100nF + 10nF (RF rail; place 10nF closest to each pin)",
            "V5P0_LCD: 22uF + 100nF",
        ],
    },
    {
        "file": "02_mcu.kicad_sch",
        "title": "MCU - ESP32-C5-WROOM-1U + USB/JTAG + boot logic",
        "pins": [
            ("V3P3",        "input"),
            ("GND",         "input"),
            ("USB_DP",      "bidirectional"),
            ("USB_DM",      "bidirectional"),
            ("UART_TX",     "output"),
            ("UART_RX",     "input"),
            ("SPI_LCD_SCK", "output"),
            ("SPI_LCD_MOSI","output"),
            ("SPI_LCD_MISO","input"),
            ("SPI_LCD_CS",  "output"),
            ("SPI_LCD_DC",  "output"),
            ("SPI_LCD_RST", "output"),
            ("SPI_LCD_BL",  "output"),
            ("I2C_SDA",     "bidirectional"),
            ("I2C_SCL",     "output"),
            ("TOUCH_INT",   "input"),
            ("TOUCH_RST",   "output"),
            ("SPI_RF_SCK",  "output"),
            ("SPI_RF_MOSI", "output"),
            ("SPI_RF_MISO", "input"),
            ("CC1101_CS",   "output"),
            ("CC1101_GDO0", "input"),
            ("CC1101_GDO2", "input"),
            ("ADF_LE",      "output"),
            ("ADF_CE",      "output"),
            ("ADF_LD",      "input"),
            ("SD_CS",       "output"),
            ("SW_BAND_CTL", "output"),
            ("SW_SMA_A_CTL","output"),
            ("SW_SMA_B_CTL","output"),
            ("ATTEN_LO_LE", "output"),
            ("ATTEN_HI_LE", "output"),
            ("ATTEN_CLK",   "output"),
            ("ATTEN_DATA",  "output"),
            ("LNA_LO_EN",   "output"),
            ("LNA_HI_EN",   "output"),
            ("LNA_LO_BYP",  "output"),
            ("LNA_HI_BYP",  "output"),
            ("RF_ACTIVE",   "output"),
            ("BTN_OK",      "input"),
            ("BTN_BACK",    "input"),
            ("BTN_UP",      "input"),
            ("BTN_DOWN",    "input"),
            ("BAT_LVL",     "input"),
            ("CHG_STAT",    "input"),
        ],
        "plan": [
            "ESP32-C5-WROOM-1U-N8R8 (LCSC C-TBD) - dual-band Wi-Fi 6 + BLE 5.3, 8MB flash, 8MB PSRAM, u.FL antenna pigtail.",
            "DECOUPLING",
            "----------",
            "VDD pin: 10uF + 100nF + 10nF + 1nF in parallel right at the module pad.",
            "EN pin: 10k pullup to V3P3, 1uF to GND, RC delay >= 50ms after VDD stable.",
            "BOOT/STRAP",
            "----------",
            "GPIO0: 10k pullup; pushbutton to GND (BOOT button).",
            "EN  : 10k pullup; pushbutton to GND (RST button); 100nF to GND.",
            "GPIO45/46/8 strapping: leave at default (boot-from-flash).",
            "USB",
            "---",
            "USB_DP / USB_DM go to USB-C (with 22 ohm series + ESD diodes). Use native USB-Serial-JTAG.",
            "UART0 also broken out to a 4-pin header (RX/TX/RTS/DTR auto-reset for esptool).",
            "PIN ASSIGNMENT (CANDIDATE - HUMAN MUST VERIFY AGAINST C5 STRAPS)",
            "---------------------------------------------------------------",
            "GPIO 4..7   : SPI for LCD (SCK/MOSI/MISO/CS)",
            "GPIO 8      : LCD DC",
            "GPIO 9      : LCD RST",
            "GPIO 10     : LCD BL (LEDC PWM channel 0)",
            "GPIO 11/12  : I2C (SCL/SDA) for FT6336U @ 400 kHz",
            "GPIO 13     : TOUCH_INT",
            "GPIO 14     : TOUCH_RST",
            "GPIO 15..18 : SPI for RF (SCK/MOSI/MISO/CC1101_CS)",
            "GPIO 19/20  : CC1101 GDO0/GDO2",
            "GPIO 21..23 : ADF4351 LE/CE/LD",
            "GPIO 24     : SD_CS",
            "GPIO 25..27 : PE4259 SW_BAND/SMA_A/SMA_B control",
            "GPIO 28..31 : PE43711 LE_LO/LE_HI/CLK/DATA",
            "GPIO 32..35 : LNA_LO_EN/HI_EN/LO_BYP/HI_BYP",
            "GPIO 36     : RF_ACTIVE LED (red, 1k series)",
            "GPIO 37..40 : 4 user buttons (OK/BACK/UP/DOWN, internal pullups)",
            "ADC1_CH0    : BAT_LVL",
            "GPIO ANY    : CHG_STAT (input, pullup)",
        ],
    },
    {
        "file": "03_display.kicad_sch",
        "title": "Display - ILI9488 3.5\" SPI LCD + FT6336U cap touch",
        "pins": [
            ("V3P3",        "input"),
            ("V5P0_LCD",    "input"),
            ("GND",         "input"),
            ("SPI_LCD_SCK", "input"),
            ("SPI_LCD_MOSI","input"),
            ("SPI_LCD_MISO","output"),
            ("SPI_LCD_CS",  "input"),
            ("SPI_LCD_DC",  "input"),
            ("SPI_LCD_RST", "input"),
            ("SPI_LCD_BL",  "input"),
            ("I2C_SDA",     "bidirectional"),
            ("I2C_SCL",     "input"),
            ("TOUCH_INT",   "output"),
            ("TOUCH_RST",   "input"),
        ],
        "plan": [
            "DISPLAY MODULE",
            "==============",
            "ILI9488 480x320 IPS 3.5\" SPI LCD, FFC 40-pin (or pre-built breakout via FFC).",
            "Drive in 16-bit color via SPI 4-wire (RGB565), max 40 MHz SCK.",
            "Backlight: 4x white LEDs in series, 80mA total. AOT403 N-MOSFET driven by SPI_LCD_BL (LEDC PWM, 5 kHz).",
            "Series resistor: V5P0_LCD - 12 ohm - 4xLED string - drain of FET - GND.",
            "TOUCH",
            "-----",
            "FT6336U on same FFC (most 3.5\" panels integrate it). I2C @ 400 kHz, addr 0x38.",
            "TOUCH_INT: open-drain, 10k pullup to V3P3.",
            "TOUCH_RST: 10k pullup to V3P3, ESP32 drives low to reset.",
            "DECOUPLING",
            "----------",
            "V3P3 near LCD VCI: 10uF + 100nF.",
            "V5P0_LCD near backlight: 22uF + 100nF.",
        ],
    },
    {
        "file": "04_rf_frontend.kicad_sch",
        "title": "RF Front-End - SMA-A/B, diplexer, 3x PE4259, 2x PE43711, 2x SPF5189Z, U.FL test pads, bias-T",
        "pins": [
            ("V3P3_RF",     "input"),
            ("GND",         "input"),
            ("ESP_UFL_RF",  "input"),
            ("CC1101_RF",   "input"),
            ("RTLSDR_RF",   "output"),
            ("ADF_RF",      "input"),
            ("SW_BAND_CTL", "input"),
            ("SW_SMA_A_CTL","input"),
            ("SW_SMA_B_CTL","input"),
            ("ATTEN_LO_LE", "input"),
            ("ATTEN_HI_LE", "input"),
            ("ATTEN_CLK",   "input"),
            ("ATTEN_DATA",  "input"),
            ("LNA_LO_EN",   "input"),
            ("LNA_HI_EN",   "input"),
            ("LNA_LO_BYP",  "input"),
            ("LNA_HI_BYP",  "input"),
            ("BIAST_EN",    "input"),
        ],
        "plan": [
            "RF FRONT-END (50 ohm CONTROLLED IMPEDANCE)",
            "==========================================",
            "Two antennas:",
            "  SMA-A: 300 MHz - 2.5 GHz   (low band)",
            "  SMA-B: 2.5 GHz - 5.8 GHz   (high band)",
            "TOPOLOGY:",
            "  ESP32-C5 u.FL --[PE4259 #1: SW_BAND]-- {2.4G route to SMA-A} | {5G route to SMA-B}",
            "  CC1101 RF -----[PE43711 #1 ATTEN_LO]----[diplexer LP <1G]------> SMA-A common pin",
            "                                                                  ^",
            "  ESP-2.4G <-[PE4259 #2: SW_SMA_A_HP]-> RTL-SDR <-[SPF5189 #1, bypass via PE4259]----+",
            "                                                                                     |",
            "                                                       diplexer HP >2G --------------+",
            "  ESP-5G   <-[PE4259 #3: SW_SMA_B  ]-> ADF4351 <-[PE43711 #2 ATTEN_HI]--> SMA-B common pin",
            "                                                                                     ",
            "ADAPTABILITY (RX side):",
            "  SPF5189Z LNAs sit ahead of each RX path (one for low band into RTL-SDR via diplexer HP,",
            "  one optional for high band). Each has a PE4259 SPDT around it for bypass when signals",
            "  are strong. Bias enable comes from LNA_LO_EN / LNA_HI_EN.",
            "BIAS-T on SMA-A:",
            "  Shunt 100uH choke from VBIAST_5V to centre conductor through 0 ohm 0402 (DNP by default).",
            "  Series 10nF DC block on the radio side. Footprint present, parts not stuffed by default.",
            "  BIAST_EN gates a P-channel FET that connects 5V to the choke -- never powered at boot.",
            "U.FL CONDUCTED-TEST PADS:",
            "  Place a u.FL connector tap (via a 33pF coupling cap to GND through a u.FL footprint",
            "  that defaults open) at: CC1101 TX out, ADF4351 RF out, ESP32 u.FL line, RTL-SDR in.",
            "  Allows lab measurement without radiating.",
            "PE4259 SUPPLY PINS:",
            "  Each PE4259 needs V3P3_RF on V+ pin (some variants), 100nF decoupling close.",
            "  Control line direct from ESP32 GPIO; no level shift needed.",
            "PE43711 SUPPLY:",
            "  V3P3_RF on VDD, 100nF decoupling. Serial 3-wire LE/CLK/DATA from ESP32, parallel-mode",
            "  P/S pin tied LOW for serial control.",
            "SPF5189Z BIAS:",
            "  Vd = 5V via 22nH bias choke + 100nF / 10nF on the supply side, output DC blocked with 10nF.",
            "  Enable via P-channel FET gated by LNA_*_EN.",
            "LAYOUT NOTES (FOR PCB SHEET):",
            "  - All RF traces 50 ohm coplanar waveguide on top layer, GND pour both sides + via fence",
            "    every lambda/20 at 5.8 GHz (~2.5 mm).",
            "  - Keep SMA-B path < 25 mm from connector to PE4259 #1.",
            "  - U.FL pigtail from ESP32-C5 module to PE4259 #1: < 50 mm, low-loss coax.",
            "  - Diplexer corner around 1.5 GHz, LC topology (e.g. Murata LFB182G45).",
        ],
    },
    {
        "file": "05_subghz.kicad_sch",
        "title": "Sub-GHz - CC1101 transceiver",
        "pins": [
            ("V3P3_RF",     "input"),
            ("GND",         "input"),
            ("SPI_RF_SCK",  "input"),
            ("SPI_RF_MOSI", "input"),
            ("SPI_RF_MISO", "output"),
            ("CC1101_CS",   "input"),
            ("CC1101_GDO0", "output"),
            ("CC1101_GDO2", "output"),
            ("CC1101_RF",   "output"),
        ],
        "plan": [
            "CC1101 - TI sub-GHz transceiver. Use the bare IC (QFN-20) plus its reference balun + matching",
            "network for 433/868/915 MHz. TI app-note DN017 recommends:",
            "  - 26 MHz crystal (CL = 10pF), 12pF/12pF load caps.",
            "  - Balun: Johanson 0433BM15A0001 or Murata LDB212G4520C-110 (band-dependent).",
            "  - Output DC block (10nF), then to PE43711 #1 in the RF front-end sheet (via CC1101_RF).",
            "DECOUPLING: 100nF + 10nF + 1nF on each VDD pin (4 places).",
            "GDO0/GDO2 GPIOs go straight to the ESP32 (used for FIFO IRQ and clock-out).",
        ],
    },
    {
        "file": "06_siggen.kicad_sch",
        "title": "Signal generator - ADF4351 PLL/VCO",
        "pins": [
            ("V3P3_RF",     "input"),
            ("V5P0_LCD",    "input"),
            ("GND",         "input"),
            ("ADF_LE",      "input"),
            ("ADF_CE",      "input"),
            ("ADF_LD",      "output"),
            ("SPI_RF_SCK",  "input"),
            ("SPI_RF_MOSI", "input"),
            ("ADF_RF",      "output"),
        ],
        "plan": [
            "ADF4351 - 35 MHz to 4.4 GHz fractional-N PLL with integrated VCO.",
            "Two supply rails per the datasheet:",
            "  - AVDD/DVDD = 3.3V (V3P3_RF)",
            "  - VVCO/VP   = 5.0V (V5P0_LCD branch through a clean LDO -- consider TPS7A4700 if",
            "                       phase-noise budget is tight; otherwise AP2112K-5.0 is OK).",
            "Reference: 25 MHz TCXO (e.g. SiTime SiT5008) on REFin, AC-coupled with 100nF.",
            "Loop filter: 4.7 kohm + 4.7nF + 100pF (canonical 50 kHz LBW, see ADIsimPLL).",
            "MUXOUT routed to ADF_LD (digital lock detect to ESP32).",
            "Output A (RF+): single-ended via 50 ohm pull-up + DC block (10nF) -> ADF_RF.",
            "Output B   : terminated 50 ohm to GND.",
            "Decoupling: 100nF + 10nF on every supply pin.",
        ],
    },
    {
        "file": "07_io.kicad_sch",
        "title": "User I/O - buttons, RGB LED, RF-active LED, MicroSD",
        "pins": [
            ("V3P3",        "input"),
            ("GND",         "input"),
            ("BTN_OK",      "output"),
            ("BTN_BACK",    "output"),
            ("BTN_UP",      "output"),
            ("BTN_DOWN",    "output"),
            ("RF_ACTIVE",   "input"),
            ("SD_CS",       "input"),
            ("SPI_RF_SCK",  "input"),
            ("SPI_RF_MOSI", "input"),
            ("SPI_RF_MISO", "output"),
        ],
        "plan": [
            "BUTTONS (4): SMD tactile, RC debounce 100nF + 10k pullup to V3P3, ESD TVS to GND.",
            "RF-ACTIVE LED: red 0603, 1k series, driven HIGH = ON. This LED is wired in HARDWARE",
            "  in series with the rf_safety arbiter logic so it cannot lie about TX state.",
            "STATUS LED: WS2812B-2020 RGB on the front panel, V3P3 + 100nF, data from a free GPIO.",
            "MICROSD: standard push-push card cage, shares SPI_RF bus, dedicated SD_CS. Card detect",
            "  pin to a free GPIO with 10k pullup. Series 33 ohm on SCK/MOSI/MISO for SI.",
        ],
    },
]


def make_uuid() -> str:
    return str(uuid.uuid4())


def render_pin(name: str, direction: str, x: int, y: int, side: str) -> str:
    """Hierarchical label inside a sub-sheet."""
    angle = {"left": 0, "right": 180, "top": 270, "bottom": 90}[side]
    return textwrap.dedent(f"""\
        \t(hierarchical_label "{name}"
        \t\t(shape {direction})
        \t\t(at {x} {y} {angle})
        \t\t(effects
        \t\t\t(font (size 1.27 1.27))
        \t\t\t(justify {'left' if side == 'left' else 'right'})
        \t\t)
        \t\t(uuid "{make_uuid()}")
        \t)
    """)


def render_sheet_pin(name: str, direction: str, x: int, y: int) -> str:
    """Pin on the sheet symbol in the root sheet."""
    return textwrap.dedent(f"""\
        \t\t(pin "{name}" {direction}
        \t\t\t(at {x} {y} 0)
        \t\t\t(effects
        \t\t\t\t(font (size 1.27 1.27))
        \t\t\t\t(justify left)
        \t\t\t)
        \t\t\t(uuid "{make_uuid()}")
        \t\t)
    """)


def make_subsheet(meta: dict) -> str:
    pins_block = []
    # Distribute pins down the left edge starting at y=30, step 5 mm.
    y = 30
    for name, direction in meta["pins"]:
        pins_block.append(render_pin(name, direction, 30, y, "left"))
        y += 5

    # Render plan as a single text block on the right of the sheet.
    plan_text = "\\n".join(meta["plan"]).replace('"', '\\"')
    title_escaped = meta["title"].replace('"', '\\"')
    plan_block = textwrap.dedent(f"""\
        \t(text "{plan_text}"
        \t\t(at 100 30 0)
        \t\t(effects
        \t\t\t(font (size 1.27 1.27))
        \t\t\t(justify left top)
        \t\t)
        \t\t(uuid "{make_uuid()}")
        \t)
    """)

    return textwrap.dedent(f"""\
        (kicad_sch
        \t(version {KICAD_VERSION})
        \t(generator "{GENERATOR}")
        \t(generator_version "{GENERATOR_VERSION}")
        \t(uuid "{make_uuid()}")
        \t(paper "A3")
        \t(title_block
        \t\t(title "{title_escaped}")
        \t\t(rev "0.1.0-dev")
        \t\t(company "WifiKiwi contributors")
        \t\t(comment 1 "Hierarchical sub-sheet -- see WifiKiwi.kicad_sch root")
        \t\t(comment 2 "Licensed under CERN-OHL-S v2")
        \t)
        \t(lib_symbols)
        """) + "".join(pins_block) + plan_block + textwrap.dedent("""\
        \t(embedded_fonts no)
        )
        """)


def make_root() -> str:
    """Root sheet that embeds all sub-sheets as hierarchical sheet symbols."""
    out = []
    out.append(textwrap.dedent(f"""\
        (kicad_sch
        \t(version {KICAD_VERSION})
        \t(generator "{GENERATOR}")
        \t(generator_version "{GENERATOR_VERSION}")
        \t(uuid "00000000-0000-0000-0000-000000000001")
        \t(paper "A2")
        \t(title_block
        \t\t(title "WifiKiwi - Top Sheet")
        \t\t(rev "0.1.0-dev")
        \t\t(company "WifiKiwi contributors")
        \t\t(comment 1 "Hierarchical root -- see sheets/*.kicad_sch")
        \t\t(comment 2 "Licensed under CERN-OHL-S v2")
        \t)
        \t(lib_symbols)
        """))

    # Place sheets in a 2-column grid.
    col_x = [40, 200]
    row_y_start = 30
    row_step = 60
    for idx, meta in enumerate(SHEETS):
        x = col_x[idx % 2]
        y = row_y_start + (idx // 2) * row_step
        sheet_uuid = make_uuid()
        # Render sheet pins from the meta -- distributed down the left side.
        pin_blocks = []
        py = y + 5
        for name, direction in meta["pins"]:
            pin_blocks.append(render_sheet_pin(name, direction, x, py))
            py += 2.54  # 100 mil grid
        sheet = textwrap.dedent(f"""\
            \t(sheet
            \t\t(at {x} {y})
            \t\t(size 140 {max(40, len(meta['pins']) * 2.54 + 10):.2f})
            \t\t(exclude_from_sim no)
            \t\t(in_bom yes)
            \t\t(on_board yes)
            \t\t(dnp no)
            \t\t(fields_autoplaced yes)
            \t\t(stroke
            \t\t\t(width 0.1524)
            \t\t\t(type solid)
            \t\t)
            \t\t(fill (color 0 0 0 0.0000))
            \t\t(uuid "{sheet_uuid}")
            \t\t(property "Sheetname" "{meta['title'].replace('"', chr(92) + chr(34))}"
            \t\t\t(at {x} {y - 0.7112} 0)
            \t\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
            \t\t)
            \t\t(property "Sheetfile" "sheets/{meta['file']}"
            \t\t\t(at {x} {y + max(40, len(meta['pins']) * 2.54 + 10) + 0.7112:.4f} 0)
            \t\t\t(effects (font (size 1.27 1.27)) (justify left top))
            \t\t)
            """)
        sheet += "".join(pin_blocks) + "\t)\n"
        out.append(sheet)

    # sheet_instances: declare each sheet's path.
    out.append("\t(sheet_instances\n")
    out.append('\t\t(path "/" (page "1"))\n')
    out.append("\t)\n")
    out.append("\t(embedded_fonts no)\n")
    out.append(")\n")
    return "".join(out)


def main() -> None:
    SHEETS_DIR.mkdir(exist_ok=True)
    for meta in SHEETS:
        path = SHEETS_DIR / meta["file"]
        path.write_text(make_subsheet(meta))
        print(f"wrote {path.relative_to(HERE)}")
    ROOT_SCH.write_text(make_root())
    print(f"wrote {ROOT_SCH.relative_to(HERE)}")


if __name__ == "__main__":
    main()
