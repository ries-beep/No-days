import re
import customtkinter as ctk
from tkinter import PhotoImage
from spellchecker import SpellChecker

# Appearance settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Suspicious word list
words = [
    "www", "hurry", "urgent", "immediate action required", "act now", "verify your account",
    "your account has been suspended", "unusual activity detected", "your account is locked",
    "limited time offer", "final notice", "security alert", "unauthorized login attempt",
    "failure to act will result in suspension", "update your billing information", "payment declined",
    "refund available", "transaction failed", "invoice attached", "you have a pending payment",
    "claim your reward", "earn money fast", "bank notification", "account balance alert",
    "reset your password", "confirm your identity", "secure your account", "click to login",
    "verify your credentials", "password expired", "security update required",
    "congratulations, you've won", "you've been selected", "free gift", "exclusive offer",
    "you're a lucky winner", "claim your prize now", "get rich quick", "microsoft support",
    "apple id alert", "amazon customer service", "paypal notification", "irs notice", "your bank",
    "it department", "ceo request", "hr department", "view attachment", "click here",
    "open document", "access your statement", "check the file", "download now", "login here",
    "don't share this with anyone", "this is confidential", "act discreetly", "you must comply",
    "failure to comply will result in consequences", "avoid penalties", "your package is on hold",
    "action needed to restore access", "your email storage is full", "account scheduled for deletion",
    "click here to stop this", "account deactivation", "confirm your account", "your action is required",
    "important notice", "secure link", "security check", "identity confirmation", "verify immediately",
    "login from new device", "review recent activity", "credential update required",
    "your account needs attention", "billing issue", "past due notice", "email access blocked",
    "you are in violation", "unauthorized payment", "click to resolve", "urgent attention needed",
    "security token expired", "verify your login", "account warning", "compliance notice",
    "service disruption", "click to proceed", "suspicious transaction", "pressing matter",
    "login credentials required", "complete your profile", "new terms of service", "important update",
    "login attempt detected", "multi-factor authentication disabled", "reactivation link",
    "document awaiting signature", "e-signature required", "contract update", "reset link inside",
    "unauthorized withdrawal", "it security alert", "account configuration error",
    "payment confirmation needed", "restricted access", "security verification step",
    "one-time password required", "otp verification needed", "you must take action"
]

# Known TLDs
tlds = [".com", ".org", ".edu", ".gov", ".us", ".net", ".biz", ".info"]

# Functions
def extract_tlds(text):
    return re.findall(r"\.[a-zA-Z]{2,}", text)

def contains_http_or_https(text):
    if "http://" in text and "https://" not in text:
        return "http"
    elif "https://" in text:
        return "https"
    return None

def on_click():
    user_input = entry.get().strip()
    inslink = link.get().strip()
    spell = SpellChecker()
    zero = 0

    if not user_input and not inslink:
        result_label.configure(text="Input fields are empty.")
        threat_label.configure(text="")
        wrong_spell.configure(text="")
        linkresult.configure(text="")
        linkboxresult.configure(text="")
        return

    found_words = [word for word in words if re.search(rf'\b{re.escape(word)}\b', user_input, re.IGNORECASE)]
    count = len(found_words)
    message = f"Detected suspicious words ({count}): {', '.join(found_words)}" if count > 0 else "No suspicious words detected."

    input_words = re.findall(r'\b\w+\b', user_input)
    misspelled = spell.unknown(input_words)
    cspelling = len(misspelled)
    message3 = f"Misspelled words: {', '.join(misspelled)}" if misspelled else "No misspelled words detected."

    message_tlds = extract_tlds(user_input)
    unknown_tlds_message = [tld for tld in message_tlds if tld not in tlds]

    if contains_http_or_https(user_input) == "http":
        message4 = "Link in message box: ⚠ Message uses HTTP (not secure)."
        zero += 1
    elif unknown_tlds_message:
        message4 = f"Link in message box: ⚠ Suspicious Domain: {', '.join(unknown_tlds_message)}"
        zero += 1
    else:
        message4 = "No suspicious links found in message."

    link_tlds = extract_tlds(inslink)
    unknown_tlds_link = [tld for tld in link_tlds if tld not in tlds]

    if contains_http_or_https(inslink) == "http":
        message5 = "Link in link box: ⚠ Link uses HTTP (not secure)."
        zero += 1
    elif unknown_tlds_link:
        message5 = f"Link in link box: ⚠ Suspicious Domain: {', '.join(unknown_tlds_link)}"
        zero += 1
    else:
        message5 = "No suspicious links found in link."

    # Threat analysis
    analysis = count + zero + cspelling
    if analysis >= 6:
        message2 = "⚠ Threat Level: 100% | Confirmed phishing - STOP immediately!"
    elif analysis == 5:
        message2 = "⚠ Threat Level: 50% | Moderate scam risk - proceed with caution."
    elif analysis == 4:
        message2 = "⚠ Threat Level: 40% | Mild threat - likely phishing."
    elif analysis == 3:
        message2 = "⚠ Threat Level: 30% | Mild threat - inspect the content."
    elif analysis == 2:
        message2 = "⚠ Threat Level: 20% | Low threat - something looks off."
    elif analysis == 1:
        message2 = "⚠ Threat Level: 10% | Minimal threat - review it carefully."
    else:
        message2 = "✅ Threat Level: 0% | Safe - nothing suspicious detected."

    result_label.configure(text=message, text_color="red")
    threat_label.configure(text=message2, text_color="orange")
    wrong_spell.configure(text=message3, text_color="yellow")
    linkresult.configure(text=message4, text_color="red")
    linkboxresult.configure(text=message5, text_color="red")

# GUI
root = ctk.CTk()
root.title("Phishing Detector")
root.geometry("1000x600")

main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20, anchor="w")

header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
header_frame.pack(anchor="w", pady=(0, 20))

# Logo
try:
    logo_img = PhotoImage(file="logo.ico")
    logo_label = ctk.CTkLabel(header_frame, image=logo_img, text="", compound="left")
    logo_label.pack(side="left", padx=(0, 10))
except Exception as e:
    print("Logo not found:", e)
    ctk.CTkLabel(header_frame, text="🛡️", font=ctk.CTkFont(size=24)).pack(side="left", padx=(0, 10))

header_label = ctk.CTkLabel(
    header_frame,
    text="Phishing Message Detector",
    font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
    text_color="#f5f5f5"
)
header_label.pack(side="left")

# Message Entry
entry_label = ctk.CTkLabel(main_frame, text="Input the message:",
                           font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"), text_color="#f5f5f5")
entry_label.pack(anchor="w", pady=(10, 0))

entry = ctk.CTkEntry(main_frame, width=500, font=ctk.CTkFont(size=14))
entry.pack(anchor="w", ipady=4, pady=5)

# Link Entry
link_label = ctk.CTkLabel(main_frame, text="Input the link (optional):",
                          font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"), text_color="#f5f5f5")
link_label.pack(anchor="w", pady=(10, 0))

link = ctk.CTkEntry(main_frame, width=500, font=ctk.CTkFont(size=14))
link.pack(anchor="w", ipady=4, pady=5)

button = ctk.CTkButton(
    main_frame,
    text="Scan",
    command=on_click,
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="#3E2D8A",
    hover_color="#5540B3"
)
button.pack(anchor="w", pady=20)

# Output Labels
result_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12), text_color="red")
result_label.pack(anchor="w", pady=2)

threat_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="orange")
threat_label.pack(anchor="w", pady=2)

wrong_spell = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12, slant="italic"), text_color="yellow")
wrong_spell.pack(anchor="w", pady=2)

linkresult = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12), text_color="red")
linkresult.pack(anchor="w", pady=2)

linkboxresult = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12), text_color="red")
linkboxresult.pack(anchor="w", pady=2)

root.mainloop()
