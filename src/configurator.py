import tkinter as tk
from tkinter import messagebox
import winreg
import sys

def save_to_registry(api_url, api_key):
    try:
        registry_path = r"Software\TicketMaker"
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        winreg.SetValueEx(key, "URL", 0, winreg.REG_SZ, api_url)
        winreg.SetValueEx(key, "API_KEY", 0, winreg.REG_SZ, api_key)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to the registry: {e}")
        return False

def submit():
    api_url = url_entry.get()
    api_key = key_entry.get()
    if not api_url or not api_key:
        messagebox.showwarning("Input Error", "Both fields are required!")
        return
    if save_to_registry(api_url, api_key):
        messagebox.showinfo("Success", "API URL and Key saved successfully!")
        root.destroy()

def set_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg="grey")
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg="black")
    def on_focus_out(event):
        if not entry.get():
            set_placeholder(entry, placeholder_text)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Parse command-line arguments
prepopulated_url = sys.argv[1] if len(sys.argv) > 1 else "https://yourcompany.freshdesk.com"
prepopulated_key = sys.argv[2] if len(sys.argv) > 2 else "Your Freshdesk account API key"

# Create the GUI
root = tk.Tk()
root.title("TicketMaker Configuration")

instructions = (
    "This is part of the TicketMaker installation process.\n\n"
    "Please enter your Freshdesk URL and API key below to complete the TicketMaker setup."
)
tk.Label(root, text=instructions, justify="left", wraplength=400, fg="blue").grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))

# API URL
tk.Label(root, text="Freshdesk URL:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=40)
url_entry.grid(row=1, column=1, padx=10, pady=10)
url_entry.insert(0, prepopulated_url)

# API Key
tk.Label(root, text="Freshdesk API Key:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
key_entry = tk.Entry(root, width=40)
key_entry.grid(row=2, column=1, padx=10, pady=10)
key_entry.insert(0, prepopulated_key)

# Submit button
submit_button = tk.Button(root, text="Save", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))

root.mainloop()