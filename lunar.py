import json
import os
import sys
import customtkinter as ctk
from pynput import keyboard
from termcolor import colored
import threading
import tkinter as tk
from tkinter import messagebox

class SyntharGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Synthar.cc - Neural Network Aimbot")
        self.geometry("800x600")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Synthar.cc", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Status: Disabled", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        # Main settings frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        # Load config
        self.config = self.load_config()
        
        # Sensitivity settings
        self.xy_sens = ctk.CTkSlider(self.settings_frame, from_=1, to=100, command=self.update_config)
        self.xy_sens.grid(row=0, column=1, padx=(20, 10), pady=(10, 0), sticky="ew")
        self.xy_sens.set(self.config.get("xy_sens", 10))
        
        self.xy_sens_label = ctk.CTkLabel(self.settings_frame, text="XY Sensitivity:")
        self.xy_sens_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        
        # Targeting sensitivity
        self.targeting_sens = ctk.CTkSlider(self.settings_frame, from_=1, to=100, command=self.update_config)
        self.targeting_sens.grid(row=1, column=1, padx=(20, 10), pady=(10, 0), sticky="ew")
        self.targeting_sens.set(self.config.get("targeting_sens", 10))
        
        self.targeting_sens_label = ctk.CTkLabel(self.settings_frame, text="Targeting Sensitivity:")
        self.targeting_sens_label.grid(row=1, column=0, padx=10, pady=(10, 0))
        
        # AI Confidence
        self.confidence = ctk.CTkSlider(self.settings_frame, from_=0.1, to=1.0, command=self.update_config)
        self.confidence.grid(row=2, column=1, padx=(20, 10), pady=(10, 0), sticky="ew")
        self.confidence.set(0.45)
        
        self.confidence_label = ctk.CTkLabel(self.settings_frame, text="AI Confidence:")
        self.confidence_label.grid(row=2, column=0, padx=10, pady=(10, 0))
        
        # Triggerbot switch
        self.triggerbot = ctk.CTkSwitch(self.settings_frame, text="Triggerbot", command=self.update_config)
        self.triggerbot.grid(row=3, column=0, padx=10, pady=(10, 0), columnspan=2)
        self.triggerbot.select()
        
        # Resolution settings
        self.res_frame = ctk.CTkFrame(self.settings_frame)
        self.res_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew")
        
        self.res_x = ctk.CTkEntry(self.res_frame, placeholder_text="Width")
        self.res_x.grid(row=0, column=1, padx=10, pady=10)
        self.res_x.insert(0, str(self.config.get("screen_res_x", 1920)))
        
        self.res_y = ctk.CTkEntry(self.res_frame, placeholder_text="Height")
        self.res_y.grid(row=0, column=2, padx=10, pady=10)
        self.res_y.insert(0, str(self.config.get("screen_res_y", 1080)))
        
        # Start button
        self.start_button = ctk.CTkButton(self.sidebar_frame, text="Start", command=self.start_aimbot)
        self.start_button.grid(row=2, column=0, padx=20, pady=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_aimbot)
        self.stop_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.aimbot_thread = None
        self.running = False

    def load_config(self):
        try:
            with open('lib/config/config.json', 'r') as f:
                return json.load(f)
        except:
            return {"xy_sens": 10, "targeting_sens": 10}

    def update_config(self, *args):
        config = {
            "xy_sens": self.xy_sens.get(),
            "targeting_sens": self.targeting_sens.get(),
            "xy_scale": 10/self.xy_sens.get(),
            "targeting_scale": 1000/(self.targeting_sens.get() * self.xy_sens.get())
        }
        
        os.makedirs("lib/config", exist_ok=True)
        with open('lib/config/config.json', 'w') as f:
            json.dump(config, f)

    def start_aimbot(self):
        if not self.running:
            self.running = True
            self.status_label.configure(text="Status: Running")
            self.aimbot_thread = threading.Thread(target=self.run_aimbot)
            self.aimbot_thread.daemon = True
            self.aimbot_thread.start()

    def stop_aimbot(self):
        self.running = False
        self.status_label.configure(text="Status: Disabled")
        if self.aimbot_thread:
            self.aimbot_thread.join()

    def run_aimbot(self):
        from lib.aimbot import Aimbot
        aimbot = Aimbot(collect_data=False)
        while self.running:
            try:
                aimbot.start()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                break

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = SyntharGUI()
    app.mainloop()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    main()