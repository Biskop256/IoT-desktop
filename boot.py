from machine import Pin
import time
import config_setup

reset_button = Pin(7, Pin.IN, Pin.PULL_UP)
reset_led = Pin(16, Pin.OUT)  # Reset LED
reset_led.off()

# Check reset button at boot
if not reset_button.value():
    reset_led.value(1)
    time.sleep(2)
    reset_led.value(0)
    config_setup.get_cred() # Go into setup mode
    
else:
    import main  # Normal start
    main.main()
