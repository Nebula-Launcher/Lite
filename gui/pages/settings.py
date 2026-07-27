import os
import tkinter as tk
from tkinter import filedialog

from gui.widgets.styled import StyledFrame, StyledCard, StyledLabel, StyledHeading, StyledButton, StyledEntry


class SettingsPage(tk.Frame):
    def __init__(self, master, theme, config, launcher, theme_manager=None, on_theme_change=None, **kw):
        kw["bg"] = theme.get("bg", "#1e1e2e")
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.theme = theme
        self.config = config
        self.launcher = launcher
        self.theme_manager = theme_manager
        self._on_theme_change = on_theme_change

        self._build_ui()

    def _build_ui(self):
        t = self.theme
        for w in self.winfo_children():
            w.destroy()

        tk.Frame(self, bg=t.get("bg", "#1e1e2e"), height=24).pack()

        StyledHeading(self, t, "Settings", size_key="title_size").pack(anchor="w", padx=28)
        StyledLabel(self, t, text="Configure your launcher",
                     fg=t.get("muted", "#6c7086")).pack(anchor="w", padx=28, pady=(2, 16))

        # Username
        card = StyledCard(self, t)
        card.pack(fill="x", padx=24, pady=(0, 12))
        StyledLabel(card, t, text="Username", fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 6))
        self._username_entry = StyledEntry(card, t, placeholder="Enter username", width=30)
        self._username_entry.pack(fill="x")
        self._username_entry.set(self.config.username)

        # RAM
        card2 = StyledCard(self, t)
        card2.pack(fill="x", padx=24, pady=(0, 12))
        StyledLabel(card2, t, text="RAM Allocation (MB)", fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 6))
        ram_row = tk.Frame(card2, bg=t.get("card_bg", "#252536"))
        ram_row.pack(fill="x")
        self._ram_entry = StyledEntry(ram_row, t, placeholder="4096", width=10)
        self._ram_entry.pack(side="left")
        self._ram_entry.set(str(self.config.ram_mb))
        StyledLabel(ram_row, t, text="MB (min 512)",
                     fg=t.get("muted", "#6c7086")).pack(side="left", padx=(8, 0))

        # Minecraft Directory
        card3 = StyledCard(self, t)
        card3.pack(fill="x", padx=24, pady=(0, 12))
        StyledLabel(card3, t, text="Minecraft Directory", fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 6))
        dir_row = tk.Frame(card3, bg=t.get("card_bg", "#252536"))
        dir_row.pack(fill="x")
        self._dir_entry = StyledEntry(dir_row, t, placeholder="~/.nebula", width=30)
        self._dir_entry.pack(side="left", fill="x", expand=True)
        self._dir_entry.set(self.config.minecraft_directory)
        browse_btn = StyledButton(dir_row, t, text="Browse", width=70,
                                   command=self._browse_dir,
                                   bg_key="button_bg", fg_key="button_fg",
                                   hover_key="button_hover")
        browse_btn.pack(side="right")

        # Theme
        card4 = StyledCard(self, t)
        card4.pack(fill="x", padx=24, pady=(0, 12))
        StyledLabel(card4, t, text="Theme", fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 6))
        theme_row = tk.Frame(card4, bg=t.get("card_bg", "#252536"))
        theme_row.pack(fill="x")

        self._theme_var = tk.StringVar(value=self.theme_manager.current_name if self.theme_manager else "dark")

        if self.theme_manager:
            for name in self.theme_manager.get_theme_names():
                rb = tk.Radiobutton(theme_row, text=name.replace("_", " ").title(),
                                     variable=self._theme_var, value=name,
                                     bg=t.get("card_bg", "#252536"),
                                     fg=t.get("fg", "#cdd6f4"),
                                     selectcolor=t.get("button_bg", "#313244"),
                                     activebackground=t.get("card_bg", "#252536"),
                                     activeforeground=t.get("fg", "#cdd6f4"),
                                     font=(t.get("font_family", "Segoe UI"),
                                           t.get("font_size", 11)),
                                     command=self._on_theme_select)
                rb.pack(side="left", padx=(0, 16))

        # Save button
        btn_frame = tk.Frame(self, bg=t.get("bg", "#1e1e2e"))
        btn_frame.pack(fill="x", padx=24, pady=(8, 0))

        save_btn = StyledButton(btn_frame, t, text="Save Settings", width=120,
                                 bg_key="accent", fg_key="button_fg",
                                 hover_key="accent_hover",
                                 command=self._save)
        save_btn.pack(side="left")

        self._save_status = StyledLabel(btn_frame, t, text="",
                                         fg=t.get("success", "#a6e3a1"))
        self._save_status.pack(side="left", padx=(12, 0))

    def _browse_dir(self):
        path = filedialog.askdirectory(title="Select Minecraft Directory")
        if path:
            self._dir_entry.set(path)

    def _on_theme_select(self):
        if self.theme_manager and self._on_theme_change:
            name = self._theme_var.get()
            self.theme_manager.set_theme(name)
            self._on_theme_change(name)

    def _save(self):
        username = self._username_entry.get().strip()
        ram_str = self._ram_entry.get().strip()
        mc_dir = self._dir_entry.get().strip()

        if username:
            self.config.username = username

        if ram_str.isdigit() and int(ram_str) >= 512:
            self.config.ram_mb = int(ram_str)

        if mc_dir:
            self.config.minecraft_directory = mc_dir
            self.launcher.mc_dir = mc_dir

        self.config.save()
        self._save_status.configure(text="Settings saved!")

    def refresh_data(self):
        self._username_entry.set(self.config.username)
        self._ram_entry.set(str(self.config.ram_mb))
        self._dir_entry.set(self.config.minecraft_directory)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        self._build_ui()
