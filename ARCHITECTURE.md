"""
Dependency Graph and Module Flow

MAIN APPLICATION FLOW:
======================

main.py (Application Entry Point)
    ├─→ imports UIController from ui.py
    ├─→ imports SimulationEngine from simulator.py
    │
    ├─→ UIController
    │    └─→ imports config.py (for constants and styling)
    │    └─→ CustomTitleBar (window management)
    │    └─→ BenchmarkDisplay (metrics dashboard)
    │
    ├─→ SimulationEngine
    │    └─→ imports InputController from controllers.py
    │    └─→ imports config.py (for benchmarking settings)
    │
    ├─→ KeyboardListener (from pynput)
    │    └─→ Global hotkey handling
    │
    └─→ Threading
         └─→ Simulation runs in daemon thread


MODULE DEPENDENCIES:
====================

main.py
  ├── ui.py
  │    └── config.py
  ├── simulator.py
  │    ├── controllers.py
  │    └── config.py
  ├── config.py
  └── pynput.keyboard (external)

ui.py
  └── config.py (constants, colors, settings)
       └── pynput (mouse, keyboard for key definitions)

simulator.py
  ├── controllers.py
  │    └── pynput.keyboard (external)
  │    └── pynput.mouse (external)
  └── config.py

controllers.py
  └── pynput.keyboard (external)
  └── pynput.mouse (external)

config.py
  └── pynput.keyboard (external)
  └── pynput.mouse (external)


CONFIGURATION FLOW:
===================

1. User sets values in UI (config.py provides defaults)
2. UI.get_*() methods retrieve values with validation
3. main.py passes values to SimulationEngine
4. SimulationEngine uses InputController to execute events
5. SimulationEngine tracks metrics and calls callbacks
6. UI updates benchmark display with callback data


EVENT FLOW:
===========

User Action → KeyboardListener → main._on_key_press()
                ↓
            Check mode (Toggle/Hold)
                ↓
            Start/Stop simulation
                ↓
            SimulationEngine.run_simulation()
                ↓
            InputController.execute_input_event()
                ↓
            OS receives input


CALLBACK FLOW:
==============

SimulationEngine.run_simulation()
    ↓
    (every N events)
    ↓
    on_update_callback()
    ↓
    UIController.update_benchmark()
    ↓
    BenchmarkDisplay.update_metrics()


INITIALIZATION SEQUENCE:
========================

1. WindowsButtonSimulatorApp.__init__()
2. → SimulationEngine() created
3. → UIController() created
4.   → CustomTitleBar() created
5.   → BenchmarkDisplay() created
6.   → All ComboBox/Entry widgets populated from config.py
7. → KeyboardListener() started
8. → UIController.show() → mainloop()


SHUTDOWN SEQUENCE:
==================

1. User closes window
2. _on_app_close() triggered
3. engine.is_running = False
4. listener.stop()
5. window.destroy()
6. Program exits


KEY CONFIGURATION POINTS:
=========================

To modify behavior, edit:

Appearance:
  • config.py - COLOR_* constants

Key Mappings:
  • config.py - MOUSE_KEYS, KEYBOARD_KEYS, ACTIVATION_KEYS_MAP

Defaults:
  • config.py - DEFAULT_* constants

Simulation Logic:
  • simulator.py - SimulationEngine.run_simulation()

Input Execution:
  • controllers.py - InputController methods

UI Layout/Styling:
  • ui.py - UIController._create_main_content()


TESTING INDIVIDUAL MODULES:
============================

Test InputController:
  from controllers import InputController
  controller = InputController()
  from pynput.mouse import Button
  controller.execute_mouse_click(Button.left)

Test SimulationEngine:
  from simulator import SimulationEngine
  engine = SimulationEngine()
  engine.run_simulation(100, "mouse", Button.left)

Test Config Values:
  import config
  print(config.COLOR_ACCENT_SOFT)
  print(config.ALL_KEYS_MAP)

Test UI:
  from ui import UIController
  def dummy_start(): pass
  def dummy_stop(): pass
  ui = UIController(lambda: None, dummy_start, dummy_stop)
  print(ui.get_target_cps())
"""
