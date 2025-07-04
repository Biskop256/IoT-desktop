import network
import socket
import time
import os
from machine import Pin
from umqtt.simple import MQTTClient

def save_config(ssid, password, mqtt_broker, mqtt_user, mqtt_password, client_id):
    with open("config.txt", "w") as f:
        f.write(f"{ssid}\n{password}\n{mqtt_broker}\n{mqtt_user}\n{mqtt_password}\n{client_id}\n")
        
def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(20):
        if wlan.isconnected():
            return True
        time.sleep(0.5)
    return False

def mqtt_connect(mqtt_broker, mqtt_user, mqtt_password, client_id, timeout=20):
    import gc
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < (timeout * 1000):
        try:
            client = MQTTClient(client_id, mqtt_broker, user=mqtt_user, password=mqtt_password, keepalive=30)
            client.connect()
            return True, client
        except Exception as e:
            print("Fel:",e)
            time.sleep(2)
            gc.collect()
            
    return False, None

def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid="CredentialsSetup", password="desk1234")
    ap.active(True)
    while not ap.active():
        pass
    return ap

def get_cred():
    time.sleep(1)
    led = Pin(16, Pin.OUT)
    led.on()  # Show that we're in setup mode

    ap = start_ap()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    error_msg = ""
    print("AP running, open 192.168.4.1 in browser")

    
    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024).decode()
        
        html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: sans-serif; padding: 20px; background-color: #f5f5f5; }}
                    input {{ margin: 5px 0; width: 100%; padding: 5px; }}
                    form {{ max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 10px; }}
                    h1 {{ text-align: center; }}
                    .error {{ color: red; }}
                </style>
            </head>
            <body>
                <h1>Configuration-settings</h1>
                <form method="POST">
                    SSID: <input name="ssid" required/><br>
                    Password: <input name="password" type="password" /><br>
                    MQTT-broker: <input name="mqtt_broker" required/><br>
                    MQTT-user: <input name="mqtt_user" /><br>
                    MQTT-password: <input name="mqtt_password" type="password"/><br>
                    Client ID: <input name="client_id" required/><br>
                    <input type="submit" value="Connect" />
                </form>
            </body>
            </html>
        """
        
        # Check if credentials posted
        if "POST" in request:
            try:
                print("Request received, disconnecting from AP")
                time.sleep(5)
                body = request.split("\r\n\r\n")[1]
                params = {kv.split("=")[0]: kv.split("=")[1] for kv in body.split("&")}
                ssid = params["ssid"]
                password = params["password"]
                mqtt_broker = params["mqtt_broker"]
                mqtt_user = params["mqtt_user"]
                mqtt_password = params["mqtt_password"]
                client_id = params["client_id"]
                
                ssid = ssid.replace('+', ' ')
                password = password.replace('+', ' ')
                
                ap.active(False)
                
                wifi_ok = wifi_connect(ssid, password)
                print("Wifi, handled, waiting to settle, trying MQTT\n", wifi_ok) # Debugging
                time.sleep(10)
                mqtt_ok, client = mqtt_connect(mqtt_broker, mqtt_user, mqtt_password, client_id)
                
                if wifi_ok and mqtt_ok:
                    print("Wifi and MQTT connections successful")
                    save_config(ssid, password, mqtt_broker, mqtt_user, mqtt_password, client_id)
                    led.off()
                    time.sleep(2)
                    
                    # Visual confirmation
                    for i in range(3):
                        led.on()
                        time.sleep(0.2)
                        led.off()
                        time.sleep(0.2)
                    import IoT
                    ap.active(False)
                    IoT.IoT_main(client)

                else:
                    print("Wifi or MQTT connection failed. Try again.")
                    led.off()
                    time.sleep(0.5)
                    led.on()
                    time.sleep(1)
                    led.off()
                    
            except Exception as e:
                print(f"Error: {e}")
                
        else:
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            cl.sendall(html)
            cl.close()
