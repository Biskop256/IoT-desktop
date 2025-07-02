# Automatic Fan and Light Control with Raspberry Pi Pico W

## Overview

This project is a smart automation system using a Raspberry Pi Pico W. It controls a lamp and a fan based on motion detection (PIR sensor), user-defined auto/manual modes, temperature (DHT11 sensor) and the position of the sun. The device connects to WiFi using a simple captive portal for setup and communicates over MQTT with Home Assistant set up on a Raspberry pi 4.

- **Title**: Smart Fan & Light Controller with PIR, DHT11, MQTT, and Home Assistant
- **Short Overview**: Motion and temperature based light and fan control using a microcontroller with web-based WiFi provisioning and MQTT automation.
- **Estimated Time**: ~6–12 hours including circuit setup, Home Assistant setup, and debugging

---

## Objective

To create a self-contained and WiFi-configurable automation device that:

- Turns on lights and based on motion and time of day and a fan based on temperature and motion
- Allows switching between automatic and manual modes
- Sends temperature, humidity, movement and button data to Home Assistant
- Can be easily reconfigured via a button held at startup

---

## Material

| Component            | Use                                               | Notes                                               | Cost (SEK)|
|----------------------|----------------------------------------------------|----------------------------------------------------|----------|
| Raspberry Pi Pico WH | Main microcontroller                               | WiFi-enabled                                       |99        |
| Raspberry Pi 4 ||||
| Desktop fan ||||
| PIR Sensor (HC-SR501)| Detects motion                                     | 3.3V GPIO                                          |55        |
| DHT11 ||||
| 5V Relay Module      | Controls the fan                                   | Cheaper options exist                              |99        |
| Resistors            | For LEDs and pull-up for DHT11 sensor              | Four 1kΩ, one 10kΩ                                 |          |
| LEDs                 | Indicators for buttons and wifi-reset mode         |                                                    |          |
| Switches             | Tactile switches as buttons                        |                                                    |          |
| Breadboard||||
| Jumper wires||||
| Capacitor ||||


---

## Computer Setup

- **IDE**: Thonny with MicroPython support
- **Firmware**: Flash latest (1.25.0) MicroPython `.uf2` to Pico W
- **Steps**:
  1. Hold BOOTSEL while plugging in → shows `RPI-RP2`. Make sure the cable supports data transfer.
  2. Flash firmware
  3. Upload: `boot.py`, `wifi_setup.py`, `main.py`, `iot.py` from this repository.
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

