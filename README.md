# ELEC0138 Security and Privacy Coursework – Group 7

## Overview

This repository contains the implementation and experimental results for ELEC0138 coursework, covering both **Threat Modelling & Attack Simulation (CW1)** and **Security & Privacy Defense Strategy (CW2)**.

The project focuses on a **BLE-based medical IoT device**, demonstrating real-world vulnerabilities and corresponding defense mechanisms.

---

## Repository Structure

```
attack/
    ble_attack_commands.md     # BLE attack procedures and explanations (CW1)

defense/
    secure_ble_demo.py         # Secure BLE prototype implementation (CW2)

README.md
```

---

## Coursework 1: Threat Modelling & Attack Simulation

The attack analysis identifies several critical BLE security weaknesses:

- Unauthorized device discovery and connection
- Passive packet sniffing (eavesdropping)
- Unrestricted interaction with GATT services
- Ability to switch between passive and active attack modes

Detailed attack procedures and command-level demonstrations are provided in:

👉 `attack/ble_attack_commands.md`

---

## Coursework 2: Security & Privacy Defense Strategy

A secure BLE prototype is implemented to mitigate the identified threats.

### Key Security Features

- **Authentication control**  
  Only authorized devices are allowed to establish connections

- **Role-based access control (RBAC)**  
  Different permissions for patient, doctor, and attacker roles

- **Data encryption (Fernet symmetric encryption)**  
  Protects sensitive medical data during transmission

- **Secure GATT interaction logic**  
  Prevents unauthorized read/write operations

---

## Demo Scenarios

The system simulates multiple realistic interaction scenarios:

1. Legitimate patient accessing medical data  
2. Doctor performing authorized write operations  
3. Unauthorized attacker attempting connection  
4. Unauthorized GATT write attempts  
5. Intercepted encrypted communication  

---

## How to Run the Demo

### Requirements

```bash
pip install cryptography
```

### Run

```bash
python defense/secure_ble_demo.py
```

---

## Key Insights

This project demonstrates that:

- BLE devices without proper security are highly vulnerable  
- Passive attacks can occur without any device interaction  
- Security must be enforced at multiple layers (connection, data, access control)  
- Even a lightweight prototype can significantly improve system resilience  

---

## Author

Group 7  
ELEC0138 – Security and Privacy  
University College London
