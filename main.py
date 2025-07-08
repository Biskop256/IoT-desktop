import time
import network
import IoT
import config_setup
from machine import Pin

led = Pin(16, Pin.OUT)

def main():
    def get_config():
        try:
            with open("config.txt", "r") as f:
                ssid = f.readline().strip()
                password = f.readline().strip()
                mqtt_broker = f.readline().strip()
                mqtt_user = f.readline().strip()
                mqtt_password = f.readline().strip()
                client_id = f.readline().strip()
                return ssid, password, mqtt_broker, mqtt_user, mqtt_password, client_id
        except:
            print("config.txt does not exist")
            for i in range(2):
                led.on()
                time.sleep(1)
                led.off()
                time.sleep(0.2)
            return
    
    ssid, password, mqtt_broker, mqtt_user, mqtt_password, client_id = get_config()
    wifi_ok = config_setup.wifi_connect(ssid, password)
    mqtt_ok, client = config_setup.mqtt_connect(mqtt_broker, mqtt_user, mqtt_password, client_id)

    if wifi_ok and mqtt_ok:
        print("Connection successful, starting up...")
        for i in range(3):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
        IoT.IoT_main(client)
    else:
        print("Connection failed, reset your credentials.")
        led.on()
        time.sleep(1)
        led.off()
