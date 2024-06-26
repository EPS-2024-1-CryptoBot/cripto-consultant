import re
import tkinter as tk
from tkinter import messagebox


class InputKeysWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Insira as suas chaves...")

        # Set window size and center it on the screen
        window_width = 600
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Set background color
        bg_color = '#111827'  # Converted rgb(17, 24, 39) to hexadecimal
        root.configure(bg=bg_color)

        # Configure grid layout
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Define common style options
        label_options = {'bg': bg_color, 'fg': 'white'}
        entry_options = {'bg': 'white', 'fg': 'black'}
        button_options = {'bg': 'white', 'fg': 'black'}

        # Binance keys
        self.binance_api_key_label = tk.Label(root, text="Binance API Key", **label_options)
        self.binance_api_key_label.grid(column=0, row=0, padx=20, pady=10, sticky=tk.W)
        self.binance_api_key_entry = tk.Entry(root, **entry_options)
        self.binance_api_key_entry.grid(column=0, row=1, padx=20, pady=10, sticky=tk.EW)

        self.binance_secret_key_label = tk.Label(root, text="Binance Secret Key", **label_options)
        self.binance_secret_key_label.grid(column=0, row=2, padx=20, pady=10, sticky=tk.W)
        self.binance_secret_key_entry = tk.Entry(root, **entry_options)
        self.binance_secret_key_entry.grid(column=0, row=3, padx=20, pady=10, sticky=tk.EW)

        # Bitmex keys
        self.bitmex_api_key_label = tk.Label(root, text="Bitmex API Key", **label_options)
        self.bitmex_api_key_label.grid(column=1, row=0, padx=20, pady=10, sticky=tk.W)
        self.bitmex_api_key_entry = tk.Entry(root, **entry_options)
        self.bitmex_api_key_entry.grid(column=1, row=1, padx=20, pady=10, sticky=tk.EW)

        self.bitmex_secret_key_label = tk.Label(root, text="Bitmex Secret Key", **label_options)
        self.bitmex_secret_key_label.grid(column=1, row=2, padx=20, pady=10, sticky=tk.W)
        self.bitmex_secret_key_entry = tk.Entry(root, **entry_options)
        self.bitmex_secret_key_entry.grid(column=1, row=3, padx=20, pady=10, sticky=tk.EW)

        # Submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.validate_keys, **button_options)
        self.submit_button.grid(column=0, row=4, columnspan=2, pady=20)

    def validate_keys(self):
        binance_api_key = self.binance_api_key_entry.get()
        binance_secret_key = self.binance_secret_key_entry.get()
        bitmex_api_key = self.bitmex_api_key_entry.get()
        bitmex_secret_key = self.bitmex_secret_key_entry.get()

        if not self.is_valid_binance_key(binance_api_key, binance_secret_key):
            print(f"Invalid Binance API Key or Secret Key: API Key: {binance_api_key}, Secret Key: {binance_secret_key}")
            messagebox.showerror("Error", "Invalid Binance API Key or Secret Key")
            return

        if not self.is_valid_bitmex_key(bitmex_api_key, bitmex_secret_key):
            print(f"Invalid Bitmex API Key or Secret Key: API Key: {bitmex_api_key}, Secret Key: {bitmex_secret_key}")
            messagebox.showerror("Error", "Invalid Bitmex API Key or Secret Key")
            return

        self.root.destroy()

        self.binance_keys = (binance_api_key, binance_secret_key)
        self.bitmex_keys = (bitmex_api_key, bitmex_secret_key)

    @staticmethod
    def is_valid_binance_key(api_key, secret_key):
        if len(api_key) != 64:
            print(f"Binance API Key length error: {api_key}")
            return False
        if not re.match(r'^[A-Fa-f0-9]+$', api_key):
            print(f"Binance API Key regex error: {api_key}")
            return False
        if len(secret_key) != 64:
            print(f"Binance Secret Key length error: {secret_key}")
            return False
        if not re.match(r'^[A-Fa-f0-9]+$', secret_key):
            print(f"Binance Secret Key regex error: {secret_key}")
            return False
        return True

    @staticmethod
    def is_valid_bitmex_key(api_key, secret_key):
        if len(api_key) != 24:
            print(f"Bitmex API Key length error: {api_key}")
            return False
        if not re.match(r'^[A-Za-z0-9]+$', api_key):
            print(f"Bitmex API Key regex error: {api_key}")
            return False
        if len(secret_key) != 48:
            print(f"Bitmex Secret Key length error: {secret_key}")
            return False
        if not re.match(r'^[A-Za-z0-9_\-]+$', secret_key):
            print(f"Bitmex Secret Key regex error: {secret_key}")
            return False
        return True


def get_api_keys():
    root = tk.Tk()
    app = InputKeysWindow(root)
    root.mainloop()
    return app.binance_keys, app.bitmex_keys
