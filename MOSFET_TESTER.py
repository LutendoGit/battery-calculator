import time
import csv
from datetime import datetime

class MOSFETTester:
    def __init__(self, mosfet_id, type='N-channel'):
        self.mosfet_id = mosfet_id
        self.type = type
        self.results = {}

    def log_gate_voltage(self, voltage):
        self.results['Gate Voltage (V)'] = voltage
        self.results['Gate Status'] = 'ON' if voltage > 2.5 else 'OFF'

    def log_continuity(self, drain_to_source_continuity):
        self.results['Drain-Source Continuity'] = 'Yes' if drain_to_source_continuity else 'No'

    def log_body_diode(self, diode_drop):
        self.results['Body Diode Drop (V)'] = diode_drop
        self.results['Diode Direction'] = 'Forward' if 0.4 < diode_drop < 0.8 else 'Unexpected'

    def export_results(self, filename='mosfet_test_log.csv'):
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Timestamp', 'MOSFET ID', 'Type'] + list(self.results.keys()))
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({'Timestamp': datetime.now().isoformat(), 'MOSFET ID': self.mosfet_id, 'Type': self.type, **self.results})

    def display_summary(self):
        print(f"\n🔍 MOSFET Test Summary: {self.mosfet_id}")
        for k, v in self.results.items():
            print(f"  {k}: {v}")

# Example usage
if __name__ == "__main__":
    tester = MOSFETTester("Q1_Discharge")
    tester.log_gate_voltage(3.3)  # Simulated gate voltage
    tester.log_continuity(True)   # Simulated continuity test
    tester.log_body_diode(0.65)   # Simulated diode drop
    tester.display_summary()
    tester.export_results()
