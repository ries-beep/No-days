import string
import customtkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

def check_password_complexity(password):
    special_characters = string.punctuation
    
    has_uppercase = any(char.isupper() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(char in special_characters for char in password)
    
    return {
        "Uppercase": has_uppercase,
        "Number": has_number,
        "Special_character": has_special,
        "is_complex": has_uppercase and has_number and has_special
    }

class PasswordCheckerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Checker")
        self.geometry("450x400")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self.main_frame, 
            text="Enter Password to Check", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(10, 5), sticky="ew")

        # MODIFICATION: Removed 'show="*"', so the input is visible
        self.password_entry = customtkinter.CTkEntry(
            self.main_frame, 
            placeholder_text="Password", 
            width=300
        )
        self.password_entry.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        self.check_button = customtkinter.CTkButton(
            self.main_frame, 
            text="Check Strength", 
            command=self.update_results
        )
        self.check_button.grid(row=2, column=0, pady=10)

        self.results_frame = customtkinter.CTkFrame(self.main_frame)
        self.results_frame.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.labels = {}
        row_count = 0
        
        self.labels['title'] = customtkinter.CTkLabel(
            self.results_frame, 
            text="REQUIREMENTS:",
            font=customtkinter.CTkFont(weight="bold")
        )
        self.labels['title'].grid(row=row_count, column=0, sticky="w", padx=10, pady=(5, 0))
        row_count += 1
        
        self.labels['uppercase'] = self.create_result_label(self.results_frame, "Uppercase Letter:", row_count)
        row_count += 1
        
        self.labels['number'] = self.create_result_label(self.results_frame, "Number (Digit):", row_count)
        row_count += 1
        
        self.labels['special'] = self.create_result_label(self.results_frame, "Special Character:", row_count)
        row_count += 1

        self.overall_label = customtkinter.CTkLabel(
            self.results_frame, 
            text="Enter a password and click 'Check'!", 
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color="yellow"
        )
        self.overall_label.grid(row=row_count, column=0, columnspan=2, pady=(10, 5), padx=10)


    def create_result_label(self, parent, text, row):
        label = customtkinter.CTkLabel(parent, text=text, anchor="w")
        label.grid(row=row, column=0, sticky="w", padx=10, pady=2)
        
        status_label = customtkinter.CTkLabel(parent, text="—", anchor="e")
        status_label.grid(row=row, column=1, sticky="e", padx=10, pady=2)
        return status_label

    def update_results(self):
        password = self.password_entry.get()
        if not password:
            self.overall_label.configure(text=" Empty input password.", text_color="red")
            self.labels['uppercase'].configure(text="?", text_color="red")
            self.labels['number'].configure(text="?", text_color="red")
            self.labels['special'].configure(text="?", text_color="red")
            return

        results = check_password_complexity(password)
        
        self.set_label_status(self.labels['uppercase'], results['Uppercase'])
        self.set_label_status(self.labels['number'], results['Number'])
        self.set_label_status(self.labels['special'], results['Special_character'])

        if results['is_complex']:
            self.overall_label.configure(
                text="Strong password!", 
                text_color="lime"
            )
        else:
            self.overall_label.configure(
                text="Weak password", 
                text_color="red"
            )

    def set_label_status(self, label, status):
        if status:
            label.configure(text="YES", text_color="lime")
        else:
            label.configure(text="NO", text_color="red")


if __name__ == "__main__":
    app = PasswordCheckerApp()
    app.mainloop()