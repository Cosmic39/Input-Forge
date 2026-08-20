"""UI components and window management."""

import customtkinter as ctk
import config as cfg


class CustomTitleBar:
    """Custom window title bar with drag and close/minimize buttons."""

    def __init__(self, parent, on_close_callback):
        """
        Initialize the custom title bar.
        
        Args:
            parent: Parent widget
            on_close_callback: Callback function for close button
        """
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=cfg.COLOR_HEADER,
            corner_radius=0,
            height=45,
            border_width=1,
            border_color="#2A2A2A",
        )
        self.frame.pack(side="top", fill="x")

        self._parent = parent
        self._x = 0
        self._y = 0

        self._create_title_bar(on_close_callback)

    def _create_title_bar(self, on_close_callback):
        """Create title bar elements."""
        self.frame.bind("<Button-1>", self._start_drag)
        self.frame.bind("<B1-Motion>", self._do_drag)

        title_label = ctk.CTkLabel(
            self.frame,
            text=cfg.WINDOW_TITLE,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        )
        title_label.pack(side="left", padx=15, pady=8)
        title_label.bind("<Button-1>", self._start_drag)
        title_label.bind("<B1-Motion>", self._do_drag)

        close_btn = ctk.CTkButton(
            self.frame,
            text="✕",
            width=45,
            height=45,
            corner_radius=0,
            fg_color="transparent",
            hover_color=cfg.COLOR_ACCENT_HOVER,
            text_color=cfg.COLOR_TEXT,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=on_close_callback,
        )
        close_btn.pack(side="right")

        minimize_btn = ctk.CTkButton(
            self.frame,
            text="—",
            width=45,
            height=45,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#333333",
            text_color=cfg.COLOR_TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._minimize_window(),
        )
        minimize_btn.pack(side="right")

    def _start_drag(self, event):
        """Start window drag."""
        self._x = event.x
        self._y = event.y

    def _do_drag(self, event):
        """Perform window drag."""
        x = self._parent.winfo_x() + (event.x - self._x)
        y = self._parent.winfo_y() + (event.y - self._y)
        self._parent.geometry(f"+{x}+{y}")

    def _minimize_window(self):
        """Minimize the window."""
        self._parent.overrideredirect(False)
        self._parent.iconify()
        self._parent.bind("<FocusIn>", self._restore_window)

    def _restore_window(self, event):
        """Restore the window."""
        self._parent.overrideredirect(True)


class BenchmarkDisplay:
    """Benchmark and analytics dashboard."""

    def __init__(self, parent):
        """
        Initialize the benchmark display.
        
        Args:
            parent: Parent widget
        """
        self.frame = ctk.CTkFrame(
            parent,
            fg_color="#181818",
            border_color="#333333",
            border_width=1,
            corner_radius=8,
        )

        self.lbl_cps = ctk.CTkLabel(
            self.frame,
            text="Actual CPS: 0.0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888",
        )
        self.lbl_cps.pack(side="left", padx=15, pady=8)

        self.lbl_events = ctk.CTkLabel(
            self.frame,
            text="Events: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888",
        )
        self.lbl_events.pack(side="left", padx=15, pady=8)

        self.lbl_accuracy = ctk.CTkLabel(
            self.frame,
            text="Accuracy: 0%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888",
        )
        self.lbl_accuracy.pack(side="left", padx=15, pady=8)

    def update_metrics(self, cps, events, target_cps):
        """
        Update benchmark metrics display.
        
        Args:
            cps (float): Actual CPS
            events (int): Total events executed
            target_cps (float): Target CPS for accuracy calculation
        """
        self.lbl_cps.configure(
            text=f"Actual CPS: {cps:.1f}",
            text_color=cfg.COLOR_BORDER_SOFT
        )
        self.lbl_events.configure(
            text=f"Events: {events}",
            text_color=cfg.COLOR_BORDER_SOFT
        )
        accuracy = min(100.0, (cps / target_cps) * 100) if target_cps > 0 else 0.0
        self.lbl_accuracy.configure(
            text=f"Accuracy: {accuracy:.1f}%",
            text_color=cfg.COLOR_BORDER_SOFT
        )

    def pack_in_grid(self, parent, row, columnspan, padx, pady):
        """Pack frame into grid layout."""
        self.frame.grid(
            row=row, column=0, columnspan=columnspan, padx=padx, pady=pady, sticky="ew"
        )


class UIController:
    """Main UI controller for the application."""

    def __init__(self, on_close_callback, on_start_callback, on_stop_callback):
        """
        Initialize the UI controller.
        
        Args:
            on_close_callback: Callback when window closes
            on_start_callback: Callback when simulator starts
            on_stop_callback: Callback when simulator stops
        """
        self.window = ctk.CTk()
        self.window.title(cfg.WINDOW_TITLE)
        self.window.geometry(cfg.WINDOW_GEOMETRY)
        self.window.overrideredirect(True)
        self.window.configure(fg_color=cfg.COLOR_BG)

        self._on_start_callback = on_start_callback
        self._on_stop_callback = on_stop_callback

        # Create UI elements
        CustomTitleBar(self.window, on_close_callback)
        self._create_main_content()

    def _create_main_content(self):
        """Create main content area with all input controls."""
        content_frame = ctk.CTkFrame(
            self.window,
            fg_color=cfg.COLOR_BG,
            corner_radius=12,
            border_width=2,
            border_color=cfg.COLOR_BORDER_SOFT,
        )
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=1)

        # Selected Key
        ctk.CTkLabel(
            content_frame,
            text="Selected Key:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=0, column=0, padx=20, pady=(15, 8), sticky="w")

        self.combo_selected_key = ctk.CTkComboBox(
            content_frame,
            values=list(cfg.ALL_KEYS_MAP.keys()),
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            button_color=cfg.COLOR_ACCENT_SOFT,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=260,
            height=32,
        )
        self.combo_selected_key.set(cfg.DEFAULT_MOUSE_KEY)
        self.combo_selected_key.grid(row=0, column=1, padx=(0, 20), pady=(15, 8), sticky="w")

        # Activation Key
        ctk.CTkLabel(
            content_frame,
            text="Activation Key:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=1, column=0, padx=20, pady=8, sticky="w")

        self.combo_toggle_key = ctk.CTkComboBox(
            content_frame,
            values=list(cfg.ACTIVATION_KEYS_MAP.keys()),
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            button_color=cfg.COLOR_ACCENT_SOFT,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=260,
            height=32,
        )
        self.combo_toggle_key.set(cfg.DEFAULT_ACTIVATION_KEY)
        self.combo_toggle_key.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="w")

        # Mode
        ctk.CTkLabel(
            content_frame,
            text="Mode:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=2, column=0, padx=20, pady=8, sticky="w")

        self.combo_mode = ctk.CTkComboBox(
            content_frame,
            values=cfg.MODE_OPTIONS,
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            button_color=cfg.COLOR_ACCENT_SOFT,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=260,
            height=32,
        )
        self.combo_mode.set(cfg.DEFAULT_MODE)
        self.combo_mode.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="w")

        # Target CPS
        ctk.CTkLabel(
            content_frame,
            text="Target CPS (1-1000):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=3, column=0, padx=20, pady=8, sticky="w")

        self.entry_cps = ctk.CTkEntry(
            content_frame,
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=120,
            height=32,
        )
        self.entry_cps.insert(0, str(cfg.DEFAULT_CPS))
        self.entry_cps.grid(row=3, column=1, padx=(0, 20), pady=8, sticky="w")

        # Start Delay
        ctk.CTkLabel(
            content_frame,
            text="Start Delay (sec):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=4, column=0, padx=20, pady=8, sticky="w")

        self.entry_delay = ctk.CTkEntry(
            content_frame,
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=120,
            height=32,
        )
        self.entry_delay.insert(0, str(cfg.DEFAULT_START_DELAY))
        self.entry_delay.grid(row=4, column=1, padx=(0, 20), pady=8, sticky="w")

        # Duration
        ctk.CTkLabel(
            content_frame,
            text="Duration:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=cfg.COLOR_TEXT,
        ).grid(row=5, column=0, padx=20, pady=8, sticky="w")

        self.combo_duration = ctk.CTkComboBox(
            content_frame,
            values=cfg.DURATION_OPTIONS,
            font=ctk.CTkFont(size=12),
            fg_color=cfg.COLOR_INPUT_BG,
            button_color=cfg.COLOR_ACCENT_SOFT,
            border_color=cfg.COLOR_BORDER_SOFT,
            border_width=1.5,
            corner_radius=6,
            width=180,
            height=32,
        )
        self.combo_duration.set(cfg.DEFAULT_DURATION)
        self.combo_duration.grid(row=5, column=1, padx=(0, 20), pady=8, sticky="w")

        # Benchmark Display
        self.benchmark = BenchmarkDisplay(content_frame)
        self.benchmark.pack_in_grid(content_frame, 6, 2, 20, 10)

        # Status Label
        self.lbl_status = ctk.CTkLabel(
            content_frame,
            text="Status: STOPPED (Press ESC for Emergency Stop)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#A0A0A0",
        )
        self.lbl_status.grid(row=7, column=0, columnspan=2, padx=20, pady=(2, 5))

        # Action Toggle Button
        self.btn_apply = ctk.CTkButton(
            content_frame,
            text="START SIMULATOR",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=cfg.COLOR_ACCENT_SOFT,
            hover_color=cfg.COLOR_ACCENT_HOVER,
            text_color=cfg.COLOR_TEXT,
            height=40,
            corner_radius=8,
            command=self._on_toggle,
        )
        self.btn_apply.grid(row=8, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")

        # ASCII Signature
        ascii_label = ctk.CTkLabel(
            content_frame,
            text=cfg.ASCII_SIGNATURE,
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color=cfg.COLOR_BORDER_SOFT,
            justify="center",
        )
        ascii_label.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

    def _on_toggle(self):
        """Handle toggle button click."""
        if self.btn_apply.cget("text") == "START SIMULATOR":
            self._start_simulator()
        else:
            self._stop_simulator()

    def _start_simulator(self):
        """Start the simulator."""
        self.btn_apply.configure(
            text="STOP SIMULATOR",
            fg_color="#2A2A2A",
            hover_color="#3A3A3A"
        )
        self.combo_selected_key.configure(state="disabled")
        self.entry_cps.configure(state="disabled")
        self.lbl_status.configure(text="Status: RUNNING...")
        if self._on_start_callback:
            self._on_start_callback()

    def _stop_simulator(self):
        """Stop the simulator."""
        self.btn_apply.configure(
            text="START SIMULATOR",
            fg_color=cfg.COLOR_ACCENT_SOFT,
            hover_color=cfg.COLOR_ACCENT_HOVER,
        )
        self.lbl_status.configure(
            text="Status: STOPPED (Press ESC for Emergency Stop)",
            text_color="#A0A0A0",
        )
        self.combo_selected_key.configure(state="normal")
        self.entry_cps.configure(state="normal")
        if self._on_stop_callback:
            self._on_stop_callback()

    def get_selected_key(self):
        """Get the selected key mapping."""
        key_str = self.combo_selected_key.get()
        return cfg.ALL_KEYS_MAP.get(key_str, ("mouse", None))

    def get_activation_key(self):
        """Get the activation key."""
        key_str = self.combo_toggle_key.get()
        return cfg.ACTIVATION_KEYS_MAP.get(key_str)

    def get_mode(self):
        """Get the selected mode."""
        return self.combo_mode.get()

    def get_target_cps(self):
        """Get target CPS value."""
        try:
            cps = float(self.entry_cps.get())
            return max(cfg.MIN_CPS, min(cfg.MAX_CPS, cps))
        except ValueError:
            return cfg.DEFAULT_CPS

    def get_start_delay(self):
        """Get start delay value."""
        try:
            delay = float(self.entry_delay.get())
            return max(0.0, delay)
        except ValueError:
            return 0.0

    def get_max_duration(self):
        """Get max duration value."""
        val = self.combo_duration.get()
        if "5" in val:
            return 5.0
        if "10" in val:
            return 10.0
        if "30" in val:
            return 30.0
        if "60" in val:
            return 60.0
        return None

    def update_benchmark(self, cps, events):
        """Update benchmark display."""
        target_cps = self.get_target_cps()
        self.benchmark.update_metrics(cps, events, target_cps)

    def set_status(self, text):
        """Set status label text."""
        self.lbl_status.configure(text=text)

    def show(self):
        """Show the window."""
        self.window.mainloop()
