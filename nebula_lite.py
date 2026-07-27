#!/usr/bin/env python3
"""Nebula-Lite - A lightweight GUI Minecraft launcher."""

import sys

try:
    import tkinter
except ImportError:
    print("Error: tkinter is not installed.")
    print("On Ubuntu/Debian: sudo apt install python3-tk")
    print("On Fedora: sudo dnf install python3-tkinter")
    sys.exit(1)

try:
    import minecraft_launcher_lib
except ImportError:
    print("Error: minecraft-launcher-lib is not installed.")
    print("Run: pip install minecraft-launcher-lib")
    sys.exit(1)


def main():
    from gui.app import NebulaLiteApp
    app = NebulaLiteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
