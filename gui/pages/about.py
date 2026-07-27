import tkinter as tk

from gui.widgets.styled import StyledFrame, StyledCard, StyledLabel, StyledHeading


VERSION = "1.0.0"
BANNER_TEXT = "N E B U L A"


class AboutPage(tk.Frame):
    def __init__(self, master, theme, **kw):
        kw["bg"] = theme.get("bg", "#1e1e2e")
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.theme = theme

        self._build_ui()

    def _build_ui(self):
        t = self.theme
        for w in self.winfo_children():
            w.destroy()

        tk.Frame(self, bg=t.get("bg", "#1e1e2e"), height=24).pack()

        StyledHeading(self, t, "About", size_key="title_size").pack(anchor="w", padx=28)
        StyledLabel(self, t, text="About Nebula-Lite",
                     fg=t.get("muted", "#6c7086")).pack(anchor="w", padx=28, pady=(2, 24))

        card = StyledCard(self, t)
        card.pack(fill="x", padx=24, pady=(0, 16))

        StyledLabel(card, t, text=BANNER_TEXT,
                     fg=t.get("accent", "#89b4fa"),
                     font=(t.get("font_family", "Segoe UI"), 22, "bold")).pack(pady=(12, 2))

        StyledLabel(card, t, text="Lite",
                     fg=t.get("muted", "#6c7086"),
                     font=(t.get("font_family", "Segoe UI"), 11)).pack(pady=(0, 12))

        StyledLabel(card, t, text=f"Version {VERSION}",
                     fg=t.get("fg", "#cdd6f4")).pack(pady=(0, 4))

        StyledLabel(card, t, text="A lightweight cracked Minecraft launcher",
                     fg=t.get("muted", "#6c7086")).pack(pady=(0, 12))

        card2 = StyledCard(self, t)
        card2.pack(fill="x", padx=24, pady=(0, 16))

        StyledLabel(card2, t, text="Features",
                     fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 8))

        features = [
            "Install and launch any Minecraft version",
            "Offline / cracked mode authentication",
            "Configurable RAM and game directory",
            "Server auto-connect on launch",
            "Themeable GUI with custom JSON themes",
        ]
        for feat in features:
            StyledLabel(card2, t, text=f"  {feat}",
                         fg=t.get("fg", "#cdd6f4")).pack(anchor="w", pady=1)

        card3 = StyledCard(self, t)
        card3.pack(fill="x", padx=24, pady=(0, 16))

        StyledLabel(card3, t, text="Credits",
                     fg=t.get("accent", "#89b4fa")).pack(anchor="w", pady=(0, 8))
        StyledLabel(card3, t, text="  Powered by minecraft-launcher-lib",
                     fg=t.get("fg", "#cdd6f4")).pack(anchor="w", pady=1)
        StyledLabel(card3, t, text="  Built with Python + tkinter",
                     fg=t.get("fg", "#cdd6f4")).pack(anchor="w", pady=1)

    def refresh_data(self):
        pass

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        self._build_ui()
