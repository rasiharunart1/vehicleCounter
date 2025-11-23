import psutil
import serial.tools.list_ports

target_port = "COM5"
found = False

# List all serial ports for reference
print("Available serial ports:")
for port in serial.tools.list_ports.comports():
    print(f" - {port.device}")

# Check each process for handles to COM14
print(f"\nChecking which process is using {target_port}...\n")
for proc in psutil.process_iter(['pid', 'name']):
    try:
        for conn in proc.open_files():
            if target_port.lower() in conn.path.lower():
                print(f"PID: {proc.pid} | Name: {proc.name()} | Path: {conn.path}")
                found = True
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

if not found:
    print(f"{target_port} is not in use by any process (or needs admin rights to detect).")