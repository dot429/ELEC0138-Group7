# BLE Attack Demonstration (Group 7)

This document presents the BLE attack procedures conducted in Coursework 1. The experiments demonstrate key security weaknesses in the target device, including lack of authentication, exposure to passive sniffing, and unrestricted interaction with device services.

---

## Scenario 1: Device Discovery and Unauthorized Connection

```bash
sudo -s
cd ~/whad-workshop
source venv/bin/activate

# Step 1: Clean up previous processes
pkill -9 -f wsniff
pkill -9 -f wble 2>/dev/null

# Step 2: Initialize the device
wup uart0

# Step 3: Start BLE central mode
wble-central -i uart0

# Scan for nearby devices
scan

# Press Ctrl+C to stop scanning
connect ea:f9:a9:0d:39:be
```

**Explanation:**  
This scenario shows that the BLE device can be discovered and connected without any authentication. An attacker within communication range can directly establish a connection, indicating a lack of access control at the connection level.

---

## Scenario 2: Passive Packet Sniffing

```bash
pkill -9 -f wsniff
wup uart0

# Start sniffing BLE traffic
wsniff -i uart0 --format repr ble -a
```

**Explanation:**  
This demonstrates that BLE communication can be passively intercepted. The attacker does not need to establish a connection and can still observe transmitted data, exposing sensitive information.

---

## Scenario 3: Switching Between Passive and Active Modes

```bash
# Stop sniffing (Ctrl + C)
Ctrl + C

# Force cleanup
pkill -9 -f wsniff

# Reinitialize the device
wup uart0

# Restart BLE central mode
wble-central -i uart0

scan
```

**Explanation:**  
This scenario shows that an attacker can easily switch between passive sniffing and active interaction. This flexibility increases the attack surface and allows attackers to combine multiple attack strategies.

---

## Summary of Observed Vulnerabilities

The experiments reveal several critical security issues:

- Lack of authentication during connection establishment  
- Exposure to passive eavesdropping  
- Ability to interact with device services without restriction  
- Increased attack capability due to flexible attack modes  

These vulnerabilities motivate the secure system design proposed in Coursework 2.
