# Nebula Lite

> A lightweight, open-source Minecraft launcher with a modern graphical interface.

## ✨ Features

- 🖥️ Clean graphical interface
- 🚀 Lightweight and fast
- 🎮 Offline (cracked) authentication
- 📥 Automatic Minecraft installation
- 📚 Browse and launch any Minecraft version
- 💾 Custom Minecraft directory support
- 🧠 Configurable RAM allocation
- 🌐 Direct server connection
- 🐧 Linux, Windows, and macOS support
- ❤️ Open Source

## 📦 Requirements

- Python **3.11+**
- Java **17+** (or the version required by your Minecraft version)
- `minecraft-launcher-lib`
- `tkinter`

Install the required Python library:

```bash
pip install minecraft-launcher-lib
```

### Linux

Install Tkinter if it isn't already installed.

**Debian / Ubuntu**

```bash
sudo apt install python3-tk
```

**Fedora**

```bash
sudo dnf install python3-tkinter
```

## 🚀 Running

```bash
python nebula.py
```

## 📁 Project Structure

```text
nebula/
├── nebula.py
├── gui/
│   ├── app.py
│   ├── pages/
│   ├── widgets/
│   └── assets/
└── README.md
```

## 🔒 Authentication

Currently supported:

- ✅ Offline Authentication

Planned support:

- ⏳ Ely.by Authentication

Microsoft authentication is intentionally **not** supported.

## 🎯 Goals

Nebula is built around a few simple ideas:

- Lightweight
- Fast startup
- Easy to contribute to
- Open Source
- Privacy-friendly
- Cross-platform
- Modern user interface

## 🛣️ Roadmap

- GUI improvements
- Ely.by login
- Modpack support
- Fabric & Forge installer
- Multiple accounts
- Themes
- Automatic updates

## 🤝 Contributing

Contributions are always welcome. Feel free to open issues or submit pull requests.

## 📜 License

Released under the **MIT License**.

## 🌌 Nebula Family

| Launcher | Description |
|----------|-------------|
| **Nebula Nano** | Ultra-lightweight terminal launcher |
| **Nebula** | Modern graphical launcher *(Alpha)* |
| **Nebula Lite** | Lightweight GUI launcher|

---

Built with Python, Tkinter, and a stubborn refusal to install seventeen Electron processes just to click a "Play" button.
