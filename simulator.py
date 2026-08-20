"""Simulation engine for automated input events."""

import time
from controllers import InputController
from config import BENCHMARK_UPDATE_INTERVAL


class SimulationEngine:
    """Handles the core simulation logic and event execution."""

    def __init__(self):
        """Initialize the simulation engine."""
        self.input_controller = InputController()
        self.is_running = False
        self.total_events = 0
        self.start_timestamp = 0.0
        self.actual_cps = 0.0

    def execute_event(self, action_type, target):
        """
        Execute a single input event.
        
        Args:
            action_type (str): "mouse" or "keyboard"
            target: pynput button or key
        """
        self.input_controller.execute_input_event(action_type, target)

    def reset_counters(self):
        """Reset benchmark counters."""
        self.total_events = 0
        self.actual_cps = 0.0
        self.start_timestamp = 0.0

    def calculate_metrics(self):
        """
        Calculate current CPS and accuracy metrics.
        
        Returns:
            tuple: (actual_cps, accuracy_percentage)
        """
        elapsed = time.perf_counter() - self.start_timestamp
        if elapsed > 0:
            self.actual_cps = self.total_events / elapsed
            return self.actual_cps, self.total_events
        return 0.0, 0

    def update_event_count(self):
        """Increment event counter and return True if update UI needed."""
        self.total_events += 1
        return self.total_events % BENCHMARK_UPDATE_INTERVAL == 0

    def run_simulation(self, target_cps, action_type, target, max_duration=None,
                       on_update_callback=None, on_stop_callback=None):
        """
        Run the simulation worker loop.
        
        Args:
            target_cps (float): Target clicks per second
            action_type (str): "mouse" or "keyboard"
            target: pynput button or key
            max_duration (float): Maximum duration in seconds (None for unlimited)
            on_update_callback (callable): Callback for benchmark updates
            on_stop_callback (callable): Callback when simulation stops
        """
        self.is_running = True
        self.reset_counters()
        self.start_timestamp = time.perf_counter()

        interval = 1.0 / target_cps
        next_event_time = time.perf_counter()

        while self.is_running:
            now = time.perf_counter()

            # Check max duration
            if max_duration and (now - self.start_timestamp) >= max_duration:
                break

            # Execute event if interval has passed
            if now >= next_event_time:
                self.execute_event(action_type, target)
                if self.update_event_count():
                    elapsed = time.perf_counter() - self.start_timestamp
                    if elapsed > 0:
                        self.actual_cps = self.total_events / elapsed
                        if on_update_callback:
                            on_update_callback(self.actual_cps, self.total_events)
                next_event_time += interval
            else:
                sleep_delta = next_event_time - now
                if sleep_delta > 0.002:
                    time.sleep(sleep_delta - 0.001)

        self.is_running = False
        if on_stop_callback:
            on_stop_callback()

    def stop(self):
        """Stop the simulation."""
        self.is_running = False
