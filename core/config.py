import json
import os
from pathlib import Path

DEFAULT_MINECRAFT_DIR = os.path.join(str(Path.home()), ".nebula")


class Config:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path) if config_path else Path("nebula_config.json")
        self._data = {
            "username": "Nebula",
            "minecraft_directory": DEFAULT_MINECRAFT_DIR,
            "ram_mb": 4096,
            "last_version": "",
            "last_server": "",
            "last_port": 25565,
            "theme": "dark",
        }
        self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    self._data.update(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def __getattr__(self, name):
        if name.startswith("_") or name in ("config_path", "load", "save"):
            return super().__getattribute__(name)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_") or name == "config_path":
            super().__setattr__(name, value)
        elif hasattr(self, "_data"):
            self._data[name] = value
        else:
            super().__setattr__(name, value)
