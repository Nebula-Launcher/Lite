import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master, theme, pages: list, on_select=None,
                 theme_manager=None, on_theme_change=None, **kw):
        kw.setdefault("bg", theme.get("sidebar_bg", "#181825"))
        kw.setdefault("width", 160)
        kw["highlightthickness"] = 0
        super().__init__(master, **kw)
        self.pack_propagate(False)
        self.theme = theme
        self._on_select = on_select
        self._buttons: dict[str, tk.Frame] = {}
        self._active: str = ""
        self._theme_manager = theme_manager
        self._on_theme_change = on_theme_change

        self._logo_frame = tk.Frame(self, bg=theme.get("sidebar_bg", "#181825"))
        self._logo_frame.pack(fill="x", pady=(20, 24))

        self._logo_label = tk.Label(self._logo_frame, text="Nebula",
                                    bg=theme.get("sidebar_bg", "#181825"),
                                    fg=theme.get("accent", "#89b4fa"),
                                    font=(theme.get("font_family", "Segoe UI"),
                                          18, "bold"))
        self._logo_label.pack()

        self._lite_label = tk.Label(self._logo_frame, text="Lite",
                                    bg=theme.get("sidebar_bg", "#181825"),
                                    fg=theme.get("sidebar_fg", "#a6adc8"),
                                    font=(theme.get("font_family", "Segoe UI"), 10))
        self._lite_label.pack()

        self._items_frame = tk.Frame(self, bg=theme.get("sidebar_bg", "#181825"))
        self._items_frame.pack(fill="x", expand=True)

        for page_id, label, icon in pages:
            self._add_item(page_id, label, icon)

        if self._theme_manager:
            self._theme_frame = tk.Frame(self, bg=theme.get("sidebar_bg", "#181825"))
            self._theme_frame.pack(side="bottom", fill="x", padx=8, pady=(0, 12))

            self._theme_btn = tk.Label(
                self._theme_frame,
                text=f"\u263c {self._theme_manager.current_name.title()}",
                bg=theme.get("sidebar_bg", "#181825"),
                fg=theme.get("sidebar_fg", "#a6adc8"),
                font=(theme.get("font_family", "Segoe UI"), 10),
                cursor="hand2",
            )
            self._theme_btn.pack(pady=4)
            self._theme_btn.bind("<Button-1>", lambda e: self._cycle_theme())
            self._theme_btn.bind("<Enter>", lambda e: self._theme_btn.configure(
                fg=theme.get("accent", "#89b4fa")))
            self._theme_btn.bind("<Leave>", lambda e: self._theme_btn.configure(
                fg=theme.get("sidebar_fg", "#a6adc8")))

    def _add_item(self, page_id, label, icon):
        t = self.theme
        item_bg = t.get("sidebar_bg", "#181825")

        container = tk.Frame(self._items_frame, bg=item_bg, cursor="hand2")
        container.pack(fill="x", padx=8, pady=2)

        inner = tk.Frame(container, bg=item_bg)
        inner.pack(fill="x", padx=8, pady=6)

        icon_lbl = tk.Label(inner, text=icon, bg=item_bg,
                            fg=t.get("sidebar_fg", "#a6adc8"),
                            font=(t.get("font_family", "Segoe UI"), 13),
                            width=2)
        icon_lbl.pack(side="left")

        text_lbl = tk.Label(inner, text=label, bg=item_bg,
                            fg=t.get("sidebar_fg", "#a6adc8"),
                            font=(t.get("font_family", "Segoe UI"),
                                  t.get("font_size", 11)))
        text_lbl.pack(side="left", padx=(4, 0))

        for widget in (container, inner, icon_lbl, text_lbl):
            widget.bind("<Button-1>", lambda e, pid=page_id: self._select(pid))
            widget.bind("<Enter>", lambda e, c=container, i=inner, il=icon_lbl,
                        tl=text_lbl: self._on_hover(c, i, il, tl, True))
            widget.bind("<Leave>", lambda e, c=container, i=inner, il=icon_lbl,
                        tl=text_lbl: self._on_hover(c, i, il, tl, False))

        self._buttons[page_id] = {
            "container": container, "inner": inner,
            "icon": icon_lbl, "text": text_lbl,
        }

    def _on_hover(self, container, inner, icon_lbl, text_lbl, entering):
        if self._active and container == self._buttons[self._active]["container"]:
            return
        t = self.theme
        color = t.get("sidebar_fg", "#a6adc8") if entering else t.get("sidebar_bg", "#181825")
        if entering:
            color = t.get("button_hover", "#45475a")
        for w in (container, inner):
            w.configure(bg=color)
        icon_lbl.configure(bg=color)
        text_lbl.configure(bg=color, fg=t.get("sidebar_fg", "#a6adc8") if entering
                           else t.get("sidebar_fg", "#a6adc8"))

    def _select(self, page_id):
        if self._active:
            self._deselect(self._active)
        self._active = page_id
        t = self.theme
        btn = self._buttons[page_id]
        active_bg = t.get("sidebar_bg", "#181825")
        for w in (btn["container"], btn["inner"]):
            w.configure(bg=active_bg)
        btn["icon"].configure(bg=active_bg, fg=t.get("sidebar_active", "#89b4fa"))
        btn["text"].configure(bg=active_bg, fg=t.get("sidebar_active", "#89b4fa"))

        if self._on_select:
            self._on_select(page_id)

    def _deselect(self, page_id):
        t = self.theme
        btn = self._buttons[page_id]
        normal_bg = t.get("sidebar_bg", "#181825")
        for w in (btn["container"], btn["inner"]):
            w.configure(bg=normal_bg)
        btn["icon"].configure(bg=normal_bg, fg=t.get("sidebar_fg", "#a6adc8"))
        btn["text"].configure(bg=normal_bg, fg=t.get("sidebar_fg", "#a6adc8"))

    def select_page(self, page_id):
        self._select(page_id)

    def _cycle_theme(self):
        if not self._theme_manager:
            return
        names = self._theme_manager.get_theme_names()
        current = self._theme_manager.current_name
        idx = names.index(current) if current in names else 0
        next_name = names[(idx + 1) % len(names)]
        self._theme_manager.set_theme(next_name)
        self._theme_btn.configure(text=f"\u263c {next_name.title()}")
        if self._on_theme_change:
            self._on_theme_change(next_name)

    def update_theme(self, theme):
        self.theme = theme
        t = theme
        self.configure(bg=t.get("sidebar_bg", "#181825"))
        self._logo_frame.configure(bg=t.get("sidebar_bg", "#181825"))
        self._logo_label.configure(bg=t.get("sidebar_bg", "#181825"),
                                   fg=t.get("accent", "#89b4fa"),
                                   font=(t.get("font_family", "Segoe UI"), 18, "bold"))
        self._lite_label.configure(bg=t.get("sidebar_bg", "#181825"),
                                   fg=t.get("sidebar_fg", "#a6adc8"),
                                   font=(t.get("font_family", "Segoe UI"), 10))
        self._items_frame.configure(bg=t.get("sidebar_bg", "#181825"))
        if self._theme_manager and hasattr(self, "_theme_frame"):
            self._theme_frame.configure(bg=t.get("sidebar_bg", "#181825"))
            self._theme_btn.configure(
                bg=t.get("sidebar_bg", "#181825"),
                fg=t.get("sidebar_fg", "#a6adc8"),
                text=f"\u263c {self._theme_manager.current_name.title()}",
                font=(t.get("font_family", "Segoe UI"), 10))
        for page_id, btn in self._buttons.items():
            if page_id == self._active:
                self._select(page_id)
            else:
                self._deselect(page_id)
