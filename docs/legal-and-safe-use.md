# Legal and safe-use guide

> **Read this before powering the device.**

WifiKiwi is a research tool. Like any radio transmitter, it is subject to
laws that vary by country. Using it improperly is a serious legal risk —
in many jurisdictions a felony — and can disrupt safety-critical systems
(Wi-Fi calling and 911, medical telemetry, alarms, industrial controls,
aviation). The project's design choices below are made specifically to
keep WifiKiwi within the lines.

## Design constraints

WifiKiwi is intentionally **not** capable of:

- Broadband jamming or denial-of-service across whole bands.
- Transmitting at power levels above the stock module outputs (≤ +20 dBm).
  No high-power PA is fitted, and the PCB is not designed to accept one
  (no reserved footprint, no bias rails, no PA-grade trace impedance, no
  thermal copper, no power-budget headroom).
- Operating in the 6 GHz Wi-Fi 6E/7 band — no microcontroller-class chip
  exists for it.
- Continuous wideband transmit. The only "wideband" transmit path is the
  ADF4351 single-tone signal generator, intended for filter
  characterization and antenna sweeps, not for jamming or interference.

## Recommended use

1. **Faraday cage.** Operate inside a properly-sealed shielded enclosure
   (60 dB+ isolation at 2.4–5 GHz). Cheap consumer "Faraday bags" are
   usually inadequate; build or buy a real cage.
2. **Owned equipment only.** Targets must be devices and APs you own and
   have full administrative authority over. The firmware enforces a
   user-defined BSSID/MAC allowlist on attack screens.
3. **Conducted-RF testing where possible.** Use the U.FL test pads on the
   PCB to wire the radio outputs through coax + lab attenuators directly
   to the device under test, with no antennas at all. This is the safest
   and most reproducible way to do Wi-Fi protocol stress testing.
4. **Country code + regulatory mode.** Set the Wi-Fi country code in
   Settings (defaults to MX). The C5 will respect channel and power
   restrictions for that region.
5. **Don't carry it powered-on outside the cage.** The "RF active" red LED
   exists to remind you. The hard power slide switch kills the boost
   converter completely.

## Country-specific notes

### Mexico (IFT)

- Relevant authority: **Instituto Federal de Telecomunicaciones (IFT)**.
- Relevant regulation: **Cuadro Nacional de Atribución de Frecuencias
  (CNAF)** plus **NOM-208-SCFI-2016** for short-range devices.
- 2.4 GHz ISM (2400–2483.5 MHz) and 5 GHz UNII bands are open for
  unlicensed use under power and DFS rules; the C5 with stock module
  output stays within these limits.
- Sub-GHz: 902–928 MHz ISM is available; the CC1101 in default
  configuration operates within it. The 433 MHz region requires more care
  in MX — check current IFT rules for your band of operation.
- **Jamming**, **eavesdropping on networks you do not own**, and
  **operating uncertified high-power transmitters** are all prohibited
  and can carry administrative and criminal penalties.

### United States (FCC)

- Operating any jammer is illegal under 47 U.S.C. §§ 301, 302a, 333. Civil
  penalties up to ~$112k per violation; criminal exposure exists.
- 2.4 / 5 GHz ISM/UNII unlicensed use under Part 15.247 / 15.407.
- 902–928 MHz ISM under Part 15.249.
- Operating against networks you do not own may violate the Computer
  Fraud and Abuse Act (18 U.S.C. § 1030) and the Wiretap Act
  (18 U.S.C. § 2511).

### European Union

- Radio Equipment Directive (2014/53/EU). Unlicensed use of 2.4 GHz
  (ETSI EN 300 328), 5 GHz (EN 301 893), and sub-GHz SRD bands per
  EN 300 220.
- National regulators enforce; jammers are uniformly illegal across
  member states.

### Other jurisdictions

You are responsible for checking your local rules. Most countries
prohibit jammers and unauthorized transmitters categorically.

## What this guide is not

This guide is **not legal advice.** It is a summary written by hobbyists.
If you intend to operate WifiKiwi for paid security work, in a regulated
environment, or anywhere near safety-critical systems, consult a lawyer
and your local regulator first.
