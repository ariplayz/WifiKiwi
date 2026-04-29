# Contributing to WifiKiwi

Thanks for your interest. This project is open-source and welcomes
contributions from anyone who agrees with its goals and constraints.

## Project goals (and hard limits)

WifiKiwi is a research and education tool for legal Wi-Fi/RF testing on
**owned equipment** inside a **shielded enclosure**. The project will not
accept contributions that:

- Add jamming, broadband interference, or denial-of-service capabilities
  against bands the device is not authorized to operate in.
- Add high-power PAs or footprint/scaffolding (bias networks, trace
  pre-routing, thermal copper, power-budget headroom) for adding one later.
- Disable, weaken, or remove the safety/legal modal confirmations in the
  firmware UI.
- Add features specifically designed to attack networks or devices the user
  does not own (e.g. mass deauth without an explicit allowlist).

These are not negotiable. PRs that violate them will be closed without merge.

## Developer Certificate of Origin (DCO)

We use the [DCO](https://developercertificate.org/) instead of a CLA. Sign
every commit:

```
git commit -s -m "your message"
```

This appends a `Signed-off-by: Your Name <you@example.com>` trailer that
attests you have the right to submit the contribution under the project's
licenses.

## Licenses

By contributing you agree your contribution is licensed under:

- **GPL-3.0-or-later** for code in `firmware/`
- **CERN-OHL-S v2** for files in `hardware/`
- **CC-BY-SA 4.0** for files in `docs/`

## Workflow

1. Open or claim an issue.
2. Branch from `main`: `git checkout -b feat/short-description`.
3. Keep PRs small and focused — one logical change per PR.
4. Run the local checks before pushing:
   - Firmware: `cd firmware && pio run` (or `idf.py build`)
   - Hardware: open the KiCad project and run ERC + DRC; export gerbers.
   - Markdown: `markdownlint docs/`.
5. Sign off your commits (`-s`).
6. Open a PR; CI must be green.
7. At least one maintainer review is required.

## Code style

- **C/C++** (firmware): follow `.clang-format` in `firmware/` (LLVM style,
  4-space indent, 100-col).
- **Python** (build scripts): `black`, `ruff`.
- **KiCad**: 8.0+ project format, libraries vendored under
  `hardware/kicad/lib/`.

## Reporting security issues

Please do **not** open public issues for security vulnerabilities. Email
the maintainers privately first. We follow coordinated disclosure.
