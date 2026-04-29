# Firmware build

🚧 **TBD** — this guide will be written once the firmware fork is in place
and reliably builds on ESP32-C5.

## Outline (planned)

1. Install ESP-IDF v5.4 or newer with ESP32-C5 target support.
2. `git clone --recursive https://github.com/ariplayz/WifiKiwi.git`
3. `cd firmware && idf.py set-target esp32c5 && idf.py menuconfig`
4. `idf.py build`
5. `idf.py -p /dev/ttyUSB0 flash monitor`

## Alternative: PlatformIO

PlatformIO support for ESP32-C5 is being tracked upstream. When available,
a `platformio.ini` will be added.
