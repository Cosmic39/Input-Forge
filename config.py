"""Configuration and constants for Windows Button Simulator."""

import customtkinter as ctk
from pynput.keyboard import Key
from pynput.mouse import Button

# Initialize customtkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Color Palette - Soft Red Theme
COLOR_BG = "#121212"
COLOR_HEADER = "#1E1E1E"
COLOR_TEXT = "#E0E0E0"
COLOR_ACCENT_SOFT = "#D32F2F"
COLOR_ACCENT_HOVER = "#B71C1C"
COLOR_BORDER_SOFT = "#E57373"
COLOR_INPUT_BG = "#1E1E1E"

# Window Settings
WINDOW_TITLE = "Windows Button Simulator Pro"
WINDOW_GEOMETRY = "620x690"

# CPS Range
MIN_CPS = 1.0
MAX_CPS = 1000.0
DEFAULT_CPS = 100.0

# Default Start Delay
DEFAULT_START_DELAY = 0.0

# Duration Options
DURATION_OPTIONS = [
    "Unlimited",
    "5 Seconds",
    "10 Seconds",
    "30 Seconds",
    "60 Seconds",
]
DEFAULT_DURATION = "Unlimited"

# Mode Options
MODE_OPTIONS = [
    "Toggle (Press to Start/Stop)",
    "Hold (Active while Pressed)",
]
DEFAULT_MODE = "Toggle (Press to Start/Stop)"

# Activation Keys (F1-F12)
ACTIVATION_KEYS_MAP = {
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12,
}
DEFAULT_ACTIVATION_KEY = "F8"

# Mouse Keys
MOUSE_KEYS = {
    "Mouse: Left Click": ("mouse", Button.left),
    "Mouse: Right Click": ("mouse", Button.right),
    "Mouse: Middle Click": ("mouse", Button.middle),
    "Mouse: Button 4 (X1)": ("mouse", Button.x1),
    "Mouse: Button 5 (X2)": ("mouse", Button.x2),
}
DEFAULT_MOUSE_KEY = "Mouse: Right Click"

# Keyboard Keys (A-Z, 0-9, Special Keys)
KEYBOARD_KEYS = {
    "Key: Space": ("keyboard", Key.space),
    "Key: Enter": ("keyboard", Key.enter),
    "Key: Tab": ("keyboard", Key.tab),
    "Key: Shift": ("keyboard", Key.shift),
    "Key: Ctrl": ("keyboard", Key.ctrl),
    "Key: Alt": ("keyboard", Key.alt),
}

# Add A-Z keys
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    KEYBOARD_KEYS[f"Key: {char}"] = ("keyboard", char.lower())

# Add 0-9 keys
for num in "0123456789":
    KEYBOARD_KEYS[f"Key: {num}"] = ("keyboard", num)

# Combined all keys map
ALL_KEYS_MAP = {**MOUSE_KEYS, **KEYBOARD_KEYS}

# ASCII Art Signature
ASCII_SIGNATURE = (
    "██████   ██    ██         ██████  ██████  ███████ ███    ███ ██  ██████ \n"
    "██   ██   ██  ██   ██    ██      ██    ██ ██      ████  ████ ██ ██      \n"
    "██████     ████          ██      ██    ██ ███████ ██ ████ ██ ██ ██      \n"
    "██   ██     ██     ██    ██      ██    ██      ██ ██  ██  ██ ██ ██      \n"
    "██████      ██            ██████  ██████  ███████ ██      ██ ██  ██████ \n"
)

# Benchmark Update Interval (every N events)
BENCHMARK_UPDATE_INTERVAL = 20
