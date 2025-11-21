# Autolauncher v0.1.2-alpha Release Notes

**First Public Alpha Release** - Modern Task Scheduling with Auto-Updates

© 2025 4never Company. All rights reserved.

---

## 🎉 What's New in v0.1.2-alpha

### 🎨 Modern Visual Design
- **Rounded Corner Icons**: All icons and logos now feature modern 15% rounded corners
- **Professional Branding**: Custom Autolauncher icons throughout Windows
  - Window title bar and taskbar
  - System tray notification area
  - Task Manager displays "Autolauncher.exe"
- **Transparent Assets**: PNG format with full alpha transparency for perfect integration

### 🔄 Automatic Update System
- **One-Click Updates**: Download and install updates directly from within the app
- **Progress Tracking**: Real-time download progress with MB counter
- **Auto-Restart**: Application automatically restarts after update installation
- **Smart Detection**: Automatically detects if running as executable or Python script
- **Semantic Versioning**: Proper version comparison for reliable updates

### 📦 Standalone Executable
- **No Python Required**: Runs on any Windows 10/11 PC without dependencies
- **Single File**: Everything bundled into one 62MB executable
- **Self-Contained**: All icons, assets, and configurations included
- **Professional**: Proper Windows integration with custom icons

### 🛠️ Core Features
- Task scheduling with countdown timers
- One-time and recurring schedules (hourly, daily, weekly)
- System tray integration with minimize to tray
- Light and dark theme support with auto-enforcement
- Fluent Design UI with modern aesthetics

---

## 📥 Installation

### Option 1: Standalone Executable (Recommended)
1. Download `Autolauncher.exe`
2. Run it - no installation needed!
3. (Optional) Create a desktop shortcut

### Option 2: Run from Source
1. Download source code
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python autolauncher.py`

---

## 🚀 What's Included

### Application Features
✅ Schedule programs to launch automatically
✅ Recurring schedules (hourly/daily/weekly)
✅ Countdown timers showing time until execution
✅ Run tasks immediately with "Run Now"
✅ Enable/disable tasks without deletion
✅ System tray integration
✅ Light/Dark theme toggle
✅ Update checking and auto-installation

### Technical Features
✅ Windows App User Model ID for proper branding
✅ Multi-resolution icon support (16x16 to 256x256)
✅ Alpha-transparent PNG icons
✅ Threaded update downloads (non-blocking UI)
✅ Automatic executable replacement and restart
✅ Comprehensive error handling and logging

---

## 🎯 System Requirements

- **OS**: Windows 10 or Windows 11
- **RAM**: 100MB minimum
- **Disk Space**: 100MB
- **Internet**: Required for update checks only (optional)

---

## 📸 Features Showcase

### Modern Rounded Icons
All branding assets feature contemporary rounded corners:
- Icons: 15% corner radius for friendly, approachable feel
- Logos: 10% corner radius for professional, subtle elegance
- Full transparency support for seamless Windows integration

### Auto-Update System
- Check for updates from Settings → About
- One-click download and installation
- Progress: "Downloaded 45.2 MB / 62.0 MB (73%)"
- Automatic restart after installation

### Professional Windows Integration
- Custom icon in taskbar (not Python logo)
- Proper app name in Task Manager
- System tray icon matches application theme
- Native Windows UI with Fluent Design

---

## 🔧 Building from Source

Want to build your own executable?

```powershell
# Install dependencies
pip install -r requirements.txt

# Build the executable
python build_exe.py

# Output: dist\Autolauncher.exe
```

See `BUILD_GUIDE.md` for detailed instructions.

---

## 📚 Documentation

- **BUILD_GUIDE.md**: How to build the executable
- **UPDATE_SYSTEM.md**: Auto-update system documentation
- **autolauncher_tutorial.md**: User guide and tutorial
- **README.md**: Project overview

---

## ⚠️ Known Issues (Alpha)

This is an **alpha release**. Please report issues on GitHub!

Current known limitations:
- Update system requires manual GitHub release creation
- No automatic background update checks (manual only)
- Windows-only (no macOS/Linux support yet)

---

## 🐛 Reporting Issues

Found a bug or have a feature request?

1. Go to [GitHub Issues](https://github.com/Code4neverCompany/Code4never-AutoLauncher_AlphaVersion/issues)
2. Click "New Issue"
3. Describe the problem or suggestion

Include:
- Your Windows version
- Steps to reproduce
- Expected vs actual behavior
- Screenshot if applicable

---

## 🔄 Updating

### If You Downloaded the Executable:
1. Open Autolauncher
2. Go to Settings → About
3. Click "Check for Updates"
4. Click "Download & Install" if update available
5. App will restart automatically with new version

### If Running from Source:
```powershell
git pull origin main
pip install -r requirements.txt
python autolauncher.py
```

---

## 💡 Tips & Tricks

1. **Minimize to Tray**: Close button minimizes to system tray instead of quitting
2. **Theme Switching**: Use the "Toggle Theme" button in the toolbar
3. **Quick Run**: Select a task and click "Run Now" to execute immediately
4. **Task Management**: Tasks persist even when app is closed

---

## 🙏 Credits

**Developed by**: Code4never Company  
**Framework**: PySide6 (Qt6)  
**UI Library**: qfluentwidgets (Fluent Design)  
**Icons**: Custom Autolauncher branding  
**Build Tool**: PyInstaller

---

## 📄 License

© 2025 4never Company. All rights reserved.

See EULA in workspace for full terms and conditions.

---

## 🔮 Roadmap

Future enhancements planned:
- [ ] Delta updates (download only changes)
- [ ] Automatic background update checks
- [ ] Task categories and grouping
- [ ] Task import/export
- [ ] Command-line arguments support
- [ ] Portable mode (no registry writes)
- [ ] Multi-language support

---

## 📞 Support

Need help?
- 📖 Read the documentation in `autolauncher_tutorial.md`
- 🐛 Report bugs on GitHub Issues
- 💬 Discussion: GitHub Discussions
- 📧 Email: [Your support email]

---

**Thank you for trying Autolauncher Alpha!**

Your feedback helps make this app better for everyone. 🚀

---

**Release Date**: November 21, 2025  
**Version**: 0.1.2-alpha  
**Build**: Alpha Release 1
