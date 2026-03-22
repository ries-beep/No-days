import customtkinter
import socket
import re
import threading # Use threading to keep the GUI responsive during the scan

# --- Configuration and Patterns ---
# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Regular Expression Pattern to extract the number of ports you want to scan.
port_range_pattern = re.compile(r"([0-9]+)-([0-9]+)")

# --- Main Application Class ---
class PortScannerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- Setup Window ---
        self.title("Nmap")
        self.geometry("600x450")
        customtkinter.set_appearance_mode("Dark")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # --- Variables ---
        self.ip_address = customtkinter.StringVar(value="127.0.0.1")
        self.port_range = customtkinter.StringVar(value="80-100")
        self.scan_running = False

        # --- Create Widgets ---

        # 1. IP Address Input
        self.ip_label = customtkinter.CTkLabel(self, text="Target IP Address:")
        self.ip_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.ip_entry = customtkinter.CTkEntry(self, textvariable=self.ip_address, width=200)
        self.ip_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # 2. Port Range Input
        self.port_label = customtkinter.CTkLabel(self, text="Port Range (e.g., 80-100):")
        self.port_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.port_entry = customtkinter.CTkEntry(self, textvariable=self.port_range, width=200)
        self.port_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # 3. Scan Button
        self.scan_button = customtkinter.CTkButton(self, text="Start Scan", command=self.start_scan_thread)
        self.scan_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # 4. Results Text Box
        self.results_label = customtkinter.CTkLabel(self, text="Scan Results:")
        self.results_label.grid(row=3, column=0, padx=20, pady=5, sticky="sw")
        self.results_textbox = customtkinter.CTkTextbox(self, width=550, height=150)
        self.results_textbox.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

        
        self.grid_rowconfigure(4, weight=5)



    def port_scan_logic(self):
        self.results_textbox.delete("1.0", "end") 
        self.results_textbox.insert("end", "Starting scan...\n")
        self.scan_running = True
        self.scan_button.configure(state="disabled", text="Scanning...")

        ip_add_entered = self.ip_address.get().strip()
        port_range_str = self.port_range.get().strip().replace(" ", "")
        open_ports = []
        port_min = 0
        port_max = 0

        # Validate IP Address
        if not ip_add_pattern.search(ip_add_entered):
            self.results_textbox.insert("end", f"ERROR: '{ip_add_entered}' is an invalid IP address.\n")
            self.scan_running = False
            self.scan_button.configure(state="normal", text="Start Scan")
            return

        # Validate Port Range
        port_range_valid = port_range_pattern.search(port_range_str)
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            if port_min > port_max:
                self.results_textbox.insert("end", "ERROR: Start port must be less than or equal to end port.\n")
                self.scan_running = False
                self.scan_button.configure(state="normal", text="Start Scan")
                return
        else:
            self.results_textbox.insert("end", f"ERROR: Port range '{port_range_str}' is invalid. Use format: <int>-<int>.\n")
            self.scan_running = False
            self.scan_button.configure(state="normal", text="Start Scan")
            return

        self.results_textbox.insert("end", f"Scanning {ip_add_entered} from port {port_min} to {port_max}...\n")


        for port in range(port_min, port_max + 1):
            try:
                # Update status in real-time (optional, can slow down scan)
                self.results_textbox.insert("end", f"port {port}|\r")
                self.results_textbox.see("end")
                self.update() # Update the GUI

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.05)  # Shorter timeout for faster GUI demo
                    result = s.connect_ex((ip_add_entered, port))
                    
                    if result == 0:
                        open_ports.append(port)
                        self.results_textbox.insert("end", f"Port {port} is OPEN!\n")
                        self.results_textbox.see("end")
                        self.update()

            except Exception as e:
                
                self.results_textbox.insert("end", f"An error occurred: {e}\n")
                break

        self.results_textbox.insert("end", "-"*30 + "\n")
        if open_ports:
            self.results_textbox.insert("end", f"Scan Complete. Open ports on {ip_add_entered}:\n")
            for port in open_ports:
                self.results_textbox.insert("end", f"-> Port {port}\n")
        else:
            self.results_textbox.insert("end", f"Scan Complete. No open ports found in the range {port_min}-{port_max}.\n")

        
        self.scan_running = False
        self.scan_button.configure(state="normal", text="Start Scan")


    def start_scan_thread(self):
        if not self.scan_running:
            # Create and start a new thread for the port scan
            scan_thread = threading.Thread(target=self.port_scan_logic)
            scan_thread.start()


if __name__ == "__main__":
    app = PortScannerApp()
    app.mainloop()