# Release Notes: c4n-AutoLauncher v1.0.6

**Release Date:** November 23, 2025

## 🎉 What's New

### Task Management Enhancements
- **⏸️ Pause/Resume Tasks** - Temporarily pause scheduled tasks without deleting them
  - Visual status indicator (Active/Paused)
  - Maintains task position while paused
  - Selection preserved after pause/resume action
  
- **⏱️ Live Countdown Timers** - Real-time countdown display for all scheduled tasks
  - Shows time remaining until next execution (e.g., "2h 15m 30s")
  - Intelligent handling of daily recurring tasks (calculates next day's occurrence)
  - Paused tasks show static schedule without countdown

### Customization Features
- **📅 Date Format Options** - Choose your preferred date display format
  - YYYY-MM-DD (ISO standard)
  - DD.MM.YYYY (European)
  - MM/DD/YYYY (US)
  - DD-MM-YYYY (Alternative)
  - Live table updates when format changes

### Monitoring & Logging
- **📊 Execution Log** - Comprehensive event tracking system
  - Tracks: STARTED, FINISHED, FAILED, POSTPONED, SKIPPED events
  - View logs in clean table dialog
  - Clear and Refresh functionality
  - Persistent storage across sessions

### UI/UX Improvements
- **🎨 Cleaner Task List** - Icons now inline with task names
  - Removed separate icon column for better space utilization
  - Professional appearance with integrated icons
  - Theme-aware text colors (white in dark mode, black in light mode)
  - Automatic theme updates when toggling

- **⚙️ Settings Layout** - Fixed truncation issues
  - All labels now fully visible
  - Concise, readable descriptions
  - Proper alignment and spacing

- ** 🖼️ Icon Handling** - Enhanced icon extraction
  - Auto-extraction for .lnk (shortcut) files
  - Icons cached to disk for performance
  - Graceful fallback for missing icons

## 📦 Installation

### New Installation
1. Download `c4n-AutoLauncher_v1.0.6_Setup.exe`
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### Updating from Previous Version
**Option 1: Auto-Update (Recommended)**
- Open the application
- Navigate to About section
- Click "Check for Updates"
- Click "Update" when available
- Application will restart with new version

**Option 2: Manual Update**
1. Download `c4n-AutoLauncher_v1.0.6.zip`
2. Extract to your installation directory
3. Replace existing files
4. Restart the application

## 🔧 Technical Details

**Files Changed:**
- `autolauncher.py` - Main UI and countdown logic
- `scheduler.py` - Pause/resume task handling
- `settings_interface.py` - Date format settings
- `execution_logger.py` - NEW: Event logging system
- `log_dialog.py` - NEW: Log viewer dialog
- `config.py` - Version update to 1.0.6
- `version_info.json` - Changelog update

**Dependencies:**
- Python 3.14 (for development)
- PyQt5
- qfluentwidgets
- APScheduler
- All dependencies bundled in executable

## 🐛 Bug Fixes
- Fixed task selection clearing after pause/resume
- Fixed daily task countdown showing past times
- Fixed Settings label truncation
- Fixed icon column not adapting to theme
- Fixed .lnk shortcut icon extraction

##💡 Usage Tips
1. **Pause Long Tasks During Work Hours** - Use pause/resume for tasks you don't want to run while working
2. **Monitor Task History** - Check the Execution Log to see which tasks ran successfully
3. **Customize Your View** - Change date format to match your regional preferences
4. **Use Countdown Timers** - Quickly see when your next task will run

## 🔮 Coming Soon
- Modern card-based UI for task list
- Task categories and tags
- Enhanced smart execution modes
- Task chains and dependencies

---

**Full Changelog**: https://github.com/Code4neverCompany/Code4never-AutoLauncher_AlphaVersion/compare/v1.0.5...v1.0.6

**4never Company** | Built with ❤️ using PyQt5 and QFluentWidgets
