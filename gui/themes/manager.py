import json
import os
from pathlib import Path

BUILTIN_DIR = Path(__file__).parent
USER_DIR = Path.home() / ".nebula" / "themes"


class ThemeManager:
    def __init__(self):
        self._themes: dict[str, dict] = {}
        self._current: dict = {}
        self._current_name: str = "dark"
        self._load_builtins()
        self._load_user_themes()

    def _load_builtins(self):
        for name in ("dark", "light"):
            path = BUILTIN_DIR / f"{name}.json"
            if path.exists():
                self._themes[name] = json.loads(path.read_text())

    def _load_user_themes(self):
        if USER_DIR.exists():
            for f in USER_DIR.glob("*.json"):
                try:
                    self._themes[f.stem] = json.loads(f.read_text())
                except (json.JSONDecodeError, OSError):
                    pass

    def get_theme_names(self) -> list[str]:
        return list(self._themes.keys())

    def get_theme(self, name: str) -> dict:
        return self._themes.get(name, self._themes.get("dark", {}))

    @property
    def current(self) -> dict:
        return self._current

    @property
    def current_name(self) -> str:
        return self._current_name

    def set_theme(self, name: str):
        if name in self._themes:
            self._current = self._themes[name]
            self._current_name = name

    def get_color(self, key: str) -> str:
        return self._current.get(key, "#ffffff")

    def get_font(self, key: str = "font_size") -> tuple:
        family = self._current.get("font_family", "Segoe UI")
        size = self._current.get(key, 11)
        return (family, size)

    def apply_theme(self, widget):
        self._apply_recursive(widget)

    def _apply_recursive(self, widget):
        import tkinter as tk

        t = self._current
        wtype = type(widget).__name__

        try:
            if wtype in ("Frame", "Tk", "Toplevel"):
                widget.configure(bg=t.get("bg", "#1e1e2e"))
            elif wtype == "Label":
                widget.configure(bg=t.get("bg", "#1e1e2e"), fg=t.get("fg", "#cdd6f4"),
                                 font=self.get_font())
            elif wtype == "Button":
                pass
            elif wtype == "Entry":
                widget.configure(bg=t.get("entry_bg", "#313244"),
                                 fg=t.get("entry_fg", "#cdd6f4"),
                                 insertbackground=t.get("fg", "#cdd6f4"),
                                 font=self.get_font(),
                                 relief="flat", bd=0,
                                 highlightbackground=t.get("card_border", "#313244"),
                                 highlightthickness=1)
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self._apply_recursive(child)

    def refresh_all(self, root):
        self._apply_recursive(root)
