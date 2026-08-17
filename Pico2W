from machine import Pin, I2C, time_pulse_us
from pico_i2c_lcd import I2cLcd
import network
import urequests
import time

# =====================================================
# WIFI DETAILS
# =====================================================

ssid = "YOUR_WIFI_NAME"
password = "YOUR_WIFI_PASSWORD"

# =====================================================
# BLYNK TOKEN
# =====================================================

TOKEN = "YOUR_BLYNK_TOKEN"

# =====================================================
# CONNECT TO WIFI
# =====================================================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Connecting WiFi...")
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Connecting...")
    time.sleep(1)

print("WiFi Connected")
print(wifi.ifconfig())

# =====================================================
# LCD SETUP
# =====================================================

I2C_ADDR = 0x27

i2c = I2C(
    0,
    sda=Pin(0),
    scl=Pin(1),
    freq=400000
)

lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# =====================================================
# ULTRASONIC SENSOR
# =====================================================

trig = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# =====================================================
# WARNING COMPONENTS
# =====================================================

buzzer = Pin(14, Pin.OUT)
led = Pin(15, Pin.OUT)

# =====================================================
# START MESSAGE
# =====================================================

lcd.clear()
lcd.putstr("SYSTEM READY")

time.sleep(2)

# =====================================================
# SEND DATA TO BLYNK
# =====================================================

def send_blynk(pin, value):

    try:

        url = "https://blynk.cloud/external/api/update?token={}&{}={}".format(
            TOKEN,
            pin,
            value
        )

        response = urequests.get(url)

        response.close()

        print("BLYNK SENT:", value)

    except Exception as e:

        print("BLYNK ERROR:", e)

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    # =================================================
    # DISTANCE MEASUREMENT
    # =================================================

    trig.low()
    time.sleep_us(2)

    trig.high()
    time.sleep_us(10)

    trig.low()

    try:

        duration = time_pulse_us(echo, 1, 30000)

        if duration > 0:

            distance = (duration * 0.0343) / 2

        else:

            distance = -1

    except:

        distance = -1

    print("Distance:", distance)

    # =================================================
    # SEND REAL-TIME DISTANCE TO BLYNK
    # =================================================

    if distance > 0:

        send_blynk("V2", "{:.1f}".format(distance))

    # =================================================
    # VEHICLE TOO CLOSE
    # =================================================

    if distance > 0 and distance < 10:

        print("WARNING - SLOW DOWN")

        buzzer.value(1)
        led.value(1)

        lcd.clear()
        lcd.putstr("WARNING!\nSLOW DOWN")

        send_blynk("V0", "WARNING")
        send_blynk("V1", "SLOW DOWN")

    # =================================================
    # ROAD CLEAR
    # =================================================

    else:

        buzzer.value(0)
        led.value(0)

        lcd.clear()
        lcd.putstr("ROAD CLEAR")

        send_blynk("V0", "ROAD SAFE")
        send_blynk("V1", "ROAD CLEAR")

    time.sleep(1)
