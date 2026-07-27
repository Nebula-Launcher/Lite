import tkinter as tk


class InstallProgress(tk.Frame):
    def __init__(self, master, theme, **kw):
        kw.setdefault("bg", theme.get("bg", "#1e1e2e"))
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.theme = theme

        self._status_label = tk.Label(self, text="",
                                       bg=theme.get("bg", "#1e1e2e"),
                                       fg=theme.get("fg", "#cdd6f4"),
                                       font=(theme.get("font_family", "Segoe UI"), theme.get("font_size", 11)),
                                       anchor="w")
        self._status_label.pack(fill="x", pady=(0, 6))

        self._bar_bg = tk.Frame(self, height=8,
                                 bg=theme.get("card_border", "#313244"),
                                 highlightthickness=0)
        self._bar_bg.pack(fill="x")
        self._bar_bg.pack_propagate(False)

        self._bar_fill = tk.Frame(self._bar_bg, height=8,
                                   bg=theme.get("accent", "#89b4fa"),
                                   highlightthickness=0)
        self._bar_fill.place(x=0, y=0, relwidth=0, relheight=1.0)

        self._percent_label = tk.Label(self, text="0%",
                                        bg=theme.get("bg", "#1e1e2e"),
                                        fg=theme.get("muted", "#6c7086"),
                                        font=(theme.get("font_family", "Segoe UI"), theme.get("font_size", 11)),
                                        anchor="e")
        self._percent_label.pack(fill="x", pady=(6, 0))

    def set_status(self, text):
        self._status_label.configure(text=text)

    def set_progress(self, value: float):
        pct = max(0.0, min(1.0, value))
        self._bar_fill.place(x=0, y=0, relwidth=pct, relheight=1.0)
        self._percent_label.configure(text=f"{int(pct * 100)}%")

    def reset(self):
        self._status_label.configure(text="")
        self._bar_fill.place(x=0, y=0, relwidth=0, relheight=1.0)
        self._percent_label.configure(text="0%")

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        self._status_label.configure(bg=theme.get("bg", "#1e1e2e"),
                                     fg=theme.get("fg", "#cdd6f4"),
                                     font=(theme.get("font_family", "Segoe UI"), theme.get("font_size", 11)))
        self._bar_bg.configure(bg=theme.get("card_border", "#313244"))
        self._bar_fill.configure(bg=theme.get("accent", "#89b4fa"))
        self._percent_label.configure(bg=theme.get("bg", "#1e1e2e"),
                                      fg=theme.get("muted", "#6c7086"),
                                      font=(theme.get("font_family", "Segoe UI"), theme.get("font_size", 11)))
