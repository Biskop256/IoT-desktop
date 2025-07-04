from machine import Pin
import time
import dht
import network
import socket

def IoT_main(client):
    # === MQTT Topics ===
    TOPIC_TEMP = b"home/rpico/temperature"
    TOPIC_HUM = b"home/rpico/humidity"
    TOPIC_PIR = b"home/rpico/pir"
    TOPIC_BTN_AUT = b"home/rpico/buttonAut"
    TOPIC_BTN_LIGHT = b"home/rpico/buttonLight"

    client.connect()

    # === Pins ===
    sensor = dht.DHT11(Pin(14))
    pir = Pin(11, Pin.IN)
    relay_fan = Pin(1, Pin.OUT)

    ledAut = Pin(17, Pin.OUT)
    ledLight = Pin(18, Pin.OUT)
    ledFan = Pin(20, Pin.OUT)

    buttonAut = Pin(9, Pin.IN, Pin.PULL_UP)
    buttonLight = Pin(22, Pin.IN, Pin.PULL_UP)
    buttonFan = Pin(27, Pin.IN, Pin.PULL_UP)

    # === Button-States ===
    Aut_state = False  # In automatic mode?
    Light_state = False 
    Fan_state = False
    Fan_auto_state = False # For automatic control
    
    ledLight.value(0)
    ledAut.value(0)
    ledFan.value(0)
    relay_fan.value(0)
    
    # === Main loop ===
    last_temp_time = 0
    while True:
        if not buttonAut.value():
            Aut_state = not Aut_state
            ledAut.value(Aut_state)
            client.publish(TOPIC_BTN_AUT, b"ON" if Aut_state else b"OFF")
            
            # Auto active: turn off manual control
            Fan_state = False
            ledFan.value(Fan_state)
            ledLight.value(Fan_state)
            relay_fan.value(Fan_state)
            time.sleep(0.3)

        if not buttonLight.value():
            Light_state = not Light_state
            ledLight.value(Light_state)
            client.publish(TOPIC_BTN_LIGHT, b"ON" if Light_state else b"OFF")
            Aut_state = False
            Fan_auto_state = False
            ledAut.value(Aut_state)
            relay_fan.value(Fan_auto_state)
            time.sleep(0.3)

        if not buttonFan.value():
            Fan_state = not Fan_state
            Aut_state = False
            ledAut.value(Aut_state)
            ledFan.value(Fan_state)
            relay_fan.value(Fan_state)
            time.sleep(0.3)

        # PIR-sensor och DHT-sensor every 10th second
        if time.time() - last_temp_time > 5:
            motion = pir.value()
            client.publish(TOPIC_PIR, b"1" if motion else b"0")

            try:
                sensor.measure()
                temp = sensor.temperature()
                hum = sensor.humidity()
                client.publish(TOPIC_TEMP, str(temp))
                client.publish(TOPIC_HUM, str(hum))
                print(f"Temp: {temp}°C, Humidity: {hum}%")
                
                # === Fan automation ===
                if Aut_state:
                    if temp > 25 and pir.value():  # at desk + high temp
                        Fan_auto_state = True
                    else:
                        Fan_auto_state = False
                    relay_fan.value(Fan_auto_state)  
            except:
                print("DHT sensor error!")
            last_temp_time = time.time()

        time.sleep(0.05)
