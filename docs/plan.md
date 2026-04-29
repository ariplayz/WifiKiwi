# WifiKiwi — Multi-Radio Wi-Fi / RF Research Tool

## Problem statement

A handheld, battery-powered, touchscreen RF research device for **AP and device
security testing inside a Faraday cage against hardware the operator owns**.
**Open-source** (firmware GPLv3, hardware CERN-OHL-S v2 — see Licensing
section). Built around an **ESP32-C5-WROOM-1U** module (dual-band
2.4/5 GHz Wi-Fi 6 + BLE 5.3, mass production, ~$3.18 per Espressif's product
list, see `esp32-c5.csv` in repo) plus several discrete radio modules,
fabricated as a single PCB through JLCPCB.

**Explicit non-goals (designed out, not just "discouraged"):**
- No broadband jamming.
- **No high-power PA stages on any path** (output kept at module-stock
  levels, ≤ +20 dBm, intended for use inside a shielded enclosure). This
  includes no reserved footprint, bias supply, or trace pre-routing for a
  future PA — the PCB is not designed to "accept" one. Forking the design
  to add one is the user's prerogative under CERN-OHL-S, but the upstream
  reference design will not include the scaffolding.
- **No 6 GHz operation.** No microcontroller-class chip exists for 6 GHz
  Wi-Fi 6E/7. Dropped from scope per user.
- No continuous 1 MHz – 6 GHz arbitrary TX. The wideband path is RX-only
  (RTL-SDR) plus a CW signal-generator (ADF4351, single tone) on TX.

## Honest scope vs. original ask

The original ask was "HackRF-Pro-class 1 MHz – 6 GHz TX+RX under $150."
That's not achievable — wideband SDR silicon alone (AD9361/LMS7002M class)
exceeds the budget. The plan below is the closest realistic build at
~$130–150 BOM: a multi-radio tool with **real 2.4 GHz AND 5 GHz Wi-Fi 6**
(thanks to ESP32-C5), sub-GHz capture/replay, wideband RX, and CW signal
generation.

## Architecture

```
       ┌────────────────────────────────────────────┐
       │   ESP32-C5-WROOM-1U  (8 MB flash + 8 PSRAM)│
       │   Wi-Fi 6 dual-band 2.4/5 GHz, BLE 5.3      │
       └─┬──────┬──────┬──────┬──────┬──────────────┘
       u.FL    SPI    SPI    SPI    USB-host (via CH334 hub)
         │      │      │      │      │
         │   ┌──┴───┐ ┌┴────┐ │   ┌──┴────────────┐
         │   │CC1101│ │ADF  │ │   │ RTL-SDR v4    │
         │   │sub-G │ │4351 │ │   │ (internal USB)│
         │   │300-  │ │35M- │ │   │ 500k–1.75 GHz │
         │   │928M  │ │4.4G │ │   │  RX-only      │
         │   └──┬───┘ └──┬──┘ │   └──────┬────────┘
         │      │        │    │          │
         │      │        │    │          │
         │      │        │   ILI9488     │
         │      │        │   3.5" touch  │
         │      │        │               │
         ▼      ▼        ▼               ▼
   ┌─────────────────────────────────────────────────┐
   │                RF SWITCH MATRIX                  │
   │  ┌─────────────────────┐  ┌──────────────────┐  │
   │  │ Diplexer DPX-1G     │  │ PE4259 SPDT #2   │  │
   │  │  LP < 1 GHz (CC1101)│  │  C5-5GHz ↔ ADF   │  │
   │  │  HP > 2 GHz         │  │ (high band)      │  │
   │  └─────────┬───────────┘  └────────┬─────────┘  │
   │            │ HP port                │            │
   │  ┌─────────┴───────────┐            │            │
   │  │ PE4259 SPDT #1      │            │            │
   │  │  C5-2.4G ↔ RTL-SDR  │            │            │
   │  └─────────┬───────────┘            │            │
   │   combined low+HP via diplexer      │            │
   └────────────┬────────────────────────┴────────────┘
                ▼                         ▼
              SMA-A                     SMA-B
        "Low"  300 MHz – 2.5 GHz    "High"  2.5 – 5.8 GHz
        Antenna: wideband           Antenna: 2.4/5 GHz
        log-periodic or             dual-band Wi-Fi
        2.4 GHz dipole that         dipole, 5 dBi
        also works at sub-GHz       (or 5 GHz-tuned)

   Plus: microSD (SPI), TP4056 USB-C charger, MT3608 5V boost,
         18650 holder, AMS1117-3.3 LDO, power switch, status LEDs
```

### The 2 antennas (revised per user request)
| # | SMA | Band | Sources routed to it | Recommended antenna |
|---|-----|------|----------------------|---------------------|
| A | SMA-A | **300 MHz – 2.5 GHz** ("low + 2.4") | CC1101 sub-GHz (always-on, via diplexer LP), and one of {ESP32-C5 in 2.4 GHz mode, RTL-SDR RX} via SPDT #1 then diplexer HP | Wideband log-periodic 400 MHz–2.7 GHz, **or** a 2.4 GHz dipole (limited sub-GHz performance), **or** swappable: 915 MHz whip ↔ 2.4 GHz dipole depending on band of interest |
| B | SMA-B | **2.5 – 5.8 GHz** ("high") | One of {ESP32-C5 in 5 GHz mode, ADF4351 TX} via SPDT #2 | Dual-band 2.4/5 GHz dipole 5 dBi, or 5 GHz-tuned dipole 7 dBi |

### How the switching/diplexing works

- **Diplexer DPX-1G** (e.g. Mini-Circuits LFCN-1000 + HFCN-1810 pair, or a
  single-package LTCC diplexer such as Anaren BD0810N50100AHF): cleanly
  separates the < 1 GHz path (CC1101) from the > 2 GHz path on antenna A so
  the sub-GHz radio doesn't see the 2.4 GHz energy and vice-versa. Both can
  be active simultaneously.
- **PE4259 SPDT #1** sits on the diplexer's high port and selects between the
  C5's 2.4 GHz output and the RTL-SDR's RX input (when the user wants
  wideband RX in the 2.4 GHz region). Firmware-controlled via one GPIO.
- **PE4259 SPDT #2** sits in front of SMA-B and selects between the C5's
  5 GHz output and the ADF4351's TX output (which can reach up to 4.4 GHz).
- The RTL-SDR can also be tapped to SMA-A's low side via the diplexer for
  the < 1 GHz region — but to keep the switch matrix simple this revision
  routes RTL-SDR only through SPDT #1 (HP path). Sub-GHz RX of arbitrary
  signals is done via CC1101 in sniff mode instead.
- The C5 has a **single dual-band RF pin**. To send it to either SMA-A (2.4)
  or SMA-B (5) we add **PE4259 SPDT #3** at the C5's u.FL output that picks
  which switch matrix it feeds. This is a third SPDT in the path —
  acceptable insertion loss (~0.5 dB at 2.4 GHz, ~0.8 dB at 5 GHz per
  PE4259 datasheet).

### Trade-offs of the 2-antenna design
- **Pro**: simpler enclosure, fewer SMA cutouts, cleaner aesthetic, aligns
  with user's request.
- **Con**: more RF-switch complexity on the PCB. Three PE4259s + a diplexer
  add insertion loss (~1.5–2 dB cumulative on some paths) which slightly
  reduces sensitivity and TX EIRP. Acceptable inside a Faraday cage.
- **Con**: no truly broadband antenna covers 300 MHz – 5.8 GHz well; a
  log-periodic gets close on the low side but is physically large. The
  realistic answer is a swappable-element low antenna (915 MHz whip for
  sub-GHz work, 2.4 GHz dipole for Wi-Fi work) — both screw onto SMA-A.

## Key decisions / trade-offs

- **MCU**: **ESP32-C5-WROOM-1U-N8R8** (~$3.18, mass production per Espressif
  CSV in repo). Replaces the earlier Arduino Nano ESP32 plan. Reasons:
  - Native dual-band 2.4 GHz + 5 GHz Wi-Fi 6 (HT20, up to 150 Mbps) — the
    only sub-$5 module on Earth that does this today.
  - BLE 5.3, RISC-V single-core @ 240 MHz, 384 KB SRAM, 8 MB flash, 8 MB PSRAM.
  - "-1U" variant has u.FL connector → external antenna path (required for the
    PE4259 switch to two SMAs). The "-1" variant has a PCB antenna instead.
  - Trade-off: single-radio time-shared between bands; can't TX 2.4 and 5 GHz
    simultaneously. Acceptable for this use case.
  - User will need to deal with longer Espressif lead times (4–8 weeks direct)
    or buy the dev kit (ESP32-C5-DevKitC-1) on Amazon for prototyping.
- **Sub-GHz**: CC1101 module (300–348 / 387–464 / 779–928 MHz). OOK + 2-FSK +
  GFSK + MSK. Cheap, well-supported.
- **TX adaptability via attenuation, not amplification**: each TX path gets
  a **PE43711 7-bit digital step attenuator** (0–31.75 dB, 0.25 dB steps,
  DC–6 GHz). MCU-controlled over a 3-wire serial bus. Lets the user
  precisely *reduce* output power for known-RSSI tests, rate-vs-signal
  characterization in the cage, or conducted-RF measurements. ~$3 each.
- **RX sensitivity boost via LNAs**: each RX path gets an **SPF5189Z LNA**
  (~+18 dB gain, NF ≈ 0.6 dB, 50 MHz – 4 GHz, ~$1.50 each) on a switchable
  bypass — MCU-controlled SPDT bypass so the LNA can be removed from the
  path when input signals are strong (avoids saturation). Improves
  receive-side sensitivity for sniffing/monitoring without changing TX
  emissions.
- **Conducted-RF test pads**: 2 × U.FL pads at the radio outputs (before the
  switch matrix) so the user can solder on a pigtail and connect to a
  spectrum analyzer, VNA, or another AP via coax + lab-grade attenuators
  for **fully-conducted (non-radiating) testing** — the ideal way to do
  aggressive Wi-Fi protocol work.
- **Bias-T on SMA-A** (10 µH choke + 100 nF DC block + jumper to enable):
  optionally feeds 5 V at up to 100 mA up the antenna coax for powering an
  external LNA at the antenna.
- **Wideband signal generation**: ADF4351 module (35 MHz – 4.4 GHz CW,
  single tone). Useful for filter characterization, antenna sweeps, RX
  calibration. **TX-only, single tone, not modulated** — explicitly not a
  jammer.
- **Wideband RX**: RTL-SDR v4 dongle, socketed inside the case via internal
  USB-A. ESP32-C5 → CH334 USB hub IC → internal-A receptacle. Hot-swappable.
  500 kHz – 1.75 GHz IQ RX.
- **RF switches**: 2 × PE4259 SPDT.
  - #1 routes ESP32-C5 u.FL between SMA2 (2.4 GHz) and SMA3 (5 GHz).
  - #2 routes SMA4 between RTL-SDR RX input and ADF4351 TX output.
- **Display**: 3.5" ILI9488 SPI capacitive-touch (FT6336). LVGL-driven UI.
- **Power**: single 18650 (3000 mAh) + TP4056 USB-C charge IC + MT3608 boost
  to 5 V (display backlight + RTL-SDR via internal USB) + AMS1117-3.3 LDO for
  3.3 V rail. Hard-switch on input.
- **PCB**: 4-layer JLCPCB (signal / GND / 3V3 / signal). 4-layer is needed
  for clean 50 Ω microstrip on the 5 GHz feed, controlled impedance, and
  proper ground returns. ~$10 for 5 boards at JLC.
- **5 GHz layout discipline**: keep the C5 u.FL → PE4259 → SMA3 trace as
  short and straight as possible (target < 25 mm), with continuous ground
  reference, ground stitching every λ/20, and no via discontinuities. This
  is the trickiest part of the layout and gets its own dedicated todo.
- **Enclosure**: 3D-printed (FreeCAD), SMA cutouts, screen bezel, USB-C
  passthrough.

## Touchscreen & physical controls

### Display
- **Panel**: 3.5" IPS LCD, 480×320, ILI9488 driver, **capacitive multi-touch
  via FT6336U** over I²C. Common on AliExpress/LCSC for ~$12–14.
- **Interface**: 4-wire SPI to ESP32-C5 at 40 MHz (LCD) + I²C @ 400 kHz
  (touch). Backlight on a PWM-controlled MOSFET for brightness control and
  battery savings.
- **Why this part**: best price/feature ratio in 3.5" range; ILI9488 is
  rock-solid in LVGL and TFT_eSPI; FT6336 has a mature ESP-IDF driver.
- **Alternatives considered**:
  - 2.8" ILI9341 (smaller, cheaper ~$8) — rejected for being too small for
    a Mayhem-style waterfall.
  - 4.0" ST7796 (slightly bigger, similar price) — viable backup if ILI9488
    stock dries up; pin-compatible footprint with a jumper option.

### Physical controls (in addition to touch)
The PortaPack and Marauder both pair touch with hard buttons because typing
on a 3.5" capacitive screen during a capture is miserable. Plan mirrors that:
- **5-way navigation joystick** (SKQUCAA010 or similar tactile 5-way) —
  primary up/down/left/right/select for menu use without touching the screen.
- **2 × tactile side buttons** — `BACK` and `OK` shortcuts.
- **1 × dedicated `MODE` button** — long-press cycles top-level apps
  (Wi-Fi / Sub-GHz / SDR / Settings) à la PortaPack's hardware button.
- **Hard power slide switch** at the side (kills the boost converter; charge
  still works over USB-C while off).
- **Status LEDs** (3): power, charging, RF-active (red, mandatory — visual
  reminder that something is transmitting).

## UI design

### Look-and-feel inspirations (now: direct fork/port permitted under GPLv3)
Project is open-source, so we can do more than clone aesthetics — we can
**fork and port real code** from these GPL projects:
- **PortaPack H2 / Mayhem** (GPLv3, https://github.com/portapack-mayhem/mayhem):
  source the home-screen tile system, app-switcher framework, FFT/waterfall
  rendering pipeline, and band-plan databases. Mayhem is C++ for a Cortex-M4
  + LPC43xx — we port the UI layer, not the radio drivers, since our SoC and
  SDR architecture differ.
- **ESP32 Marauder / ESP32-DIV V2** (GPLv3, https://github.com/justcallmekoko/ESP32Marauder):
  source the entire 2.4 GHz Wi-Fi attack suite (deauth, beacon spam, probe,
  PMKID, evil-twin, packet monitor) and the menu system. Marauder already
  runs on ESP32-S3; porting to ESP32-C5 is mostly toolchain (RISC-V vs
  Xtensa) plus enabling the C5's 5 GHz radio path (new — Marauder doesn't
  support 5 GHz today; we add it).
- **Bruce firmware** (https://github.com/pr3y/Bruce, GPLv3) — also worth
  cherry-picking from; it already has BLE-spam, sub-GHz support via CC1101,
  RF attack modules, and a polished LVGL UI on ESP32-S3. Bruce is probably
  the closest existing template to what WifiKiwi will be.

**Recommended approach**: start from a fork of **Bruce**, retarget the build
to ESP32-C5 (RISC-V) via ESP-IDF v1.x, add the 5 GHz Wi-Fi feature set from
Marauder concepts, layer in PortaPack-style waterfall for the SDR app.

### Framework
- **LVGL 9.x** running on ESP-IDF v1.x (the IDF version supporting C5 per
  Espressif's CSV).
- **TFT_eSPI**-style direct SPI driver wrapped behind LVGL's display port for
  max throughput; double-buffered with PSRAM-resident framebuffers.
- **lv_freetype** for one nice TTF (e.g. Inter or JetBrains Mono); fallback
  to the built-in Montserrat fonts to save flash if needed.

### Screen map (top-level)

```
┌──────────────────────────────────────────────────────────┐
│ ⚡73%   📡SD   🕑21:04   ⚠ FARADAY-CAGE MODE             │  ← persistent
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│   │   📶   │  │   📡   │  │   🎚   │  │   🛠   │        │
│   │ Wi-Fi  │  │Sub-GHz │  │  SDR   │  │ Tools  │        │
│   └────────┘  └────────┘  └────────┘  └────────┘        │
│                                                          │
│   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│   │   🔵   │  │   🎯   │  │   📜   │  │   ⚙   │        │
│   │  BLE   │  │SignalGen│ │  Logs  │  │Settings│        │
│   └────────┘  └────────┘  └────────┘  └────────┘        │
└──────────────────────────────────────────────────────────┘
```

### App-level screens (one per tile)

| App | Key screens | Notes |
|---|---|---|
| **Wi-Fi** | AP scan list (2.4 + 5 GHz), client list, channel hopper, deauth, beacon spam, evil-twin, PMKID capture, packet monitor | Every TX action gates behind a modal "Faraday-cage confirmation" requiring a hold-to-confirm gesture (Marauder pattern, hardened). Targets restricted to a user-defined allowlist of BSSIDs stored on SD. |
| **BLE** | Scanner, advertiser, BLE-spam (Apple/Android/Samsung popups for owned device test), GATT explorer | Same confirmation gate. |
| **Sub-GHz** | Frequency analyzer (CC1101 RSSI sweep), capture (OOK/FSK), replay, raw register editor, saved-signal browser | PortaPack-style band-plan list (315/433/868/915 presets). |
| **SDR** | RTL-SDR waterfall (offloaded — see "Notes / risks"), spectrum, audio demod (NFM/AM/WBFM) — likely streamed to a host PC with `rtl_tcp` and rendered there; on-device shows control + simple FFT. | Most realistic answer: on-device shows tuning + signal-level meter; full waterfall on companion app. |
| **SignalGen** | ADF4351 frequency entry (35 MHz – 4.4 GHz), output power (-4/-1/+2/+5 dBm), sweep mode, mute. | Big red "OUTPUT ACTIVE" banner whenever PE4259 routes ADF4351 to an antenna. |
| **Tools** | Spectrum sweep using CC1101+RTL-SDR data, antenna SWR helper (rough), file browser on SD, hex viewer for captures | |
| **Logs** | Per-app log tail, export to SD, time-stamped events. | |
| **Settings** | Wi-Fi country code (MX), screen brightness, button mapping, allowlist editor, OTA update, factory reset. | Country code defaults to MX; channels 12/13/14 enabled per IFT regs. |

### Visual style
- Theme: dark navy background `#0B1220`, accent cyan `#22D3EE`, warning
  amber `#F59E0B`, danger red `#EF4444` for any TX-active indicator.
- Font: JetBrains Mono 14 for body, Inter 18 for titles.
- All TX-active screens have a 4-pixel red border drawn by LVGL while the
  PA path is energized, so it's obvious at a glance.

### LVGL screen flow
```
boot splash → home tiles → app screen → modal confirm → action screen
                              ↑                              │
                              └──────── BACK button ─────────┘
```

## Enclosure / case

### Form factor
PortaPack-inspired: handheld "brick" ~115 × 75 × 28 mm, screen on the front
upper two-thirds, joystick + hardware buttons on the front lower third, two
SMA antennas on the top, USB-C + power switch on one side, battery door on
the back.

### Construction
- **3D-printed** in two halves (front bezel + rear shell), designed in
  **FreeCAD 1.0**. Source `.FCStd` files committed to the repo.
- Material: PETG (preferred, more heat-tolerant than PLA, easy to print) or
  ABS for production-feel units.
- Wall thickness 2.0 mm, M2.5 brass heat-set inserts at four corners + two
  middle posts.
- Fit tolerance: 0.2 mm clearance for the PCB, captive PCB on standoffs.
- Antenna SMAs on the **top edge**, spaced 30 mm apart so the two antennas
  don't physically clash when both are vertical whips.
- Belt-clip mount on the rear (optional bolt-on).

### Internal layout
```
front (top → bottom)              back (top → bottom)
┌─────────────────────────┐       ┌─────────────────────────┐
│ SMA-A    SMA-B          │       │  vent slots             │
│ ┌─────────────────────┐ │       │ ┌─────────────────────┐ │
│ │   3.5" touchscreen  │ │       │ │   18650 cell        │ │
│ │   480 × 320         │ │       │ │   (door clips off)  │ │
│ │                     │ │       │ │                     │ │
│ └─────────────────────┘ │       │ └─────────────────────┘ │
│  ◀ ▲ ▶  OK  BACK MODE   │       │     belt-clip boss      │
└─────────────────────────┘       └─────────────────────────┘
left side: USB-C, power slide.   right side: microSD slot, internal
                                 RTL-SDR USB access door (opens for
                                 swap), 3-LED light pipe.
```

### Case features
- **Light pipes** (clear PETG inserts) over each status LED.
- **Speaker grille** over a tiny 8 Ω piezo for UI beeps + audio demod
  (driven from an MCP6L02 op-amp + GPIO PWM).
- **Lanyard slot** on the bottom edge.
- **Faraday-cage badge**: front-panel silkscreen / printed label "FOR USE
  IN SHIELDED ENVIRONMENT — MX IFT AUTHORIZED RESEARCH ONLY" — both as a
  legal posture statement and as a deterrent against casual misuse.

## Estimated BOM (single-unit, JLC + LCSC + AliExpress)

| Item | ~USD |
|---|---|
| Arduino Nano ESP32 | 22 |
| CC1101 module | 3 |
| NRF24L01+PA/LNA module | 4 |
| ADF4351 module | 12 |
| RTL-SDR v4 dongle | 30 |
| ILI9488 3.5" touchscreen | 14 |
| PE4259 SPDT RF switch + matching | 2 |
| SMA connectors ×4 + pigtails | 8 |
| 18650 + holder + TP4056 + MT3608 + switch | 8 |
| PCB (5 pcs, 4-layer, JLC) | 10 |
| Passives, headers, USB-C, misc | 8 |
| 4 × antennas (sub-GHz whip, 2× 2.4 GHz dipole, wideband telescopic) | 20 |
| 3D-printed enclosure (filament cost) | 3 |
| **Total** | **~144** |

## High-level phases

1. **Schematic capture** in KiCad 8 — symbols, net plan, power tree.
2. **Module footprints + custom symbols** for CC1101 / NRF24 / ADF4351 / Nano
   ESP32 / ILI9488 / RTL-SDR USB header / PE4259.
3. **PCB layout** — 4-layer stackup, RF traces (50 Ω microstrip on top to GND
   on layer 2), keep-out zones, ground stitching, antenna feed lines.
4. **DRC + impedance check + 3D review**, panelize, generate JLC-compatible
   gerbers + drill + pick-and-place + BOM.
5. **Firmware skeleton** — Arduino-ESP32 core, LVGL UI, driver stubs for each
   radio, RF-switch control, settings persistence on SD/NVS.
6. **Firmware features** — Wi-Fi attack suite (deauth/beacon/probe/evil-twin
   /PMKID), CC1101 capture+replay, NRF24 scan, ADF4351 frequency control,
   RTL-SDR waterfall (rtl_tcp client to a host PC, since live FFT on ESP32 is
   marginal).
7. **Enclosure** in FreeCAD, print, fit-check.
8. **Documentation** (private, not open-source per user) — schematic PDF, BOM
   CSV, assembly guide, firmware build instructions, legal-use notice
   reiterating Faraday-cage / owned-equipment-only scope.

## Notes / risks

- **ESP32-C5 USB-host + RTL-SDR is non-trivial.** The C5 has USB Serial/JTAG
  but full USB-host stack support in ESP-IDF v1.x for the C5 is still
  maturing, and existing rtl-sdr libraries assume libusb on a Linux host.
  Realistic plan: either (a) the RTL-SDR is read by a tethered phone/PC
  over Wi-Fi using `rtl_tcp` running on the host, or (b) drop on-board
  RTL-SDR and provide a USB-C breakout so the user plugs it into a laptop.
  Decision deferred to a spike (todo `fw-rtlsdr-decision`).
- **ADF4351 phase noise is poor** — fine for stimulus, not a clean LO. Don't
  oversell it as an SDR LO.
- **Antenna 4 (wideband)** is a compromise; a true 70 MHz – 6 GHz antenna is
  large. A telescopic whip + a separate small discone for indoor use is the
  realistic answer.
- **Legal posture**: device is intended for use only inside a Faraday cage on
  user-owned equipment. Mexican IFT rules (Ley Federal de
  Telecomunicaciones y Radiodifusión, art. 145+) prohibit unauthorized
  emissions outside the ISM bands; the design is constrained to module-stock
  power and ISM/sub-GHz bands precisely to keep accidental misuse hard.
  Documentation will state this scope explicitly.

## Licensing

The project is **open-source**, dual-licensed by component type:

- **Firmware** (`/firmware/`): **GPLv3** (required because we fork code from
  Marauder, Bruce, and PortaPack/Mayhem, all GPLv3). All firmware sources,
  build scripts, partition tables, and configs ship under GPLv3.
  - `LICENSE` file in repo root contains the GPLv3 text.
  - Each upstream code import keeps its original copyright headers and is
    listed in `THIRD_PARTY_NOTICES.md` with project name, upstream URL,
    license, and the commit/version forked from.
- **Hardware design** (`/hardware/`): **CERN Open Hardware Licence v2 –
  Strongly Reciprocal (CERN-OHL-S v2)** — the hardware equivalent of GPL.
  Covers KiCad schematics, PCB layout, gerbers, BOM, mechanical FreeCAD
  files, 3D-printable STLs.
- **Documentation** (`/docs/`): **CC-BY-SA 4.0** so guides, photos, and
  diagrams can be remixed with attribution.

Contributors agree to the project's `CONTRIBUTING.md` Developer Certificate
of Origin (DCO sign-off, like the Linux kernel) — no CLA.

### Repository layout
```
WifiKiwi/
├── LICENSE                  GPLv3 (firmware default)
├── LICENSES/
│   ├── GPL-3.0.txt
│   ├── CERN-OHL-S-v2.txt
│   └── CC-BY-SA-4.0.txt
├── README.md                project overview + quick start
├── THIRD_PARTY_NOTICES.md   upstream attribution for forked code
├── CONTRIBUTING.md          DCO + code-style guide
├── CODE_OF_CONDUCT.md       Contributor Covenant 2.1
├── docs/                    CC-BY-SA 4.0
│   ├── getting-started.md
│   ├── hardware-assembly.md
│   ├── firmware-build.md
│   ├── ui-guide.md
│   ├── legal-and-safe-use.md
│   ├── images/
│   └── schematics/          rendered PDFs of the KiCad schematic
├── hardware/                CERN-OHL-S v2
│   ├── kicad/               .kicad_pro, .kicad_sch, .kicad_pcb
│   ├── gerbers/             JLC-ready zip per revision
│   ├── bom/                 BOM CSV with LCSC part numbers
│   ├── cpl/                 pick-and-place CSV
│   └── enclosure/           FreeCAD .FCStd + exported .step + .stl
├── firmware/                GPLv3
│   ├── platformio.ini       (or CMakeLists.txt for ESP-IDF)
│   ├── src/
│   ├── components/          forked drivers (CC1101, ADF4351, FT6336…)
│   ├── ui/                  LVGL screens
│   └── apps/                wifi/, ble/, subghz/, sdr/, siggen/, tools/
└── .github/
    ├── workflows/           CI: build firmware, run KiCad ERC/DRC
    └── ISSUE_TEMPLATE/
```
