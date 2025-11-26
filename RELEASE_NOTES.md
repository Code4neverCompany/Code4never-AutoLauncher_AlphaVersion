
### 🔧 Critical Updater Fix
- **Dynamic Executable Support**: The auto-updater now correctly handles cases where the application executable has been renamed (e.g., to `c4n-AutoLauncher.exe`). Previously, the update process would fail to terminate the old process if it wasn't named exactly `Autolauncher.exe`.
- **Improved Installation**: Enhanced the robustness of the update installation script.

---

## 📥 Installation

### Option 1: Auto-Update (If You Have v1.0.9)
1. App will detect v1.0.10 automatically
2. Click notification or go to About tab
3. Click "Update" button
4. Done! App restarts with new version

### Option 2: Fresh Install
1. Download `c4n-AutoLauncher_v1.0.10.zip` from GitHub Releases
2. Extract ZIP file
3. Run `c4n-AutoLauncher.exe`
4. Enjoy!

---

## 🔧 Technical Improvements

### Files Modified
- `update_manager.py` - Fixed hardcoded process name in `taskkill` command

---

## 🐛 Bug Fixes

✅ Fixed update failure when executable is renamed
✅ Improved update script error handling

---

## 📊 Performance Stats

- **Startup Time**: ~2 seconds
- **Memory Usage**: ~80MB
- **Update Check**: < 0.5 seconds (with ETag)

---

## 🎯 System Requirements

- **OS**: Windows 10 or Windows 11
- **RAM**: 100MB minimum
- **Disk Space**: 150MB
- **Internet**: Optional (only for updates)

---

## 📞 Support

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/Code4neverCompany/Code4never-AutoLauncher_AlphaVersion/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Code4neverCompany/Code4never-AutoLauncher_AlphaVersion/discussions)
- 📖 **Documentation**: See README.md

---

## 🙏 Credits

**Developed by**: 4never Company  
**UI Framework**: PyQt5 + qfluentwidgets  
**Update System**: GitHub API + HTTP ETags  

---

**Thank you for using c4n-AutoLauncher!** 🚀

Your feedback drives continuous improvement.

---

**Release Date**: November 25, 2025  
**Version**: 1.0.10-alpha  
**Build**: Alpha Release 10
