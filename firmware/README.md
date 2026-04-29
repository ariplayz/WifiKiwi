# Firmware

🚧 **TBD** — firmware sources will live here, structured as an ESP-IDF
project targeting the ESP32-C5 (RISC-V).

## Layout

```
firmware/
├── CMakeLists.txt        ESP-IDF top-level
├── sdkconfig.defaults    ESP32-C5 target, PSRAM enabled, etc.
├── partitions.csv        OTA + storage partitions
├── main/                 entry point, app dispatcher
├── components/           ports of upstream code (one component per fork)
│   ├── bruce_ui/         from pr3y/Bruce
│   ├── marauder_wifi/    from justcallmekoko/ESP32Marauder
│   ├── mayhem_dsp/       from portapack-mayhem/mayhem (FFT/waterfall)
│   ├── cc1101/           sub-GHz driver
│   ├── adf4351/          PLL signal generator driver
│   ├── pe4259_switch/    SPDT RF switch control
│   ├── pe43711_atten/    digital step attenuator control
│   ├── spf5189_lna/      LNA bias + bypass control
│   ├── ili9488_lvgl/     display driver
│   └── ft6336_touch/     touch driver
├── ui/                   LVGL screens (home tiles, status bar, app screens)
└── apps/
    ├── wifi/             2.4 + 5 GHz attack suite
    ├── ble/              BLE scan/spam/GATT
    ├── subghz/           CC1101 capture/replay
    ├── sdr/              RTL-SDR + waterfall
    ├── siggen/           ADF4351 UI
    └── tools/            spectrum sweep, file browser, attenuator/LNA UI
```

## Build (planned)

```bash
git clone --recursive https://github.com/ariplayz/WifiKiwi.git
cd WifiKiwi/firmware
idf.py set-target esp32c5
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

Requires ESP-IDF v5.4 or newer with ESP32-C5 target.
