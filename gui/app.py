import tkinter as tk

from core.config import Config
from core.launcher import NebulaLauncher
from gui.themes.manager import ThemeManager
from gui.widgets.sidebar import Sidebar
from gui.pages.home import HomePage
from gui.pages.settings import SettingsPage
from gui.pages.versions import VersionsPage
from gui.pages.about import AboutPage


class NebulaLiteApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config = Config()
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme(self.config.theme)
        self.launcher = NebulaLauncher(self.config)

        self.title("Nebula-Lite")
        self.geometry("800x520")
        self.minsize(720, 440)
        self.configure(bg=self.theme_manager.current.get("bg", "#1e1e2e"))

        t = self.theme_manager.current

        self._sidebar = Sidebar(self, t, [
            ("home", "Home", "\u25b6"),
            ("settings", "Settings", "\u2699"),
            ("versions", "Versions", "\u2630"),
            ("about", "About", "\u2139"),
        ], on_select=self._on_page_select,
           theme_manager=self.theme_manager,
           on_theme_change=self._on_theme_change)

        self._sidebar.pack(side="left", fill="y")

        self._content = tk.Frame(self, bg=t.get("bg", "#1e1e2e"),
                                  highlightthickness=0)
        self._content.pack(side="left", fill="both", expand=True)

        self._pages: dict[str, tk.Frame] = {}
        self._current_page: str = ""

        self._create_pages()
        self._show_page("home")

    def _create_pages(self):
        t = self.theme_manager.current
        self._pages["home"] = HomePage(self._content, t,
                                        self.config, self.launcher)
        self._pages["settings"] = SettingsPage(self._content, t,
                                                self.config, self.launcher,
                                                theme_manager=self.theme_manager,
                                                on_theme_change=self._on_theme_change)
        self._pages["versions"] = VersionsPage(self._content, t,
                                                self.config, self.launcher)
        self._pages["about"] = AboutPage(self._content, t)

    def _on_page_select(self, page_id):
        self._show_page(page_id)

    def _show_page(self, page_id):
        if self._current_page and self._current_page in self._pages:
            self._pages[self._current_page].pack_forget()

        page = self._pages.get(page_id)
        if page:
            if hasattr(page, "refresh_data"):
                page.refresh_data()
            page.pack(fill="both", expand=True)
            self._current_page = page_id

    def _on_theme_change(self, theme_name):
        t = self.theme_manager.current
        self.config.theme = theme_name
        self.config.save()
        self.configure(bg=t.get("bg", "#1e1e2e"))
        self._sidebar.update_theme(t)
        self._content.configure(bg=t.get("bg", "#1e1e2e"))

        for page_id, page in self._pages.items():
            if hasattr(page, "update_theme"):
                page.update_theme(t)

        self._show_page(self._current_page)
