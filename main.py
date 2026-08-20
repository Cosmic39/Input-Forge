"""Main application entry point for Windows Button Simulator."""

import threading
import time
from pynput.keyboard import Key, Listener as KeyboardListener

from ui import UIController
from simulator import SimulationEngine
import config as cfg


class WindowsButtonSimulatorApp:
    """Main application class orchestrating UI and simulation."""

    def __init__(self):
        """Initialize the application."""
        self.engine = SimulationEngine()
        self.simulation_thread = None
        
        # Initialize UI with callbacks
        self.ui = UIController(
            on_close_callback=self._on_app_close,
            on_start_callback=self._on_start_click,
            on_stop_callback=self._on_stop_click,
        )

        # Start global hotkey listener
        self.listener = KeyboardListener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()

    def _on_start_click(self):
        """Handle start button click."""
        if self.simulation_thread is None or not self.simulation_thread.is_alive():
            self.engine.is_running = True
            self.simulation_thread = threading.Thread(
                target=self._run_simulation,
                daemon=True
            )
            self.simulation_thread.start()

    def _on_stop_click(self):
        """Handle stop button click."""
        self.engine.stop()

    def _run_simulation(self):
        """Run the simulation in a separate thread."""
        start_delay = self.ui.get_start_delay()
        
        # Handle start delay countdown
        if start_delay > 0:
            for remaining in range(int(start_delay), 0, -1):
                if not self.engine.is_running:
                    return
                self.ui.set_status(f"Status: Starting in {remaining}s...")
                time.sleep(1.0)

        if not self.engine.is_running:
            return

        # Get configuration
        target_cps = self.ui.get_target_cps()
        action_type, target = self.ui.get_selected_key()
        max_duration = self.ui.get_max_duration()

        if target is None:
            self.ui.set_status("Status: STOPPED - Invalid key selected")
            self.ui._stop_simulator()
            return

        # Define callbacks
        def on_update(cps, events):
            self.ui.update_benchmark(cps, events)

        def on_stop():
            self.ui._stop_simulator()

        # Run simulation
        self.engine.is_running = True
        self.engine.run_simulation(
            target_cps=target_cps,
            action_type=action_type,
            target=target,
            max_duration=max_duration,
            on_update_callback=on_update,
            on_stop_callback=on_stop
        )

    def _on_key_press(self, key):
        """Handle global key press events."""
        # Emergency stop with ESC
        if key == Key.esc:
            if self.engine.is_running:
                self.engine.stop()
            return

        # Activation key
        activation_key = self.ui.get_activation_key()
        if key == activation_key:
            mode = self.ui.get_mode()
            if "Toggle" in mode:
                self.ui._on_toggle()
            elif "Hold" in mode and not self.engine.is_running:
                self._on_start_click()

    def _on_key_release(self, key):
        """Handle global key release events."""
        activation_key = self.ui.get_activation_key()
        if key == activation_key:
            mode = self.ui.get_mode()
            if "Hold" in mode and self.engine.is_running:
                self._on_stop_click()

    def _on_app_close(self):
        """Handle application close."""
        self.engine.is_running = False
        self.listener.stop()
        self.ui.window.destroy()

    def run(self):
        """Start the application."""
        self.ui.show()


if __name__ == "__main__":
    app = WindowsButtonSimulatorApp()
    app.run()
