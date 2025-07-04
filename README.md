# Automatic desktop Fan and Lighting

## Overview
- **Author**: Jacob Flisberg jf223wh
- **Estimated Time**: ~6–12 hours including circuit setup, Home Assistant setup, and debugging

This project is a smart automation system that controls a lamp and a fan based on motion detection (PIR sensor), user-defined auto/manual modes, temperature (DHT11 sensor), and the position of the sun. The microcontroller used is Raspberry Pi Pico W. The device connects to WiFi and communicates over MQTT with Home Assistant, running on a Raspberry Pi 4, to send data and user inputs. To avoid manually adding WiFi and MQTT credentials in the code, a reset button has been incorporated. When pressed, it starts an access point where you can enter the new credentials via a web page, which are then saved to a .txt file.

---

## Objective

To create a self-contained and WiFi-configurable automation device that:

- Turns on lights and based on motion and time of day and a fan based on temperature and motion
- Allows switching between automatic and manual modes
- Sends temperature, humidity, movement and button data to Home Assistant
- Can be easily reconfigured via a button held at startup

---

## Material
Items marked with (*) are found in the [LNU starter kit](https://www.electrokit.com/lnu-starter) for a total cheaper price than buying them separately.
| Component            | Use                                               | Notes                                               | Cost (SEK)|
|----------------------|----------------------------------------------------|----------------------------------------------------|----------|
| Raspberry Pi Pico WH*| Main microcontroller |||
| [Raspberry Pi 4](https://www.electrokit.com/raspberry-pi-4-model-b/4gb) | Host for Home Assistant | SD card, ethernet and USB C cable required |729 |
| [Desktop fan](https://www.clasohlson.com/se/USB-fl%C3%A4kt-%C3%98-14-cm/p/36-7879?utm_source=google&utm_medium=cpc&utm_campaign=p-se-pmax-clas-ohlson-feed&utm_id=21897558452&gad_source=1&gad_campaignid=21901444282&gclid=Cj0KCQjw953DBhCyARIsANhIZoZweBzYua1UH_ivY2qNI5sKeyH0RI0M__Bl6UYj-kND_Kk1e2YJAbMaAqCREALw_wcB) | The controlled fan | Basic USB fan |100|
| [PIR Sensor](https://www.electrokit.com/pir-rorelsedetektor-hc-sr501)| Detects motion | 3.3V GPIO, has settings for time delay and sensitivity |55 |
| DHT11*|Temperature and humidity sensor||49|
| [5V Relay Module](https://www.kjell.com/se/produkter/el-verktyg/elektronik/utvecklingskit/arduino/moduler/luxorparts-relamodul-for-arduino-1x-p87032)|Controls the fan| Cheaper options exist|100|
| Resistors*|For LEDs and pull-up for DHT11 sensor| Four 1kΩ, one 10kΩ|70|
| LEDs*| Indicators for buttons and wifi-reset mode| Two green, one blue (only yellow in starter kit), one red||
| [Tactile Switches](https://www.electrokit.com/knappar-pcb-sortiment-12st?gad_source=1&gad_campaignid=17338847491&gclid=Cj0KCQjw953DBhCyARIsANhIZoafeAWtfX31QQbni1Q4TaL7jI7SYvFG01E0TW891F5BpbIP6BgtArAaAozBEALw_wcB) | Buttons for reset, manual and automatic contorl | Four, one for each LED|99|
| Breadboard*|To connect all the components|||
| Jumper wires*||||
| [Capacitor](https://www.electrokit.com/x2-kondensator-100nf-275vac-10mm)|Stabiliser for the DHT11 input| One 100nF|12|


---

## Computer Setup

- **IDE**: Thonny with MicroPython support
- **Firmware**: Flash latest (1.25.0) MicroPython `.uf2` to Pico W
- **Steps**:
  1. Hold BOOTSEL while plugging in → shows `RPI-RP2`. Make sure the cable supports data transfer.
  2. Flash firmware
  3. Upload: `boot.py`, `config_setup.py`, `main.py`, `IoT.py` from this repository.
  4. When starting up, hold down the red button and initiate the configuration setup.

---

## Circuit Setup


[photo: circuit in kiCAD]

---

## Platform & Architecture

- **Local setup** with Home Assistant and Mosquitto MQTT broker
- **Device sends**:
  - Motion status
  - Auto/manual mode
  - Light/fan on/off status
  - Data of temperature and humidity
- **Device receives**:
  - Commands to switch the light on/off

### MQTT Topics

- `home/rpico/temperature`
- `home/rpico/humidity`
- `home/rpico/pir`
- `home/rpico/buttonAut`
- `home/rpico/buttonLight`

---

## The Code

### Files

- **`boot.py`**  
  On boot: if reset button is pressed, starts `wifi_setup.py`. Otherwise runs `main.py`.

- **`wifi_setup.py`**  
  Starts an access point "CridentialsSetup", password "desk1234", opens a web page on http://192.168.4.1/ where SSID, password, MQTT broker, etc. can be entered. Credentials are saved to `wifi_config.txt`.

- **`main.py`**  
  Connects to wifi using info saved in `wifi_config.txt`  and initiates `wifi_config.txt`. 

- **`IoT.py`**  
  Connects to MQTT, Reads motion sensor, checks if in auto mode, and controls the relay accordingly. Publishes to MQTT topics subscribed to by Home Assistant broker for remote control of the light.

[photo: screenshot of WiFi setup page served by the device]

---

## Connectivity

- **WiFi**: Connects using credentials saved via captive portal
- **MQTT**: Publishes sensor data and receives control signals
- **Protocols**: TCP/IP + MQTT over WiFi

---

## Integration with Home Assistant

- **MQTT integration** enabled in HA
- **Entities created**:
  - `input_boolean.auto_mode`
  - `input_boolean.motion_detected`
  - `switch.light`

### Automations (in HA):

- If `auto_mode` is `on` **and** motion is detected **and** sun is down → turn on light
- If `auto_mode` is `on` **and** no motion **or** sun is up → turn off light
- If 

### Notes:

- All conditions under `AND` must be true; "OR" blocks need careful nesting.
- Debug automations using "Run trace" in the HA automation editor.

[photo: Home Assistant dashboard showing switches and motion status]

---

## Final Result

A fully functional and WiFi-configurable automation controller for fan and light, integrated with Home Assistant and MQTT.

### Features:
- Resettable via button
- Auto/manual toggle
- Live motion tracking
- Extendable (e.g., humidifier/dehumidifier)

[photo: Final mounted setup]

---

## Next Steps

- Power optimization mode
- More robust hardware setup
- 

---

## Demo

[video: light and fan responding to motion + ]

