import threading
import tkinter as tk
from tkinter import messagebox

from gui.widgets.styled import StyledFrame, StyledCard, StyledLabel, StyledHeading, StyledButton, StyledEntry
from gui.widgets.progress import InstallProgress


class HomePage(tk.Frame):
    def __init__(self, master, theme, config, launcher, **kw):
        kw["bg"] = theme.get("bg", "#1e1e2e")
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.theme = theme
        self.config = config
        self.launcher = launcher
        self._launching = False

        self._build_ui()

    def _build_ui(self):
        t = self.theme
        for w in self.winfo_children():
            w.destroy()

        padding = tk.Frame(self, bg=t.get("bg", "#1e1e2e"), height=24)
        padding.pack()

        heading = StyledHeading(self, t, "Play Minecraft", size_key="title_size")
        heading.pack(anchor="w", padx=28)

        subtitle = StyledLabel(self, t, text="Launch your game",
                               fg=t.get("muted", "#6c7086"))
        subtitle.pack(anchor="w", padx=28, pady=(2, 16))

        info_card = StyledCard(self, t)
        info_card.pack(fill="x", padx=24, pady=(0, 16))

        row1 = tk.Frame(info_card, bg=t.get("card_bg", "#252536"))
        row1.pack(fill="x", pady=2)
        StyledLabel(row1, t, text="Username:", fg=t.get("muted", "#6c7086"),
                    width=12, anchor="w").pack(side="left")
        self._username_label = StyledLabel(row1, t, text=self.config.username)
        self._username_label.pack(side="left")

        row2 = tk.Frame(info_card, bg=t.get("card_bg", "#252536"))
        row2.pack(fill="x", pady=2)
        StyledLabel(row2, t, text="RAM:", fg=t.get("muted", "#6c7086"),
                    width=12, anchor="w").pack(side="left")
        self._ram_label = StyledLabel(row2, t, text=f"{self.config.ram_mb} MB")
        self._ram_label.pack(side="left")

        row3 = tk.Frame(info_card, bg=t.get("card_bg", "#252536"))
        row3.pack(fill="x", pady=2)
        StyledLabel(row3, t, text="MC Directory:", fg=t.get("muted", "#6c7086"),
                    width=12, anchor="w").pack(side="left")
        self._dir_label = StyledLabel(row3, t, text=self.config.minecraft_directory,
                                       wraplength=400)
        self._dir_label.pack(side="left")

        version_card = StyledCard(self, t)
        version_card.pack(fill="x", padx=24, pady=(0, 16))

        vc_row = tk.Frame(version_card, bg=t.get("card_bg", "#252536"))
        vc_row.pack(fill="x")
        StyledLabel(vc_row, t, text="Version:", fg=t.get("muted", "#6c7086"),
                    width=12, anchor="w").pack(side="left")
        self._version_entry = StyledEntry(vc_row, t, placeholder="latest",
                                           width=20)
        self._version_entry.pack(side="left", padx=(0, 8))
        self._version_entry.set(self.config.last_version or "")

        latest_btn = StyledButton(vc_row, t, text="Latest", width=70,
                                   command=self._fetch_latest,
                                   bg_key="button_bg", fg_key="button_fg",
                                   hover_key="button_hover")
        latest_btn.pack(side="left", padx=(0, 4))

        self._status_label = StyledLabel(self, t, text="",
                                          fg=t.get("muted", "#6c7086"))
        self._status_label.pack(anchor="w", padx=28, pady=(0, 4))

        self._progress = InstallProgress(self, t)
        self._progress.pack(fill="x", padx=28, pady=(0, 12))

        btn_row = tk.Frame(self, bg=t.get("bg", "#1e1e2e"))
        btn_row.pack(fill="x", padx=24, pady=(0, 8))

        self._play_btn = StyledButton(btn_row, t, text="Play",
                                       width=160, height=42,
                                       bg_key="accent", fg_key="button_fg",
                                       hover_key="accent_hover",
                                       command=self._on_play)
        self._play_btn.pack(side="left")

        self._launch_status = StyledLabel(self, t, text="",
                                           fg=t.get("muted", "#6c7086"))
        self._launch_status.pack(anchor="w", padx=28, pady=(4, 0))

    def _fetch_latest(self):
        try:
            latest = self.launcher.get_latest_version()
            self._version_entry.set(latest)
        except Exception as e:
            self._status_label.configure(text=f"Failed to fetch: {e}",
                                          fg=self.theme.get("error", "#f38ba8"))

    def _on_play(self):
        if self._launching:
            return
        version = self._version_entry.get().strip()
        if not version:
            try:
                version = self.launcher.get_latest_version()
            except Exception as e:
                self._status_label.configure(text=f"Error: {e}",
                                              fg=self.theme.get("error", "#f38ba8"))
                return

        if not self.launcher.is_version_valid(version):
            self._status_label.configure(
                text=f"'{version}' is not a valid Minecraft version.",
                fg=self.theme.get("error", "#f38ba8"))
            return

        self._play_btn.set_enabled(False)
        self._play_btn.set_text("Installing...")
        self._launching = True
        self._status_label.configure(text=f"Installing {version}...",
                                      fg=self.theme.get("fg", "#cdd6f4"))
        self._progress.reset()

        def do_install():
            try:
                def on_progress(status):
                    self.after(0, lambda: self._progress.set_status(status))

                self.launcher.install_version(version, callback={"setStatus": on_progress})
                self.after(0, lambda: self._install_done(version))
            except Exception as e:
                self.after(0, lambda: self._install_failed(str(e)))

        threading.Thread(target=do_install, daemon=True).start()

    def _install_done(self, version):
        self.config.last_version = version
        self.config.save()

        self._progress.set_progress(1.0)
        self._progress.set_status("Ready!")
        self._play_btn.set_text("Launching...")
        self._status_label.configure(text=f"Launching Minecraft {version}...",
                                      fg=self.theme.get("success", "#a6e3a1"))

        def do_launch():
            try:
                proc = self.launcher.launch(version, self.config.username,
                                             ram_mb=self.config.ram_mb)
                self.after(0, lambda: self._launch_started(proc.pid))
                proc.wait()
                self.after(0, lambda: self._launch_ended())
            except FileNotFoundError:
                self.after(0, lambda: self._launch_failed(
                    "Java not found. Install from https://adoptium.net"))
            except Exception as e:
                self.after(0, lambda: self._launch_failed(str(e)))

        threading.Thread(target=do_launch, daemon=True).start()

    def _launch_started(self, pid):
        self._launch_status.configure(
            text=f"Game running (PID {pid})",
            fg=self.theme.get("success", "#a6e3a1"))

    def _launch_ended(self):
        self._launching = False
        self._play_btn.set_text("Play")
        self._play_btn.set_enabled(True)
        self._launch_status.configure(text="Game exited.",
                                       fg=self.theme.get("muted", "#6c7086"))
        self._progress.reset()

    def _install_failed(self, error):
        self._launching = False
        self._play_btn.set_text("Play")
        self._play_btn.set_enabled(True)
        self._status_label.configure(text=f"Install failed: {error}",
                                      fg=self.theme.get("error", "#f38ba8"))
        self._progress.reset()

    def _launch_failed(self, error):
        self._launching = False
        self._play_btn.set_text("Play")
        self._play_btn.set_enabled(True)
        self._launch_status.configure(text=f"Launch failed: {error}",
                                       fg=self.theme.get("error", "#f38ba8"))

    def refresh_data(self):
        if self._username_label:
            self._username_label.configure(text=self.config.username)
        if self._ram_label:
            self._ram_label.configure(text=f"{self.config.ram_mb} MB")
        if self._dir_label:
            self._dir_label.configure(text=self.config.minecraft_directory)

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        for w in self.winfo_children():
            self._update_theme_recursive(w, theme)

    def _update_theme_recursive(self, widget, theme):
        import tkinter as tk
        wtype = type(widget).__name__
        try:
            if hasattr(widget, "update_theme"):
                widget.update_theme(theme)
                return
            if wtype in ("Frame", "Tk", "Toplevel"):
                widget.configure(bg=theme.get("bg", "#1e1e2e"))
            elif wtype == "Label":
                current_fg = widget.cget("fg")
                widget.configure(bg=theme.get("bg", "#1e1e2e"), fg=current_fg,
                                 font=(theme.get("font_family", "Segoe UI"), theme.get("font_size", 11)))
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._update_theme_recursive(child, theme)
