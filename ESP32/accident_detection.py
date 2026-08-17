from machine import Pin
import network
import urequests
import time


# =====================================================
# ESP32 - V2V ACCIDENT DETECTION
# =====================================================

# =====================================================
# WIFI DETAILS
# =====================================================

SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"


# =====================================================
# BLYNK AUTH TOKEN
# =====================================================

BLYNK_TOKEN = "YOUR_BLYNK_AUTH_TOKEN"


# =====================================================
# PIN CONFIGURATION
# =====================================================

# Vibration / impact sensor
VIBRATION_PIN = 27

# Buzzer
BUZZER_PIN = 26

# LED
LED_PIN = 25


# =====================================================
# GPIO SETUP
# =====================================================

vibration = Pin(VIBRATION_PIN, Pin.IN)

buzzer = Pin(BUZZER_PIN, Pin.OUT)
led = Pin(LED_PIN, Pin.OUT)

buzzer.value(0)
led.value(0)


# =====================================================
# CONNECT TO WIFI
# =====================================================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Connecting to WiFi...")

wifi.connect(SSID, PASSWORD)

timeout = 20

while not wifi.isconnected() and timeout > 0:
    print("Connecting...")
    time.sleep(1)
    timeout -= 1

if wifi.isconnected():

    print("WiFi Connected")
    print("IP Address:", wifi.ifconfig()[0])

else:

    print("WiFi connection failed")


# =====================================================
# SEND DATA TO BLYNK
# =====================================================

def send_blynk(pin, value):

    if not wifi.isconnected():

        print("WiFi not connected")
        return

    try:

        url = (
            "https://blynk.cloud/external/api/update"
            "?token={}&{}={}"
        ).format(
            BLYNK_TOKEN,
            pin,
            value
        )

        response = urequests.get(url)

        print("BLYNK:", pin, "=", value)
        print("HTTP:", response.status_code)

        response.close()

    except Exception as e:

        print("BLYNK ERROR:", e)


# =====================================================
# ACCIDENT ALERT
# =====================================================

def accident_alert():

    print("================================")
    print("ACCIDENT DETECTED")
    print("================================")

    # Turn ON buzzer and LED
    buzzer.value(1)
    led.value(1)

    # Send accident status to Blynk
    send_blynk("V0", "ACCIDENT DETECTED")

    # Send emergency alert status
    send_blynk("V1", "EMERGENCY ALERT")

    # Keep warning active
    time.sleep(3)

    # Turn OFF buzzer and LED
    buzzer.value(0)
    led.value(0)


# =====================================================
# START MESSAGE
# =====================================================

print("--------------------------------")
print("ESP32 V2V ACCIDENT SYSTEM")
print("--------------------------------")

send_blynk("V0", "SYSTEM READY")
send_blynk("V1", "ROAD SAFE")


# =====================================================
# MAIN LOOP
# =====================================================

while True:

    try:

        sensor_value = vibration.value()

        print("Vibration:", sensor_value)

        # -------------------------------------------------
        # ACCIDENT DETECTED
        # -------------------------------------------------

        if sensor_value == 1:

            accident_alert()

            # Small delay prevents repeated alerts
            time.sleep(2)


        # -------------------------------------------------
        # NORMAL CONDITION
        # -------------------------------------------------

        else:

            buzzer.value(0)
            led.value(0)

        time.sleep(0.2)


    except Exception as e:

        print("SYSTEM ERROR:", e)

        buzzer.value(0)
        led.value(0)

        time.sleep(1)
