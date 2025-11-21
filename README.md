# Autolauncher

A modern desktop application for scheduling and automatically executing programs at specific times.

Built with **PySide6** and **PySide6-Fluent-Widgets** for a beautiful Microsoft Fluent Design experience.

## Features

- ✨ **Modern Fluent Design UI** - Beautiful, responsive interface
- 🌓 **Theme Switching** - Toggle between Light and Dark modes
- ⏱️ **Countdown Timer** - Real-time display showing when tasks will execute
- 📋 **Task Management** - Easily add, edit, and delete scheduled tasks
- 🔔 **System Tray** - Runs in background, minimizes to tray
- 💾 **Data Persistence** - Tasks and settings saved automatically
- 📊 **Debug Logging** - Comprehensive logging for development (optional)

## Quick Start

### 1. Install Dependencies

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
python autolauncher.py
```

### 3. Add Your First Task

1. Click **"Add Task"** button
2. Enter a task name
3. Browse for an executable file
4. Set the schedule date and time
5. Click **"Add Task"**
6. Watch the countdown timer!

## Project Structure

```
Autolauncher/
├── autolauncher.py          # Main application window
├── task_dialog.py           # Task configuration dialog
├── task_manager.py          # Data persistence (JSON)
├── scheduler.py             # Task scheduling (APScheduler)
├── logger.py                # Logging configuration
├── config.py                # Application settings
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── autolauncher_tutorial.md # Complete tutorial
└── README.md               # This file
```

## Development Mode

Enable debug logging during development:

```powershell
$env:DEBUG=1
python autolauncher.py
```

This creates detailed logs in `logs/autolauncher.log`.

## Documentation

See [autolauncher_tutorial.md](autolauncher_tutorial.md) for the complete, step-by-step tutorial covering:

- Environment setup with exact commands
- Architecture overview and design decisions
- Detailed implementation guide for each module
- Icon integration instructions
- Debugging tips and troubleshooting
- Production deployment guidelines

## Requirements

- Python 3.9+
- PySide6 >= 6.5.0
- PySide6-Fluent-Widgets >= 1.7.0
- APScheduler >= 3.10.0

## License

Free to use and modify for personal and commercial projects.

## Author

Created as a tutorial for building cross-platform GUI applications with Python and Fluent Design.
