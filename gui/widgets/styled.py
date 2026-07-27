import tkinter as tk


class StyledFrame(tk.Frame):
    def __init__(self, master, theme, **kw):
        kw.setdefault("bg", theme.get("bg", "#1e1e2e"))
        kw.setdefault("highlightthickness", 0)
        super().__init__(master, **kw)
        self.theme = theme


class StyledCard(tk.Frame):
    def __init__(self, master, theme, **kw):
        kw.setdefault("bg", theme.get("card_bg", "#252536"))
        kw.setdefault("padx", 16)
        kw.setdefault("pady", 12)
        super().__init__(master, **kw)
        self.theme = theme
        self.configure(highlightbackground=theme.get("card_border", "#313244"),
                       highlightthickness=1)


class StyledLabel(tk.Label):
    def __init__(self, master, theme, **kw):
        kw.setdefault("bg", theme.get("bg", "#1e1e2e"))
        kw.setdefault("fg", theme.get("fg", "#cdd6f4"))
        kw.setdefault("font", (theme.get("font_family", "Segoe UI"),
                                theme.get("font_size", 11)))
        super().__init__(master, **kw)
        self.theme = theme


class StyledHeading(tk.Label):
    def __init__(self, master, theme, text="", size_key="heading_size", **kw):
        kw.setdefault("bg", theme.get("bg", "#1e1e2e"))
        kw.setdefault("fg", theme.get("fg", "#cdd6f4"))
        kw.setdefault("font", (theme.get("font_family", "Segoe UI"),
                                theme.get(size_key, 16)))
        kw.setdefault("text", text)
        super().__init__(master, **kw)
        self.theme = theme


class StyledButton(tk.Canvas):
    def __init__(self, master, theme, text="", command=None, width=140, height=36,
                 bg_key="button_bg", fg_key="button_fg", hover_key="button_hover",
                 font_key="font_size", **kw):
        self._bg_key = bg_key
        self._fg_key = fg_key
        self._hover_key = hover_key
        self._command = command
        self._text = text
        self._hovered = False
        self._enabled = True

        bg = theme.get(bg_key, "#313244")
        fg = theme.get(fg_key, "#cdd6f4")

        super().__init__(master, width=width, height=height,
                         bg=theme.get("bg", "#1e1e2e"),
                         highlightthickness=0, **kw)
        self.theme = theme
        self._rect = self.create_rectangle(0, 0, width, height,
                                           fill=bg, outline="", tags="bg")
        self._label = self.create_text(width // 2, height // 2, text=text,
                                       fill=fg, font=(theme.get("font_family", "Segoe UI"),
                                                      theme.get(font_key, 11)))

        font_family = theme.get("font_family", "Segoe UI")
        font_size = theme.get(font_key, 11)
        self.itemconfig(self._label, font=(font_family, font_size))

        self.tag_bind("bg", "<Enter>", self._on_enter)
        self.tag_bind("bg", "<Leave>", self._on_leave)
        self.tag_bind(self._label, "<Enter>", self._on_enter)
        self.tag_bind(self._label, "<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.tag_bind("bg", "<Button-1>", self._on_click)
        self.tag_bind(self._label, "<Button-1>", self._on_click)
        self.configure(cursor="hand2")

    def _on_enter(self, event=None):
        self._hovered = True
        hover_bg = self.theme.get(self._hover_key, "#45475a")
        self.itemconfig(self._rect, fill=hover_bg)

    def _on_leave(self, event=None):
        self._hovered = False
        normal_bg = self.theme.get(self._bg_key, "#313244")
        self.itemconfig(self._rect, fill=normal_bg)

    def _on_click(self, event=None):
        if self._enabled and self._command:
            self._command()

    def set_text(self, text):
        self._text = text
        self.itemconfig(self._label, text=text)

    def set_enabled(self, enabled: bool):
        self._enabled = enabled
        if enabled:
            self.configure(cursor="hand2")
            self.itemconfig(self._label, fill=self.theme.get(self._fg_key, "#cdd6f4"))
        else:
            self.configure(cursor="")
            self.itemconfig(self._label, fill=self.theme.get("muted", "#6c7086"))

    def update_theme(self, theme):
        self.theme = theme
        bg = theme.get(self._bg_key, "#313244")
        fg = theme.get(self._fg_key, "#cdd6f4")
        font_family = theme.get("font_family", "Segoe UI")
        font_size = theme.get("font_size", 11)
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        self.itemconfig(self._rect, fill=bg)
        self.itemconfig(self._label, fill=fg, font=(font_family, font_size))


class StyledEntry(tk.Frame):
    def __init__(self, master, theme, placeholder="", width=28, **kw):
        super().__init__(master, bg=theme.get("bg", "#1e1e2e"),
                         highlightthickness=0)
        self.theme = theme
        self._placeholder = placeholder

        self.entry = tk.Entry(self,
                              bg=theme.get("entry_bg", "#313244"),
                              fg=theme.get("entry_fg", "#cdd6f4"),
                              insertbackground=theme.get("fg", "#cdd6f4"),
                              font=(theme.get("font_family", "Segoe UI"),
                                    theme.get("font_size", 11)),
                              relief="flat", bd=0,
                              highlightbackground=theme.get("card_border", "#313244"),
                              highlightthickness=1,
                              width=width, **kw)
        self.entry.pack(fill="x", expand=True, ipady=6, padx=1, pady=1)

        if placeholder:
            self._show_placeholder()
            self.entry.bind("<FocusIn>", self._on_focus_in)
            self.entry.bind("<FocusOut>", self._on_focus_out)

    def _show_placeholder(self):
        if not self.entry.get():
            self.entry.insert(0, self._placeholder)
            self.entry.configure(fg=self.theme.get("muted", "#6c7086"))

    def _on_focus_in(self, event=None):
        if self.entry.get() == self._placeholder:
            self.entry.delete(0, "end")
            self.entry.configure(fg=self.theme.get("entry_fg", "#cdd6f4"))

    def _on_focus_out(self, event=None):
        self._show_placeholder()

    def get(self):
        val = self.entry.get()
        if val == self._placeholder:
            return ""
        return val

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.entry.configure(fg=self.theme.get("entry_fg", "#cdd6f4"))

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme.get("bg", "#1e1e2e"))
        current = self.entry.get()
        is_placeholder = current == self._placeholder
        self.entry.configure(
            bg=theme.get("entry_bg", "#313244"),
            fg=theme.get("muted" if is_placeholder else "entry_fg", "#6c7086"),
            insertbackground=theme.get("fg", "#cdd6f4"),
            highlightbackground=theme.get("card_border", "#313244"),
        )


class StyledScrollbar(tk.Canvas):
    def __init__(self, master, theme, **kw):
        super().__init__(master, width=6, bg=theme.get("bg", "#1e1e2e"),
                         highlightthickness=0, **kw)
        self.theme = theme
