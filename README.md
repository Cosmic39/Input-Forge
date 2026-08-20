# ⚒️ Input Forge

**Input Forge** is a modular Windows input simulation and benchmarking application built with Python, CustomTkinter, and `pynput`.

It provides configurable keyboard and mouse input simulation with adjustable timing, activation modes, emergency controls, and real-time performance metrics.

> **Project Status:** Active Development  
> **Version:** 0.1.0  
> **Platform:** Windows

---

## ✨ Features

### 🖥️ Modern Interface

- Dark-themed CustomTkinter interface
- Custom draggable title bar
- Soft-red accent theme
- Simple control-oriented layout
- Real-time simulation status

### 🖱️ Mouse Simulation

Supports:

- Left Click
- Right Click
- Middle Click
- Mouse Button 4 / X1
- Mouse Button 5 / X2

### ⌨️ Keyboard Simulation

Supports:

- `A-Z`
- `0-9`
- Space
- Enter
- Tab
- Shift
- Ctrl
- Alt

### ⚡ Activation System

Choose an activation key from:

```text
F1 - F12
```

Two activation modes are available:

- **Toggle** — press the activation key to start/stop
- **Hold** — simulation remains active while the activation key is held

### ⏱️ Simulation Control

Configure:

- Target CPS
- Start delay
- Simulation duration
- Unlimited operation
- Toggle/Hold activation

Supported duration presets:

```text
Unlimited
5 Seconds
10 Seconds
30 Seconds
60 Seconds
```

### 📊 Real-Time Benchmarking

Input Forge tracks:

- Actual CPS
- Total generated events
- Target-vs-actual accuracy
- Simulation runtime metrics

The simulation engine periodically sends metric updates to the UI through callbacks.

### 🛑 Emergency Stop

Press:

```text
ESC
```

to immediately stop an active simulation.

---

# 🏗️ Architecture

Input Forge is divided into separate modules so that the UI, input execution, simulation engine, and configuration remain independent.

```text
                    ┌─────────────────┐
                    │     main.py     │
                    │ Application Core│
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
       ┌──────▼──────┐              ┌──────▼────────┐
       │    ui.py    │              │ simulator.py  │
       │     UI      │              │ Simulation    │
       └──────┬──────┘              │    Engine     │
              │                     └──────┬────────┘
              │                            │
       ┌──────▼──────┐              ┌──────▼────────┐
       │  config.py  │              │controllers.py │
       │ Configuration│              │ Input Layer  │
       └─────────────┘              └──────┬────────┘
                                           │
                                    ┌──────▼──────┐
                                    │   pynput    │
                                    │ Mouse/Keys  │
                                    └─────────────┘
```

The documented application flow is:

```text
User Action
     ↓
KeyboardListener
     ↓
Activation Mode
     ↓
SimulationEngine
     ↓
InputController
     ↓
Operating System Input
```



---

# 📁 Project Structure

```text
InputForge/
│
├── main.py
├── config.py
├── controllers.py
├── simulator.py
├── ui.py
│
├── tests/
│
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
└── LICENSE
```

## `main.py`

Application entry point and orchestration layer.

Responsible for:

- Creating the application
- Connecting the UI and simulation engine
- Global keyboard listener management
- Thread management
- Event callback routing
- Application startup/shutdown



---

## `config.py`

Central configuration module.

Contains:

- Theme colors
- Window configuration
- Mouse mappings
- Keyboard mappings
- Activation key mappings
- CPS limits
- Duration options
- Default UI values



---

## `controllers.py`

Input execution layer.

Responsible for communicating with the operating system through `pynput`.

Handles:

- Mouse input
- Keyboard input
- Input event execution



---

## `simulator.py`

Core simulation engine.

Responsible for:

- Simulation loop
- Event timing
- Input execution
- Benchmark calculations
- Event counters
- Callback-based metric updates
- Thread-safe simulation state



---

## `ui.py`

User interface layer.

Contains:

- `CustomTitleBar`
- `BenchmarkDisplay`
- `UIController`
- UI controls
- Layout and styling
- User configuration handling



---

# 🔄 Configuration Flow

```text
User Configuration
        ↓
      UI
        ↓
Configuration Validation
        ↓
SimulationEngine
        ↓
InputController
        ↓
Input Event
        ↓
Benchmark Metrics
        ↓
UI Dashboard
```

The UI retrieves and validates user settings before passing them to the simulation engine, which executes the events and reports metrics back through callbacks.

---

# 🚀 Installation

## Requirements

- Windows
- Python 3.8+
- `customtkinter`
- `pynput`

Install dependencies:

```bash
pip install customtkinter pynput
```

Or, if the repository includes `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running From Source

From the project directory:

```bash
python main.py
```

---

# 🎮 Quick Start

1. Launch Input Forge.
2. Select the input you want to simulate.
3. Select an activation key (`F1-F12`).
4. Choose **Toggle** or **Hold** mode.
5. Set the target CPS.
6. Configure an optional start delay.
7. Select a duration.
8. Press **START SIMULATOR** or the configured activation key.
9. Monitor CPS, event count, and accuracy.
10. Press `ESC` to perform an emergency stop.

---

# 📦 Building the Windows Executable

Input Forge can be packaged using PyInstaller.

Example:

```bash
pyinstaller --onefile --windowed --name "Input Forge" --icon="assets/inputforge.ico" main.py
```

The resulting executable will be placed in:

```text
dist/
└── Input Forge.exe
```

For development and debugging, an `--onedir` build is recommended before creating the final `--onefile` release.

---

# 🧪 Testing

The modular architecture allows individual components to be tested independently.

Example:

```python
from controllers import InputController
```

Simulation components can also be instantiated independently from the UI.

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for module-level testing examples and dependency flow.

---

# 🛠️ Extending Input Forge

## Add a New Input Type

1. Add the input mapping in `config.py`.
2. Implement its execution method in `controllers.py`.
3. Update `simulator.py` if additional simulation logic is required.

## Modify the UI

UI layout and styling are primarily handled by:

```text
ui.py
```

Theme constants are centralized in:

```text
config.py
```

## Add Activation Keys

Activation keys are defined in:

```text
config.py
```

Add the desired key to the activation mapping and expose it through the UI configuration.

## Modify Simulation Behavior

Core simulation behavior is located in:

```text
simulator.py
```

This is where timing, event execution, and benchmark behavior can be extended.

---

# ⚙️ Performance

Input Forge is designed to keep simulation work separate from the UI.

The simulation runs in a daemon thread, uses `time.perf_counter()` for timing, periodically updates the UI through callbacks, and uses adaptive sleeping to reduce unnecessary CPU usage.

---

# 🐛 Troubleshooting

### Simulation does not start

Check:

- The selected input is valid.
- The activation key is not being captured by another application.
- The CPS value is within the supported range.

### Accuracy is lower than expected

System performance can affect timing accuracy.

Try:

- Lowering the target CPS.
- Closing resource-intensive applications.
- Running the application without unnecessary background workloads.

### Application becomes difficult to control

Press:

```text
ESC
```

to trigger the emergency stop.

---

# 🗺️ Roadmap

Potential future development:

- [ ] Input profiles
- [ ] Macro sequences
- [ ] Input recording
- [ ] Input replay
- [ ] Configurable event sequences
- [ ] Import/export of profiles
- [ ] Expanded benchmark statistics
- [ ] Additional input backends
- [ ] Plugin architecture
- [ ] Improved automated testing
- [ ] Release packaging and versioning

---

# 📚 Documentation

Additional architecture documentation is available in:

```text
ARCHITECTURE.md
```

It contains:

- Dependency graph
- Module flow
- Configuration flow
- Event flow
- Callback flow
- Initialization sequence
- Shutdown sequence
- Configuration points
- Module testing examples

---

# 🤝 Contributing

Contributions, improvements, bug reports, and feature ideas are welcome.

A typical development workflow:

```bash
git clone <repository-url>
cd InputForge
pip install -r requirements.txt
python main.py
```

Before submitting changes:

1. Keep modules focused on their responsibilities.
2. Avoid unnecessary coupling between UI and core logic.
3. Test changes before submitting them.
4. Update documentation when behavior or architecture changes.

---

# 📜 License

Input Forge is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

# 👨‍💻 Author

**Cosmic**

Built as an experimentation and development project around Windows input simulation, automation concepts, and software architecture.

---

## ⚠️ Disclaimer

Input Forge generates synthetic keyboard and mouse input on the user's computer.

Use it responsibly and only in environments where automated input is permitted. Some applications, games, services, or anti-cheat systems may prohibit automated input or simulated interactions.

---

**Input Forge — Forge your inputs.**
