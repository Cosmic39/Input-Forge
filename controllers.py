"""Input controllers for mouse and keyboard interactions."""

from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController


class InputController:
    """Manages mouse and keyboard input events."""

    def __init__(self):
        """Initialize mouse and keyboard controllers."""
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def execute_mouse_click(self, button):
        """
        Execute a mouse click event.
        
        Args:
            button: pynput.mouse.Button instance (left, right, middle, x1, x2)
        """
        self.mouse.click(button)

    def execute_keyboard_key(self, key):
        """
        Execute a keyboard key press and release.
        
        Args:
            key: pynput.keyboard.Key instance or character string
        """
        self.keyboard.press(key)
        self.keyboard.release(key)

    def execute_input_event(self, action_type, target):
        """
        Execute an input event based on type and target.
        
        Args:
            action_type (str): "mouse" or "keyboard"
            target: pynput button or key
        """
        if action_type == "mouse":
            self.execute_mouse_click(target)
        elif action_type == "keyboard":
            self.execute_keyboard_key(target)
