from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime


class SecureBLEMedicalIoTSystem:
    def __init__(self):
        # Registered devices and roles
        self.authorized_devices = {
            "patient_phone": "patient",
            "doctor_tablet": "doctor",
            "nurse_station": "nurse"
        }

        # Role permissions
        self.permissions = {
            "patient": ["read_own_data"],
            "nurse": ["read_own_data", "read_device_status"],
            "doctor": ["read_own_data", "read_device_status", "write_characteristic", "update_threshold"]
        }

        # Encryption setup
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

        # Monitoring and lockout
        self.failed_attempts = {}
        self.blocklist = set()
        self.max_failed_attempts = 3

        # Audit log
        self.audit_logs = []

        # Simulated medical data
        self.medical_data = {
            "patient_id": "P001",
            "ecg": "72 bpm",
            "spo2": "98%",
            "device_status": "normal"
        }

    # -----------------------------
    # Logging
    # -----------------------------
    def log_event(self, event_type, actor, result, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "timestamp": timestamp,
            "event_type": event_type,
            "actor": actor,
            "result": result,
            "details": details
        }
        self.audit_logs.append(record)

    # -----------------------------
    # Authentication
    # -----------------------------
    def authenticate_device(self, device_name):
        if device_name in self.blocklist:
            self.log_event(
                "AUTHENTICATION",
                device_name,
                "DENIED",
                "Device is temporarily blocklisted due to repeated failed attempts"
            )
            return False, None, "BLOCKED"

        if device_name in self.authorized_devices:
            role = self.authorized_devices[device_name]
            self.log_event(
                "AUTHENTICATION",
                device_name,
                "ALLOWED",
                f"Role assigned: {role}"
            )
            return True, role, "ALLOWED"

        # Failed authentication
        self.failed_attempts[device_name] = self.failed_attempts.get(device_name, 0) + 1

        if self.failed_attempts[device_name] >= self.max_failed_attempts:
            self.blocklist.add(device_name)
            self.log_event(
                "AUTHENTICATION",
                device_name,
                "DENIED",
                "Too many failed attempts; added to temporary blocklist"
            )
            return False, None, "BLOCKED"

        self.log_event(
            "AUTHENTICATION",
            device_name,
            "DENIED",
            f"Unauthorized device; failed attempts = {self.failed_attempts[device_name]}"
        )
        return False, None, "DENIED"

    # -----------------------------
    # Authorization
    # -----------------------------
    def check_access(self, role, action):
        if role in self.permissions and action in self.permissions[role]:
            self.log_event(
                "AUTHORIZATION",
                role,
                "ALLOWED",
                f"Action permitted: {action}"
            )
            return True

        self.log_event(
            "AUTHORIZATION",
            role,
            "DENIED",
            f"Action denied: {action}"
        )
        return False

    # -----------------------------
    # Encryption and integrity
    # -----------------------------
    def encrypt_payload(self, plaintext):
        encrypted = self.cipher.encrypt(plaintext.encode())
        self.log_event(
            "ENCRYPTION",
            "SYSTEM",
            "SUCCESS",
            "Medical payload encrypted successfully"
        )
        return encrypted

    def decrypt_payload(self, encrypted_payload):
        try:
            decrypted = self.cipher.decrypt(encrypted_payload).decode()
            self.log_event(
                "DECRYPTION",
                "SYSTEM",
                "SUCCESS",
                "Payload decrypted and integrity verified"
            )
            return True, decrypted
        except InvalidToken:
            self.log_event(
                "DECRYPTION",
                "SYSTEM",
                "FAILED",
                "Payload integrity verification failed; packet rejected"
            )
            return False, None

    # -----------------------------
    # Simulated operations
    # -----------------------------
    def read_medical_data(self):
        payload = f"ECG: {self.medical_data['ecg']}, SpO2: {self.medical_data['spo2']}"
        return self.encrypt_payload(payload)

    def write_characteristic(self, value):
        self.medical_data["device_status"] = value
        self.log_event(
            "WRITE_OPERATION",
            "SYSTEM",
            "SUCCESS",
            f"Device status updated to: {value}"
        )
        return "Characteristic updated successfully"

    # -----------------------------
    # Display helpers
    # -----------------------------
    def print_divider(self):
        print("-" * 70)

    def show_logs(self):
        self.print_divider()
        print("AUDIT LOG SUMMARY")
        self.print_divider()
        for log in self.audit_logs:
            print(
                f"[{log['timestamp']}] "
                f"{log['event_type']} | Actor: {log['actor']} | "
                f"Result: {log['result']} | Details: {log['details']}"
            )

    # -----------------------------
    # Demo scenarios
    # -----------------------------
    def run_demo(self):
        print("=== Advanced Secure BLE Medical IoT Prototype ===\n")

        # Scenario 1
        self.print_divider()
        print("[Scenario 1] Legitimate patient device: authenticated read access")
        self.print_divider()
        device = "patient_phone"
        ok, role, status = self.authenticate_device(device)
        print("Device:", device)
        print("Authentication:", status)

        if ok:
            print("Role:", role)
            action = "read_own_data"
            allowed = self.check_access(role, action)
            print("Requested action:", action)
            print("Access control:", "ALLOWED" if allowed else "DENIED")

            if allowed:
                encrypted_payload = self.read_medical_data()
                success, decrypted_payload = self.decrypt_payload(encrypted_payload)
                print("Encrypted payload:", encrypted_payload.decode())
                print("Authorized read result:", decrypted_payload if success else "FAILED")

        print()

        # Scenario 2
        self.print_divider()
        print("[Scenario 2] Legitimate doctor device: authenticated write access")
        self.print_divider()
        device = "doctor_tablet"
        ok, role, status = self.authenticate_device(device)
        print("Device:", device)
        print("Authentication:", status)

        if ok:
            print("Role:", role)
            action = "write_characteristic"
            allowed = self.check_access(role, action)
            print("Requested action:", action)
            print("Access control:", "ALLOWED" if allowed else "DENIED")

            if allowed:
                result = self.write_characteristic("alert_threshold_updated")
                print("Write operation result:", result)

        print()

        # Scenario 3
        self.print_divider()
        print("[Scenario 3] Legitimate nurse device: restricted write attempt")
        self.print_divider()
        device = "nurse_station"
        ok, role, status = self.authenticate_device(device)
        print("Device:", device)
        print("Authentication:", status)

        if ok:
            print("Role:", role)
            action = "write_characteristic"
            allowed = self.check_access(role, action)
            print("Requested action:", action)
            print("Access control:", "ALLOWED" if allowed else "DENIED")
            if not allowed:
                print("System response: write blocked due to insufficient privilege")

        print()

        # Scenario 4
        self.print_divider()
        print("[Scenario 4] Unauthorized attacker device: repeated connection attempts")
        self.print_divider()
        attacker = "attacker_device"
        for i in range(1, 5):
            ok, role, status = self.authenticate_device(attacker)
            print(f"Attempt {i}: {status}")
            if status == "BLOCKED":
                print("System response: device temporarily blocklisted")
                break

        print()

        # Scenario 5
        self.print_divider()
        print("[Scenario 5] Unauthorized GATT write attempt by attacker")
        self.print_divider()
        attacker_role = "attacker"
        action = "write_characteristic"
        allowed = self.check_access(attacker_role, action)
        print("User role:", attacker_role)
        print("Requested action:", action)
        print("Access control:", "ALLOWED" if allowed else "DENIED")
        if not allowed:
            print("System response: characteristic write blocked")

        print()

        # Scenario 6
        self.print_divider()
        print("[Scenario 6] Intercepted encrypted traffic")
        self.print_divider()
        encrypted_payload = self.read_medical_data()
        success, decrypted_payload = self.decrypt_payload(encrypted_payload)
        print("Original medical data: ECG / SpO2 values")
        print("Intercepted payload:", encrypted_payload.decode())
        print("Authorized decryption result:", decrypted_payload if success else "FAILED")
        print("Attacker observation: payload is unreadable without the key")

        print()

        # Scenario 7
        self.print_divider()
        print("[Scenario 7] Tampered encrypted traffic")
        self.print_divider()
        encrypted_payload = self.read_medical_data()

        tampered_payload = bytearray(encrypted_payload)
        tampered_payload[-1] = tampered_payload[-1] ^ 1
        tampered_payload = bytes(tampered_payload)

        success, decrypted_payload = self.decrypt_payload(tampered_payload)
        print("Tampered payload:", tampered_payload.decode(errors="ignore"))
        print("Integrity check:", "PASSED" if success else "FAILED")
        if not success:
            print("System response: packet rejected due to integrity verification failure")

        print()

        # Scenario 8
        self.show_logs()


if __name__ == "__main__":
    system = SecureBLEMedicalIoTSystem()
    system.run_demo()


