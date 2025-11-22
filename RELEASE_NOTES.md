# c4n-AutoLauncher v1.0.1-alpha Release Notes

**Update System Migration Release** - Enhanced User Experience

© 2025 4never Company. All rights reserved.

---

## 🎉 What's New in v1.0.1-alpha

### 🔄 Redesigned Update System
- **Dedicated About Section**: Update controls moved from Settings to a new About page
- **Enhanced Notifications**: Prominent update notifications with clickable "View Details" button
- **Better Discoverability**: Update system is now more visible and accessible
- **Navigation Integration**: About section added to bottom navigation panel (above Settings)

### ✨ User Experience Improvements
- **One-Click Navigation**: Click notification to jump directly to About page
- **Streamlined Settings**: Settings page now focuses only on update frequency configuration
- **Clear Instructions**: Descriptive text guides users to About page for manual checks
- **Professional Branding**: Application renamed to **c4n-AutoLauncher**

### 🔧 Technical Improvements
- **PyQt5 Compatibility**: Fixed import issues in About interface
- **Code Cleanup**: Removed duplicate update checking functionality
- **Better Architecture**: Separation of concerns between Settings and About sections

---

## 📥 Installation

### Option 1: Standalone Executable (Recommended)
1. Download `c4n-AutoLauncher.exe` from the release
2. Run it - no installation needed!
3. (Optional) Create a desktop shortcut

### Option 2: Run from Source
1. Download source code ZIP
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python autolauncher.py`

---

## 🚀 Update System Workflow

### Automatic Updates (Default)
1. App checks for updates on startup (10 seconds after launch)
2. If update available: Green notification appears with version number
3. Click **"View Details"** button in notification
4. Navigate to About page automatically
5. Click **"Check for Updates"** → **"Download & Install"**
6. Monitor download progress
7. Click **"Install Now"** → App restarts automatically

### Manual Updates
1. Click **About** in bottom navigation panel
2. Click **"Check for Updates"** button
3. If available: Dialog shows version and release notes
4. Click **"Download & Install"** → Progress bar shows download
5. Confirm installation → App restarts with new version

### Configure Update Frequency
1. Navigate to **Settings**
2. Under "Updates" section
3. Choose frequency:
   - **Disabled**: No automatic checks
   - **On Startup Only**: Check once when app launches
   - **Daily**: Check every 24 hours
   - **Weekly**: Check every 7 days

---

## 🎯 Key Features

### Navigation
✅ **About Section** - New dedicated page for app information and updates  
✅ **Version Display** - Shows current version and execution mode  
✅ **Changelog** - View release history with expandable cards  
✅ **GitHub Link** - Direct link to source code repository  

### Update Notifications
✅ **Persistent Notifications** - Stays visible until dismissed  
✅ **Success-Style Badge** - Green notification for better visibility  
✅ **Action Button** - "View Details" navigates to About page  
✅ **Version Info** - Shows available version in notification title  

### Settings Management
✅ **Update Frequency** - Configure automatic check schedule  
✅ **Clean Interface** - Removed duplicate controls  
✅ **Helpful Text** - Guides users to About page for manual checks  

---

## 🔧 What Changed

### Files Modified
- `about_interface.py` - Fixed PyQt5 compatibility
- `autolauncher.py` - Integrated About section, enhanced notifications
- `settings_interface.py` - Removed duplicate update controls
- `config.py` - Updated app name to c4n-AutoLauncher
- `version_info.json` - Version 1.0.1 with new changelog

### Architecture Improvements
- **Better Separation**: Settings for configuration, About for information
- **Enhanced UX**: Clickable notifications guide users through update process
- **Code Quality**: Removed duplicate code, improved maintainability

---

## 🎯 System Requirements

- **OS**: Windows 10 or Windows 11
- **RAM**: 100MB minimum
- **Disk Space**: 100MB
- **Internet**: Required for update checks only (optional)

---

## ⚠️ Known Issues (Alpha)

This is an **alpha release**. Please report issues on GitHub!

Current known limitations:
- Windows-only (no macOS/Linux support yet)
- Update system requires GitHub release for testing
- No delta updates (full ZIP download required)

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

## 🔄 Upgrading from v1.0.0

### If You Have v1.0.0 Installed:
The auto-update system will detect v1.0.1:
1. Notification will appear: "Update Available: v1.0.1"
2. Click "View Details"
3. Click "Download & Install"
4. App restarts automatically with new version

### If Running from Source:
```powershell
git pull origin main
pip install -r requirements.txt
python autolauncher.py
```

---

## 💡 Tips & Tricks

1. **Quick Navigation**: Use bottom navigation panel to access About and Settings
2. **Update Notifications**: Don't dismiss them - click "View Details" to see what's new
3. **Theme Switching**: Still available via "Toggle Theme" button in toolbar
4. **Minimize to Tray**: Close button minimizes to system tray

---

## 🙏 Credits

**Developed by**: Code4never Company  
**Framework**: PyQt5 (Qt5)  
**UI Library**: qfluentwidgets (Fluent Design)  
**Build Tool**: PyInstaller  

---

## 📄 License

© 2025 4never Company. All rights reserved.

See EULA in workspace for full terms and conditions.

---

## 🔮 Roadmap

Future enhancements planned:
- [ ] Background update downloads (currently foreground)
- [ ] Delta updates (download only changes)
- [ ] Task categories and grouping
- [ ] Command-line arguments support
- [ ] Multi-language support

---

## 📞 Support

Need help?
- 📖 Read the documentation in `autolauncher_tutorial.md`
- 🐛 Report bugs on GitHub Issues
- 💬 Discussion: GitHub Discussions

---

**Thank you for using c4n-AutoLauncher!**

Your feedback helps make this app better for everyone. 🚀

---

**Release Date**: November 22, 2025  
**Version**: 1.0.1-alpha  
**Build**: Alpha Release 2
