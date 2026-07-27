import threading
import tkinter as tk

from gui.widgets.styled import StyledFrame, StyledCard, StyledLabel, StyledHeading, StyledButton


class VersionsPage(tk.Frame):
    def __init__(self, master, theme, config, launcher, **kw):
        kw["bg"] = theme.get("bg", "#1e1e2e")
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.theme = theme
        self.config = config
        self.launcher = launcher

        self._build_ui()

    def _build_ui(self):
        t = self.theme
        for w in self.winfo_children():
            w.destroy()

        tk.Frame(self, bg=t.get("bg", "#1e1e2e"), height=24).pack()

        StyledHeading(self, t, "Versions", size_key="title_size").pack(anchor="w", padx=28)
        StyledLabel(self, t, text="Browse and manage Minecraft versions",
                     fg=t.get("muted", "#6c7086")).pack(anchor="w", padx=28, pady=(2, 16))

        top_row = tk.Frame(self, bg=t.get("bg", "#1e1e2e"))
        top_row.pack(fill="x", padx=24, pady=(0, 12))

        self._refresh_btn = StyledButton(top_row, t, text="Refresh", width=90,
                                          command=self._refresh,
                                          bg_key="button_bg", fg_key="button_fg",
                                          hover_key="button_hover")
        self._refresh_btn.pack(side="left")

        self._status = StyledLabel(top_row, t, text="",
                                    fg=t.get("muted", "#6c7086"))
        self._status.pack(side="left", padx=(12, 0))

        panes = tk.Frame(self, bg=t.get("bg", "#1e1e2e"))
        panes.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        left = StyledCard(panes, t)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        StyledLabel(left, t, text="Available Releases",
                     fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 8))

        left_scroll = tk.Frame(left, bg=t.get("card_bg", "#252536"))
        left_scroll.pack(fill="both", expand=True)

        self._releases_list = tk.Text(left_scroll,
                                       bg=t.get("card_bg", "#252536"),
                                       fg=t.get("fg", "#cdd6f4"),
                                       font=(t.get("font_family", "Segoe UI"),
                                             t.get("font_size", 11)),
                                       relief="flat", bd=0,
                                       highlightthickness=0,
                                       state="disabled",
                                       cursor="arrow",
                                       padx=8, pady=4)
        self._releases_scrollbar = tk.Scrollbar(left_scroll,
                                                 command=self._releases_list.yview,
                                                 bg=t.get("card_bg", "#252536"),
                                                 troughcolor=t.get("card_bg", "#252536"),
                                                 bd=0, highlightthickness=0)
        self._releases_list.configure(yscrollcommand=self._releases_scrollbar.set)
        self._releases_scrollbar.pack(side="right", fill="y")
        self._releases_list.pack(side="left", fill="both", expand=True)

        right = StyledCard(panes, t)
        right.pack(side="right", fill="both", expand=True, padx=(6, 0))

        StyledLabel(right, t, text="Installed Versions",
                     fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 8))

        right_scroll = tk.Frame(right, bg=t.get("card_bg", "#252536"))
        right_scroll.pack(fill="both", expand=True)

        self._installed_list = tk.Text(right_scroll,
                                        bg=t.get("card_bg", "#252536"),
                                        fg=t.get("fg", "#cdd6f4"),
                                        font=(t.get("font_family", "Segoe UI"),
                                              t.get("font_size", 11)),
                                        relief="flat", bd=0,
                                        highlightthickness=0,
                                        state="disabled",
                                        cursor="arrow",
                                        padx=8, pady=4)
        self._installed_scrollbar = tk.Scrollbar(right_scroll,
                                                  command=self._installed_list.yview,
                                                  bg=t.get("card_bg", "#252536"),
                                                  troughcolor=t.get("card_bg", "#252536"),
                                                  bd=0, highlightthickness=0)
        self._installed_list.configure(yscrollcommand=self._installed_scrollbar.set)
        self._installed_scrollbar.pack(side="right", fill="y")
        self._installed_list.pack(side="left", fill="both", expand=True)

    def _set_text_widget(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _refresh(self):
        self._refresh_btn.set_enabled(False)
        self._refresh_btn.set_text("Loading...")
        self._status.configure(text="Fetching versions...")

        def do_load():
            try:
                all_versions = self.launcher.get_all_versions()
                releases = [v for v in all_versions if v["type"] == "release"]
                installed = self.launcher.get_installed_versions()

                release_text = "\n".join(f"  {v['id']}" for v in releases[-30:])
                if len(releases) > 30:
                    release_text += f"\n  ... and {len(releases) - 30} more"
                if not release_text.strip():
                    release_text = "  No releases found"

                installed_text = "\n".join(f"  {v['id']}  ({v['type']})" for v in installed)
                if not installed_text.strip():
                    installed_text = "  No versions installed"

                self.after(0, lambda: self._update_lists(release_text, installed_text,
                                                          len(releases), len(installed)))
            except Exception as e:
                self.after(0, lambda: self._load_failed(str(e)))

        threading.Thread(target=do_load, daemon=True).start()

    def _update_lists(self, release_text, installed_text, release_count, installed_count):
        self._set_text_widget(self._releases_list, release_text)
        self._set_text_widget(self._installed_list, installed_text)
        self._status.configure(
            text=f"{release_count} releases, {installed_count} installed")
        self._refresh_btn.set_text("Refresh")
        self._refresh_btn.set_enabled(True)

    def _load_failed(self, error):
        self._status.configure(text=f"Failed: {error}",
                                fg=self.theme.get("error", "#f38ba8"))
        self._refresh_btn.set_text("Refresh")
        self._refresh_btn.set_enabled(True)

    def refresh_data(self):
        pass

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        self._build_ui()
