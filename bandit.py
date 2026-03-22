import customtkinter as ctk
import subprocess
import threading
from tkinter import filedialog, messagebox
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # Options: "blue", "green", "dark-blue"

class BanditScannerApp(ctk.CTk):
    """
    A CustomTkinter application for running the Bandit security scanner.
    Uses threading to keep the GUI responsive during the scanning process.
    """
    def __init__(self):
        super().__init__()

        # --- Basic Setup ---
        self.title("Bandit Security Scanner")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # --- Configuration Variables ---
        self.input_path = ctk.StringVar(value=os.getcwd())
        self.output_filename = ctk.StringVar(value="bandit_report.txt")
        
        # Check for Bandit installation
        try:
            subprocess.run(["bandit", "--version"], check=True, capture_output=True)
            self.bandit_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.bandit_available = False
            messagebox.showerror("Error", "Bandit is not installed or not found in PATH.\nInstall with: pip install bandit")

        # --- Widgets Setup ---
        self._create_input_frame()
        self._create_output_frame()
        self._create_run_button()
        self._create_results_textbox()

    def _create_input_frame(self):
        """Creates the frame for selecting the file/directory to scan."""
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Target File/Directory:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.input_entry = ctk.CTkEntry(input_frame, textvariable=self.input_path)
        self.input_entry.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="ew")

        # Frame to hold the two browse buttons (Directory and File)
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")
        
        ctk.CTkButton(button_frame, text="File...", command=self._browse_file_path, width=80).grid(row=0, column=0, padx=(0, 5), sticky="e")
        ctk.CTkButton(button_frame, text="Directory...", command=self._browse_directory_path, width=80).grid(row=0, column=1, padx=(5, 0), sticky="e")


    def _create_output_frame(self):
        """Creates the frame for specifying the output report filename."""
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(output_frame, text="Output Report Name:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.output_entry = ctk.CTkEntry(output_frame, textvariable=self.output_filename)
        self.output_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def _create_run_button(self):
        """Creates the main button to start the scan."""
        self.run_button = ctk.CTkButton(self, 
                                        text="Run Bandit Scan", 
                                        command=self._start_bandit_thread, 
                                        height=40,
                                        state="normal" if self.bandit_available else "disabled")
        self.run_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def _create_results_textbox(self):
        """Creates the textbox to display the Bandit output."""
        ctk.CTkLabel(self, text="Scan Results:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, padx=20, pady=(0, 5), sticky="sw")
        
        self.results_textbox = ctk.CTkTextbox(self, wrap="word")
        self.results_textbox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.results_textbox.insert("end", "Welcome to the Bandit Scanner. Select a file or directory and click 'Run Bandit Scan'.")
        self.results_textbox.configure(state="disabled") # Make it read-only initially

    def _browse_directory_path(self):
        """Opens a directory dialog and updates the input path variable."""
        path = filedialog.askdirectory(title="Select Directory to Scan")
        if path:
            self.input_path.set(path)

    def _browse_file_path(self):
        """Opens a file dialog (specifically for Python files) and updates the input path variable."""
        path = filedialog.askopenfilename(
            title="Select Python File to Scan",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if path:
            self.input_path.set(path)
            
    def _start_bandit_thread(self):
        """Starts the Bandit scan in a separate thread to prevent GUI freezing."""
        # Disable button while running
        self.run_button.configure(state="disabled", text="Scanning... Please Wait")
        
        # Clear previous results
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", "Starting Bandit scan...\n\n")
        self.results_textbox.configure(state="disabled")
        
        # Start the background thread
        threading.Thread(target=self._run_bandit_core, daemon=True).start()

    def _run_bandit_core(self):
        """
        The core function executed in the thread. Runs the bandit command,
        saves the output, and updates the GUI.
        """
        input_file_or_dir = self.input_path.get()
        output_file = self.output_filename.get()
        
        # Basic validation
        if not input_file_or_dir or not os.path.exists(input_file_or_dir):
            self._update_ui_after_run("Error: Invalid or non-existent input path.", success=False)
            return

        try:
            # Construct the command. We use '-r' for recursive scan, which handles both files and dirs.
            command = ["bandit", "-r", input_file_or_dir]
            
            # Execute Bandit
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=False, # Do not raise error for non-zero exit code (Bandit uses exit codes for findings)
                encoding='utf-8'
            )

            # Save the full output to the specified file
            try:
                with open(output_file, "w", encoding='utf-8') as f:
                    f.write(result.stdout)
            except IOError as e:
                self._update_ui_after_run(f"Error saving file '{output_file}': {e}", success=False)
                return

            # Display results in the GUI
            output_message = result.stdout
            
            # Check for errors (Bandit might print to stderr if there's a serious issue, like a non-existent path)
            if result.stderr:
                output_message = f"--- Bandit Execution Errors/Warnings ---\n{result.stderr}\n\n--- Full Bandit Output ---\n{output_message}"
                success = False
            else:
                success = True

            self._update_ui_after_run(output_message, output_file, success=success)

        except Exception as e:
            self._update_ui_after_run(f"An unexpected error occurred during execution: {e}", success=False)

    def _update_ui_after_run(self, result_text, output_file=None, success=True):
        """Updates the GUI elements once the thread completes."""
        
        # Use self.after to safely update CTk widgets from the non-main thread
        self.after(0, lambda: self._finalize_ui_update(result_text, output_file, success))

    def _finalize_ui_update(self, result_text, output_file, success):
        """The actual UI update function, called from the main thread."""
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", result_text)
        self.results_textbox.configure(state="disabled")

        if success:
            final_message = f"Bandit scan completed successfully."
            if output_file:
                 final_message += f"\nFull report saved to: {os.path.abspath(output_file)}"
            
            messagebox.showinfo("Scan Complete", final_message)
        else:
            messagebox.showerror("Scan Failed/Error", "The Bandit scan encountered an issue. See the Results box for details.")

        # Re-enable the button
        self.run_button.configure(state="normal", text="Run Bandit Scan")


if __name__ == "__main__":
    app = BanditScannerApp()
    app.mainloop()
