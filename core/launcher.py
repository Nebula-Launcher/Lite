import subprocess
import sys

import minecraft_launcher_lib

from core.auth import get_offline_options
from core.config import Config

VERSION = "lite"


class NebulaLauncher:
    def __init__(self, config: Config):
        self.config = config
        self.mc_dir = config.minecraft_directory

    def get_latest_version(self) -> str:
        return minecraft_launcher_lib.utils.get_latest_version()["release"]

    def get_all_versions(self) -> list:
        return minecraft_launcher_lib.utils.get_available_versions(self.mc_dir)

    def get_installed_versions(self) -> list:
        return minecraft_launcher_lib.utils.get_installed_versions(self.mc_dir)

    def is_version_valid(self, version: str) -> bool:
        return minecraft_launcher_lib.utils.is_version_valid(version, self.mc_dir)

    def install_version(self, version: str, callback=None):
        minecraft_launcher_lib.install.install_minecraft_version(
            version, self.mc_dir, callback=callback
        )

    def launch(self, version: str, username: str, ram_mb=None, extra_args=None):
        options = get_offline_options(username)
        options["launcherName"] = "NebulaLite"
        options["launcherVersion"] = VERSION
        if ram_mb:
            options["jvmArguments"] = [f"-Xmx{ram_mb}M", f"-Xms{ram_mb}M"]
        if extra_args:
            options.setdefault("jvmArguments", []).extend(extra_args)
        command = minecraft_launcher_lib.command.get_minecraft_command(
            version, self.mc_dir, options
        )
        kwargs = {"cwd": self.mc_dir}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return subprocess.Popen(command, **kwargs)
