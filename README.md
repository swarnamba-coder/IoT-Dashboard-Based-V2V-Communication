# IoT-Based V2V Communication and Smart Road Accident Alert System

Project Overview

The IoT-Based Vehicle-to-Vehicle (V2V) Communication and Smart Road Accident Alert System is a hardware and software integrated project designed to improve road safety by providing real-time vehicle distance monitoring and accident alerts.

The system uses a Raspberry Pi Pico 2W as the vehicle monitoring node and an ESP32 as the accident detection node. Sensor information is processed by the microcontrollers and communicated through Wi-Fi and the Blynk IoT dashboard.

The system can detect a nearby vehicle/object, warn the driver when the distance becomes critically low, and detect an accident using a vibration sensor. Visual and audio warnings are provided using an LCD, LED, and buzzer.

---

Project Title

IoT Dashboard Based Vehicle-to-Vehicle (V2V) Communication and Accident Alert System

---

Objectives

- To develop an IoT-based prototype for Vehicle-to-Vehicle communication.
- To monitor the distance between vehicles in real time.
- To detect accidents using a vibration sensor.
- To provide immediate accident and proximity warnings.
- To display road status and warnings on an LCD.
- To provide visual and audio alerts using an LED and buzzer.
- To transmit sensor and accident information through Wi-Fi.
- To display real-time information on a Blynk IoT dashboard.
- To demonstrate how IoT can be applied to intelligent transportation and road safety.

---

System Architecture

                    VEHICLE 1
              ACCIDENT DETECTION NODE
                       |
               +-------+-------+
               |               |
        Vibration Sensor     ESP32
                               |
                         Wi-Fi / Internet
                               |
                               v
                        BLYNK CLOUD
                               |
                         IoT Dashboard
                               |
                               v
                       Wi-Fi / Internet
                               |
                    +----------+----------+
                    |                     |
                 Pico 2W              Dashboard
                    |
          +---------+---------+
          |         |         |
       HC-SR04    LCD     LED/Buzzer
          |
     Distance Detection
                    |
                    v
               VEHICLE 2
             SAFETY NODE

---

Hardware Components

1. Raspberry Pi Pico 2W

The Raspberry Pi Pico 2W is used as the main controller for the vehicle monitoring node.

Functions

- Reads the ultrasonic sensor.
- Calculates the distance.
- Controls the LCD.
- Controls the warning LED.
- Controls the buzzer.
- Connects to Wi-Fi.
- Sends sensor information to the Blynk dashboard.

---

2. ESP32

The ESP32 is used as the accident detection node.

Functions

- Reads the vibration sensor.
- Detects sudden vibration/impact.
- Activates the LED and buzzer.
- Can transmit accident information through Wi-Fi and Blynk.

The ESP32 is useful for the accident vehicle because it provides built-in Wi-Fi connectivity and sufficient GPIO pins for sensor and alert components.

---

3. HC-SR04 Ultrasonic Sensor

The HC-SR04 is used to measure the distance between the vehicle and an obstacle/nearby vehicle.

Typical specifications

- Operating voltage: 5 V
- Measuring range: approximately 2 cm – 400 cm
- Trigger signal: 10 µs pulse
- Distance calculated from echo time

The distance is calculated using the speed of sound.

Distance = (Echo Time × Speed of Sound) / 2

The division by 2 is required because the ultrasonic wave travels to the object and returns to the sensor.

---

4. Vibration Sensor

The vibration sensor is used to detect sudden mechanical vibration or impact.

When a significant vibration is detected, the ESP32 interprets it as a possible accident event and activates the warning system.

---

5. 16×2 I2C LCD

The LCD provides local information to the driver.

Example messages:

SYSTEM READY
- ROAD CLEAR
- SLOW DOWN
- CHANGE LANE
- ACCIDENT AHEAD

The I2C interface reduces the number of GPIO connections required between the Pico 2W and LCD.

---

6. Buzzer

The buzzer provides an audible warning.

It is activated when:

- A vehicle/object is too close.
- An accident is detected.

---

7. LED

The LED provides a visual warning.

It turns ON during warning or accident conditions.

---

8. Blynk IoT Dashboard

Blynk is used as the IoT dashboard for displaying real-time information.

The dashboard can display:

- Vehicle distance
- Road status
- Accident status
- Warning messages

---

Pin Configuration

**Raspberry Pi Pico 2W
**
Component            | Pico 2W Pin

- LCD SDA              | GP0
- LCD SCL              | GP1
- HC-SR04 Echo         | GP2
- HC-SR04 Trigger      | GP3
- Buzzer               | GP14
- LED                  | GP15
- Vibration Sensor     | GP16

I2C LCD

- LCD VCC  → VBUS/appropriate supply
- LCD GND  → GND
- LCD SDA  → GP0
- LCD SCL  → GP1

HC-SR04

- TRIG → GP3
- ECHO → GP2
- GND  → GND
- VCC  → 5V

«Important: The HC-SR04 Echo pin can output 5 V. A voltage divider/level shifting should be used before connecting Echo to a Pico GPIO because Pico GPIOs are 3.3 V logic.»

---

ESP32

Example accident-node connections:

Component| ESP32 Pin
- Vibration Sensor DO| GPIO4
- LED| GPIO2
- Buzzer| GPIO5
- Vibration Sensor VCC| 3.3 V
- Vibration Sensor GND| GND

For the LED, a suitable current-limiting resistor should be used.

---

Software Requirements

- MicroPython
- Thonny IDE
- Blynk IoT
- Wi-Fi/Internet connection
- "urequests" library/module
- "pico_i2c_lcd.py" LCD library

---

Working Principle

  The project operates using two main nodes.

Vehicle 1 – Accident Vehicle

  The ESP32 continuously monitors the vibration sensor.

When a sudden vibration/impact is detected:

            Vibration Sensor
                   ↓
                  ESP32
                   ↓
             Accident Detected
                   ↓
              LED + Buzzer
                   ↓
          Blynk / IoT Communication

The accident information can then be made available to the connected monitoring system or nearby vehicle node.

---

Vehicle 2 – Receiving/Safety Vehicle

- The Raspberry Pi Pico 2W continuously measures the distance using the HC-SR04 ultrasonic sensor.
- The sensor sends an ultrasonic pulse and measures the time taken for the echo to return.
- The Pico calculates the distance and sends the value to the Blynk dashboard.

- Normal Condition
    When the distance is greater than the warning limit:

    - LCD:
      ROAD CLEAR

The buzzer and LED remain OFF.

---

- Vehicle Too Close
    When the measured distance is below 10 cm:

    - LCD:
        WARNING!
        SLOW DOWN

The following actions occur:

- Buzzer ON
- LED ON
- Blynk warning updated
- Driver receives an immediate warning

This threshold can be changed according to the requirements of the prototype.

---

- Accident Condition
    When the accident node detects significant vibration:

            ACCIDENT DETECTED
                    ↓
                  ESP32
                    ↓
            Blynk / Communication
                    ↓
             Receiving Vehicle
                    ↓
              ACCIDENT AHEAD

The receiving vehicle can provide an LCD, LED, and buzzer warning to alert the driver.

---

Blynk Dashboard
The Blynk dashboard provides real-time monitoring.

Suggested Virtual Pins

Virtual Pin| Information
- V0| Road/accident status
- V1| Warning/alert message
- V2| Distance

Recommended Widgets

V0
- Value Display / Label

V1
- Value Display / Label

V2
- Gauge
- Value Display
- SuperChart (optional)

For V2, the datastream should use a numerical data type such as Double.

Example dashboard:

    +--------------------------------+
    |       SMART ROAD SAFETY        |
    +--------------------------------+
    |                                |
    | Distance                       |
    |       36.4 cm                  |
    |                                |
    | Status: ROAD SAFE              |
    |                                |
    | Alert: ROAD CLEAR              |
    |                                |
    +--------------------------------+

- During a warning:

    - Distance: 8.5 cm
    - Status: WARNING
    - Alert: SLOW DOWN

- During an accident:

    - Status: ACCIDENT
    - Alert: ACCIDENT AHEAD

---

Communication Flow

              ACCIDENT VEHICLE
                    |
              Vibration Sensor
                    |
                  ESP32
                    |
                  Wi-Fi
                    |
                    v
               BLYNK CLOUD
                    |
                  Wi-Fi
                    |
                    v
              RECEIVING VEHICLE
                    |
                 Pico 2W
                    |
          +---------+---------+
          |         |         |
        LCD       LED       Buzzer

The prototype demonstrates how information from one vehicle can be transferred through an IoT communication layer and used to warn another vehicle.

---

Alert Conditions

Condition| LCD| LED| Buzzer| Blynk
- Distance > 10 cm| ROAD CLEAR| OFF| OFF| ROAD SAFE
- Distance < 10 cm| SLOW DOWN| ON| ON| WARNING
- Accident detected| ACCIDENT AHEAD| ON| ON| ACCIDENT ALERT

---

Example Pico 2W Code

    from machine import Pin, I2C, time_pulse_us
    from pico_i2c_lcd import I2cLcd
    import network
    import urequests
    import time
    
    ssid = "YOUR_WIFI_NAME"
    password = "YOUR_WIFI_PASSWORD"
    
    TOKEN = "YOUR_BLYNK_TOKEN"
    
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    print("Connecting WiFi...")
    wifi.connect(ssid, password)
    
    while not wifi.isconnected():
        print("Connecting...")
        time.sleep(1)
    
    print("WiFi Connected")
    print(wifi.ifconfig())
    
    I2C_ADDR = 0x27
    
    i2c = I2C(
        0,
        sda=Pin(0),
        scl=Pin(1),
        freq=400000
    )
    
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
    
    trig = Pin(3, Pin.OUT)
    echo = Pin(2, Pin.IN)
    
    buzzer = Pin(14, Pin.OUT)
    led = Pin(15, Pin.OUT)
    
    lcd.clear()
    lcd.putstr("SYSTEM READY")
    time.sleep(2)
    
    
    def send_blynk(pin, value):

        try:
    
            url = "https://blynk.cloud/external/api/update?token={}&{}={}".format(
                TOKEN,
                pin,
                value
            )
    
            response = urequests.get(url)
    
            print("BLYNK SENT:", value)
    
            response.close()
    
        except Exception as e:
    
            print("BLYNK ERROR:", e)


    while True:
    
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
    
        if distance > 0:
    
            send_blynk("V2", distance)
    
        if distance > 0 and distance < 10:
    
            print("WARNING - SLOW DOWN")
    
            buzzer.value(1)
            led.value(1)
    
            lcd.clear()
            lcd.putstr("WARNING!\nSLOW DOWN")
    
            send_blynk("V0", "WARNING")
            send_blynk("V1", "SLOW DOWN")
    
        else:
    
            buzzer.value(0)
            led.value(0)
    
            lcd.clear()
            lcd.putstr("ROAD CLEAR")
    
            send_blynk("V0", "ROAD SAFE")
            send_blynk("V1", "ROAD CLEAR")
    
        time.sleep(1)

«Do not upload real Wi-Fi passwords or Blynk authentication tokens to a public GitHub repository. Replace them with placeholders before committing the code.»

---

ESP32 Accident Detection Code

The ESP32 acts as the accident detection node.
    
    from machine import Pin
    import time
    
    vibration = Pin(4, Pin.IN)
    led = Pin(2, Pin.OUT)
    buzzer = Pin(5, Pin.OUT)
    
    print("ESP32 Accident Detection System Ready")
    
    while True:
    
        if vibration.value() == 1:
    
            print("ACCIDENT DETECTED")
    
            led.value(1)
            buzzer.value(1)
    
            time.sleep(2)
    
        else:
    
            led.value(0)
            buzzer.value(0)
    
        time.sleep(0.1)

---

Advantages

- Real-time distance monitoring.
- Accident detection.
- Immediate driver warning.
- Audio and visual alerts.
- IoT-based remote monitoring.
- Low-cost prototype.
- Easy to expand.
- Suitable for smart transportation concepts.
- Can be extended to multiple vehicles.

---

Limitations

The current system is a prototype and has some limitations:

- The HC-SR04 has a limited sensing range.
- Ultrasonic measurements can be affected by environmental conditions and object surfaces.
- A vibration sensor alone cannot reliably determine the severity or exact nature of a real accident.
- Cloud-based communication requires an Internet connection.
- The prototype does not provide exact GPS accident coordinates.
- The current implementation does not represent a production-grade automotive V2V communication protocol.

---

## Why V2V Communication is Important

  Drivers cannot always see hazards that are present ahead of them. An accident around a bend, behind another vehicle, or in heavy traffic may not be visible immediately.

  V2V communication can allow vehicles to exchange safety information such as:

  - Accident alerts
  - Sudden braking
  - Vehicle position
  - Traffic hazards
  - Road conditions
  - Collision warnings

This can provide drivers with additional reaction time and potentially improve road safety.

---

## Future Scope

The project can be extended in several ways:

1. GPS Integration

GPS can be added to provide the exact location of an accident.

2. Emergency Notifications

Accident alerts can be sent through SMS, email, or other emergency notification systems.

3. Direct V2V Communication

Instead of relying only on cloud communication, technologies such as ESP-NOW, Bluetooth, or dedicated automotive V2X technologies can be investigated for direct vehicle-to-vehicle communication.

4. Multiple Vehicles

Multiple ESP32/Pico-based vehicle nodes can be connected to the same communication system.

5. Hospital and Police Alerts

Accident information could be forwarded to emergency response systems.

6. Data Analytics

Historical accident and distance data can be stored and analyzed to identify dangerous road conditions.

7. Smart City Integration

The system could eventually communicate with intelligent traffic lights, road infrastructure, emergency services, and traffic management systems.

---

## Applications

- Vehicle safety systems
- Smart transportation
- Accident warning systems
- Intelligent traffic management
- Connected vehicle prototypes
- IoT-based road monitoring
- Smart city transportation systems
- Educational V2V/V2X demonstrations

---

## Project Results

The prototype successfully demonstrates:

- Wi-Fi connectivity using Raspberry Pi Pico 2W.
- Real-time ultrasonic distance measurement.
- LCD-based road status display.
- Warning generation when distance is below the defined threshold.
- LED and buzzer activation during warning conditions.
- Vibration-based accident detection using ESP32.
- IoT dashboard-based monitoring using Blynk.

The system demonstrates the basic concept of sharing safety information between connected vehicle nodes.

---
## Project Team

Department of Electronics and Communication Engineering

Sapthagiri NPS University, Bengaluru

Team Members

- Swarnamba P – Hardware/ Programming
- Rakshitha A N – Hardware / Testing
- SHOBHA B A – Documentation / Testing

Semester

IV Semester

Academic Year

2025–26

Project Guide

Prof. Kantharaju. T
Assistant Professor
Department of Electronics and Communication Engineering

---
## Acknowledgement

We would like to acknowledge **[Mahesh Gowda N]** for suggesting the initial concept of using vehicle-to-vehicle communication for improving road safety. This suggestion helped inspire the direction of our project. The final concept, hardware implementation, programming, IoT dashboard integration, testing, and documentation were carried out by our project team.
Repository Structure

---

    IoT-V2V-Communication/
    │
    ├── README.md
    │
    ├── Pico2W/
    │   ├── main.py
    │   └── pico_i2c_lcd.py
    │
    ├── ESP32/
    │   └── accident_detection.py
    │
    ├── Hardware/
    │   ├── circuit_diagram.png
    │   ├── block_diagram.png
    │   └── project_photo.jpg
    │
    └── Documentation/
        └── project_report.pdf

---

Conclusion

  The IoT-Based V2V Communication and Smart Road Accident Alert System demonstrates how microcontrollers, sensors, wireless communication, and cloud dashboards can be integrated to improve road safety.

  The Raspberry Pi Pico 2W provides real-time distance monitoring and driver warnings, while the ESP32 provides an independent accident detection node. The Blynk IoT dashboard provides a convenient platform for monitoring vehicle and accident information.

  Although the current project is a prototype, its architecture provides a foundation for future development involving GPS, direct V2V communication, emergency services, multiple vehicles, and intelligent transportation infrastructure.

---

Keywords

  IoT, V2V Communication, Vehicle-to-Vehicle Communication, Raspberry Pi Pico 2W, ESP32, HC-SR04, Ultrasonic Sensor, Vibration Sensor, Blynk, Accident Detection, Road Safety, Smart Transportation, IoT Dashboard
