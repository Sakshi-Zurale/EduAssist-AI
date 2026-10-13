# Computer Networks — Fundamentals

## 1. Introduction

A computer network is a collection of interconnected devices that communicate and share resources.

Examples of networked devices include:

- Computers
- Smartphones
- Servers
- Routers
- Switches
- IoT devices

Networks allow users to share:

- Data
- Applications
- Hardware
- Internet connectivity
- Services

## 2. Types of Networks

### PAN — Personal Area Network

A small network around an individual.

Example:

- Bluetooth devices

### LAN — Local Area Network

A network covering a small geographical area.

Examples:

- Home network
- College laboratory
- Office network

### MAN — Metropolitan Area Network

A network covering a city or large campus.

### WAN — Wide Area Network

A network covering large geographical areas.

The Internet is the largest example of a WAN.

## 3. Network Topologies

Network topology describes how devices are connected.

### Bus Topology

All devices share a common communication medium.

### Star Topology

All devices connect to a central switch or hub.

### Ring Topology

Each device connects to the next device, forming a ring.

### Mesh Topology

Devices have multiple interconnections.

### Tree Topology

Devices are arranged in a hierarchical structure.

## 4. OSI Model

The OSI model divides network communication into seven layers.

```text
7. Application
6. Presentation
5. Session
4. Transport
3. Network
2. Data Link
1. Physical
```

### Layer 1 — Physical

Responsible for transmission of raw bits.

Examples:

- Cables
- Signals
- Connectors

### Layer 2 — Data Link

Responsible for frames and MAC addressing.

Examples:

- Ethernet
- Switches

### Layer 3 — Network

Responsible for logical addressing and routing.

Examples:

- IP
- Routers

### Layer 4 — Transport

Provides end-to-end communication.

Protocols:

- TCP
- UDP

### Layer 5 — Session

Manages communication sessions.

### Layer 6 — Presentation

Handles:

- Data formatting
- Encryption
- Compression

### Layer 7 — Application

Provides network services to applications.

Examples:

- HTTP
- FTP
- SMTP
- DNS

## 5. TCP/IP Model

The TCP/IP model is commonly represented using four layers:

```text
Application
Transport
Internet
Network Access
```

## 6. IP Address

An IP address identifies a device on a network.

### IPv4

IPv4 uses 32-bit addresses.

Example:

```text
192.168.1.10
```

### IPv6

IPv6 uses 128-bit addresses.

It was developed to provide a much larger address space than IPv4.

## 7. MAC Address

A MAC address is a hardware-level network interface identifier.

It operates mainly at the Data Link layer.

## 8. TCP and UDP

### TCP

TCP is connection-oriented and provides reliable data delivery.

Characteristics:

- Connection-oriented
- Reliable
- Ordered delivery
- Error detection
- Flow control

### UDP

UDP is connectionless and provides faster communication with less overhead.

It does not guarantee delivery.

## 9. Common Network Protocols

| Protocol | Purpose |
|---|---|
| HTTP | Web communication |
| HTTPS | Secure web communication |
| FTP | File transfer |
| SMTP | Sending email |
| DNS | Domain name resolution |
| DHCP | Automatic IP configuration |
| SSH | Secure remote access |

## 10. DNS

DNS stands for Domain Name System.

It converts domain names into IP addresses.

Example:

```text
example.com
     ↓
IP Address
```

## 11. Router

A router connects different networks and forwards packets based on IP addresses.

## 12. Switch

A switch connects devices within a local network and forwards frames using MAC addresses.

## 13. Firewall

A firewall monitors and controls network traffic according to security rules.

It can help block unauthorized connections.

## 14. Network Security

Important network security techniques include:

- Firewalls
- Encryption
- VPN
- Authentication
- Intrusion detection
- Access control
- Network segmentation

## 15. Important Questions

1. What is a computer network?
2. Explain LAN, MAN and WAN.
3. Explain different network topologies.
4. Explain the seven layers of OSI.
5. Explain TCP/IP model.
6. What is an IP address?
7. Differentiate IPv4 and IPv6.
8. What is MAC address?
9. Compare TCP and UDP.
10. What is DNS?
11. What is a router?
12. What is a switch?
13. What is a firewall?

## Quick Revision

```text
Computer Networks
├── Network Types
│   ├── PAN
│   ├── LAN
│   ├── MAN
│   └── WAN
├── Topologies
├── OSI Model
├── TCP/IP Model
├── IP Address
├── MAC Address
├── TCP / UDP
├── Network Devices
│   ├── Router
│   ├── Switch
│   └── Firewall
└── Network Security
```