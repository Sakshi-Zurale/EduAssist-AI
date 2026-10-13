# Internet of Things — Fundamentals

## 1. Introduction

The Internet of Things (IoT) is a system of physical devices connected to networks that can collect, exchange, and sometimes process data.

IoT devices can include:

- Sensors
- Microcontrollers
- Smart appliances
- Vehicles
- Industrial equipment
- Agricultural devices
- Wearable devices

## 2. Basic IoT Architecture

A basic IoT system can be represented as:

```text
Sensors
   ↓
Microcontroller / Device
   ↓
Communication Network
   ↓
Cloud / Edge Processing
   ↓
Application
   ↓
User
```

## 3. Main Components

### Sensors

Sensors collect information from the physical environment.

Examples:

- Temperature sensor
- Humidity sensor
- Soil moisture sensor
- Light sensor
- Gas sensor
- Pressure sensor

### Actuators

Actuators perform physical actions based on control signals.

Examples:

- Relay
- Motor
- Servo motor
- Pump

### Microcontroller

A microcontroller processes sensor data and controls connected components.

Examples:

- Arduino
- ESP32
- ESP8266

## 4. ESP32

ESP32 is a microcontroller platform commonly used in IoT projects.

Important features include:

- Wi-Fi
- Bluetooth
- GPIO
- ADC
- Low-power modes
- Microcontroller processing

## 5. Communication Protocols

IoT devices can communicate using various protocols.

Examples:

- Wi-Fi
- Bluetooth
- Zigbee
- LoRaWAN
- MQTT
- HTTP

## 6. MQTT

MQTT is a lightweight messaging protocol commonly used in IoT.

It uses a publish-subscribe architecture.

```text
Publisher
    ↓
 MQTT Broker
    ↓
Subscriber
```

Example:

A temperature sensor publishes data to a topic, and a monitoring application subscribes to that topic.

## 7. IoT Data Flow

Typical IoT data flow:

```text
Physical Environment
        ↓
      Sensor
        ↓
   Microcontroller
        ↓
 Communication
        ↓
 Cloud / Edge
        ↓
 Data Processing
        ↓
 Dashboard
```

## 8. Edge Computing

Edge computing processes data close to where it is generated.

Benefits:

- Lower latency
- Reduced bandwidth usage
- Faster response
- Local processing

## 9. Cloud Computing in IoT

Cloud platforms can provide:

- Data storage
- Data processing
- Device management
- Analytics
- Visualization
- Machine learning

## 10. IoT Security

IoT devices can introduce security risks because they are connected to networks and may have limited computing resources.

Security practices include:

- Strong authentication
- Secure communication
- Device identity
- Encryption
- Firmware updates
- Network segmentation
- Secure credential management

## 11. IoT in Agriculture

IoT can support smart agriculture through:

- Soil moisture monitoring
- Temperature monitoring
- Humidity monitoring
- Irrigation automation
- Crop monitoring
- Weather data collection
- Storage monitoring

Example:

```text
Soil Sensors
     ↓
ESP32
     ↓
Internet
     ↓
Cloud
     ↓
Agriculture Dashboard
```

## 12. IoT in Smart Homes

Examples include:

- Smart lights
- Smart thermostats
- Security cameras
- Smart locks
- Energy monitoring

## 13. IoT in Industry

Industrial IoT can be used for:

- Predictive maintenance
- Machine monitoring
- Production monitoring
- Asset tracking
- Energy management

## 14. Advantages

- Real-time monitoring
- Automation
- Remote control
- Data-driven decisions
- Improved efficiency
- Predictive maintenance

## 15. Limitations

- Security risks
- Privacy concerns
- Connectivity dependency
- Device management complexity
- Power limitations
- Interoperability issues

## 16. Important Questions

1. What is IoT?
2. Explain IoT architecture.
3. What is a sensor?
4. What is an actuator?
5. What is ESP32?
6. Explain MQTT.
7. What is publish-subscribe architecture?
8. What is edge computing?
9. Explain IoT security.
10. Explain IoT applications in agriculture.
11. What is Industrial IoT?
12. What are the advantages and limitations of IoT?

## Quick Revision

```text
IoT
├── Sensors
├── Actuators
├── Microcontrollers
├── Connectivity
├── MQTT / HTTP
├── Edge Computing
├── Cloud
├── Data Processing
├── Security
└── Applications
    ├── Agriculture
    ├── Smart Home
    ├── Healthcare
    └── Industry
```
