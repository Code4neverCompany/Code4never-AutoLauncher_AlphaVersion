"""
Settings Interface Module
Displays application settings.

© 2025 4never Company. All rights reserved.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import (
    SettingCardGroup,
    SwitchSettingCard,
    FolderListSettingCard,
    OptionsSettingCard,
    PushSettingCard,
    HyperlinkCard,
    PrimaryPushSettingCard,
    ScrollArea,
    ComboBoxSettingCard,
    ExpandLayout,
    Theme,
    InfoBar,
    CustomColorSettingCard,
    setTheme,
    setThemeColor,
    RangeSettingCard,
    ColorDialog,
    SettingCard,
    ComboBox,
    FluentIcon,
    InfoBarPosition,
    IndeterminateProgressRing
)
from task_manager import SettingsManager
from logger import get_logger
from language_manager import get_language_manager, set_language
from config import DEFAULT_LANGUAGE

logger = get_logger(__name__)


class SettingsInterface(ScrollArea):
    """
    Settings interface for application preferences.
    """
    
    date_format_changed = pyqtSignal()
    language_changed = pyqtSignal()
    
    def __init__(self, settings_manager=None, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager if settings_manager else SettingsManager()
        
        # Initialize language manager
        self.lang_manager = get_language_manager()
        saved_language = self.settings_manager.get('language', DEFAULT_LANGUAGE)
        self.lang_manager.set_language(saved_language)
        
        self.scrollWidget = QWidget()
        self.expandLayout = QVBoxLayout(self.scrollWidget)
        
        # Set object name for styling
        self.setObjectName("settingsInterface")
        self.scrollWidget.setObjectName("scrollWidget")
        
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components."""
        
        # Configure layout
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        
        # Set transparent background to fix Light mode issue
        self.scrollWidget.setStyleSheet("QWidget{background-color: transparent;}")
        self.setStyleSheet("QScrollArea{background-color: transparent; border: none;}")
        
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        
        # --- General Settings Group ---
        self.generalGroup = SettingCardGroup("General", self.scrollWidget)
        
        # Execution Mode Setting
        self.executionModeCard = SettingCard(
            FluentIcon.ROBOT,
            "Execution Mode",
            "Choose how tasks should behave when you are using the computer",
            parent=self.generalGroup
        )
        
        self.modeComboBox = ComboBox(self.executionModeCard)
        self.modeComboBox.addItems(["Automatic (Postpone if busy)", "Interactive (Ask if busy)", "Aggressive (Run always)"])
        self.executionModeCard.hBoxLayout.addWidget(self.modeComboBox, 0, Qt.AlignRight)
        self.executionModeCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        # Migrate old 'automode' bool if present
        mode = self.settings_manager.get('execution_mode', 'ask')
        if self.settings_manager.get('automode', False):
            mode = 'auto'
            
        # Map mode string to index
        mode_map = {'auto': 0, 'ask': 1, 'run': 2}
        self.modeComboBox.setCurrentIndex(mode_map.get(mode, 1))
        
        # Connect signal
        self.modeComboBox.currentIndexChanged.connect(self._on_execution_mode_changed)
        
        self.generalGroup.addSettingCard(self.executionModeCard)
        
        # Pre-wake Duration Setting
        self.preWakeCard = SettingCard(
            FluentIcon.POWER_BUTTON,
            "Pre-wake Duration",
            "How many minutes before a task to wake the computer",
            parent=self.generalGroup
        )
        
        self.preWakeComboBox = ComboBox(self.preWakeCard)
        self.preWakeComboBox.addItems(["1 minute", "3 minutes", "5 minutes", "10 minutes", "15 minutes"])
        self.preWakeCard.hBoxLayout.addWidget(self.preWakeComboBox, 0, Qt.AlignRight)
        self.preWakeCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        pre_wake = self.settings_manager.get('pre_wake_minutes', 5)
        pre_wake_map = {1: 0, 3: 1, 5: 2, 10: 3, 15: 4}
        self.preWakeComboBox.setCurrentIndex(pre_wake_map.get(pre_wake, 2))
        
        # Connect signal
        self.preWakeComboBox.currentIndexChanged.connect(self._on_pre_wake_changed)
        
        self.generalGroup.addSettingCard(self.preWakeCard)
        
        # Date Format Setting
        self.dateFormatCard = SettingCard(
            FluentIcon.CALENDAR,
            "Date Format",
            "Choose your preferred date display format",
            parent=self.generalGroup
        )
        
        self.dateFormatComboBox = ComboBox(self.dateFormatCard)
        self.dateFormatComboBox.addItems(["YYYY-MM-DD", "DD.MM.YYYY", "MM/DD/YYYY", "DD-MM-YYYY"])
        self.dateFormatCard.hBoxLayout.addWidget(self.dateFormatComboBox, 0, Qt.AlignRight)
        self.dateFormatCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        date_format = self.settings_manager.get('date_format', 'YYYY-MM-DD')
        format_map = {'YYYY-MM-DD': 0, 'DD.MM.YYYY': 1, 'MM/DD/YYYY': 2, 'DD-MM-YYYY': 3}
        self.dateFormatComboBox.setCurrentIndex(format_map.get(date_format, 0))
        
        # Connect signal
        self.dateFormatComboBox.currentIndexChanged.connect(self._on_date_format_changed)
        
        self.generalGroup.addSettingCard(self.dateFormatCard)
        
        # Time Format Setting
        self.timeFormatCard = SettingCard(
            FluentIcon.HISTORY,
            "Time Format",
            "Choose between 12-hour and 24-hour time display",
            parent=self.generalGroup
        )
        
        self.timeFormatComboBox = ComboBox(self.timeFormatCard)
        self.timeFormatComboBox.addItems(["24-hour (14:30)", "12-hour (2:30 PM)"])
        self.timeFormatCard.hBoxLayout.addWidget(self.timeFormatComboBox, 0, Qt.AlignRight)
        self.timeFormatCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        time_format = self.settings_manager.get('time_format', '24h')
        format_map = {'24h': 0, '12h': 1}
        self.timeFormatComboBox.setCurrentIndex(format_map.get(time_format, 0))
        
        # Connect signal
        self.timeFormatComboBox.currentIndexChanged.connect(self._on_time_format_changed)
        
        self.generalGroup.addSettingCard(self.timeFormatCard)
        
        # Language Setting
        self.languageCard = SettingCard(
            FluentIcon.LANGUAGE,
            "Language",
            "Choose your preferred interface language",
            parent=self.generalGroup
        )
        
        self.languageComboBox = ComboBox(self.languageCard)
        # Get available languages from language manager
        available_languages = self.lang_manager.get_available_languages()
        self.language_codes = list(available_languages.keys())
        self.languageComboBox.addItems(list(available_languages.values()))
        self.languageCard.hBoxLayout.addWidget(self.languageComboBox, 0, Qt.AlignRight)
        self.languageCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        current_language = self.settings_manager.get('language', DEFAULT_LANGUAGE)
        if current_language in self.language_codes:
            self.languageComboBox.setCurrentIndex(self.language_codes.index(current_language))
        
        # Connect signal
        self.languageComboBox.currentIndexChanged.connect(self._on_language_changed)
        
        self.generalGroup.addSettingCard(self.languageCard)
        
        # --- Updates Settings Group ---
        self.updatesGroup = SettingCardGroup("Updates", self.scrollWidget)
        
        # Auto-Update Mode Setting
        self.autoUpdateCard = SettingCard(
            FluentIcon.UPDATE,
            "Auto-Update Mode",
            "Automatic: checks every 2 min, installs when next task is >30 min away",
            parent=self.updatesGroup
        )
        
        self.updateFrequencyComboBox = ComboBox(self.autoUpdateCard)
        self.updateFrequencyComboBox.addItems(["On Startup", "Manual Only", "Automatic (Smart)"])
        self.autoUpdateCard.hBoxLayout.addWidget(self.updateFrequencyComboBox, 0, Qt.AlignRight)
        self.autoUpdateCard.hBoxLayout.addSpacing(16)
        
        # Set initial state
        frequency = self.settings_manager.get('auto_update_frequency', 'startup')
        frequency_map = {'startup': 0, 'manual': 1, 'automatic': 2}
        self.updateFrequencyComboBox.setCurrentIndex(frequency_map.get(frequency, 0))
        
        # Connect signal
        self.updateFrequencyComboBox.currentIndexChanged.connect(self._on_update_frequency_changed)
        
        self.updatesGroup.addSettingCard(self.autoUpdateCard)

        
        # Add groups to layout
        self.expandLayout.addWidget(self.generalGroup)
        self.expandLayout.addWidget(self.updatesGroup)
        self.expandLayout.addStretch(1)
        
    def _on_execution_mode_changed(self, index: int):
        """Handle execution mode change."""
        modes = ['auto', 'ask', 'run']
        if 0 <= index < len(modes):
            mode = modes[index]
            self.settings_manager.set('execution_mode', mode)
            # Update legacy key for compatibility if needed, or just ignore it
            self.settings_manager.set('automode', mode == 'auto')
            
            logger.info(f"Execution mode set to: {mode}")
            
            InfoBar.success(
                title="Settings Saved",
                content=f"Execution Mode updated",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    def _on_pre_wake_changed(self, index: int):
        """Handle pre-wake duration change."""
        durations = [1, 3, 5, 10, 15]
        if 0 <= index < len(durations):
            duration = durations[index]
            self.settings_manager.set('pre_wake_minutes', duration)
            
            logger.info(f"Pre-wake duration set to: {duration} minutes")
            
            InfoBar.success(
                title="Settings Saved",
                content=f"Pre-wake duration: {duration} min",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
    
    def _on_update_frequency_changed(self, index: int):
        """Handle update frequency change."""
        frequencies = ['startup', 'manual', 'automatic']
        if 0 <= index < len(frequencies):
            frequency = frequencies[index]
            self.settings_manager.set('auto_update_frequency', frequency)
            
            logger.info(f"Auto-update mode set to: {frequency}")
            
            mode_names = ["On Startup", "Manual Only", "Automatic (Smart)"]
            
            InfoBar.success(
                title="Settings Saved",
                content=f"Update mode: {mode_names[index]}. Restart app to apply.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
    
    def _on_date_format_changed(self, index: int):
        """Handle date format change."""
        formats = ['YYYY-MM-DD', 'DD.MM.YYYY', 'MM/DD/YYYY', 'DD-MM-YYYY']
        if 0 <= index < len(formats):
            date_format = formats[index]
            self.settings_manager.set('date_format', date_format)
            
            logger.info(f"Date format set to: {date_format}")
            
            # Emit signal to update UI immediately
            self.date_format_changed.emit()
            
            InfoBar.success(
                title="Settings Saved",
                content=f"Date format: {date_format}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
    
    def _on_time_format_changed(self, index: int):
        """Handle time format change."""
        formats = ['24h', '12h']
        if 0 <= index < len(formats):
            time_format = formats[index]
            self.settings_manager.set('time_format', time_format)
            
            logger.info(f"Time format set to: {time_format}")
            
            InfoBar.success(
                title="Settings Saved",
                content=f"Time format: {'24-hour' if time_format == '24h' else '12-hour'}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    
    def _on_language_changed(self, index: int):
        """Handle language change."""
        if 0 <= index < len(self.language_codes):
            language_code = self.language_codes[index]
            self.settings_manager.set('language', language_code)
            
            # Update language manager
            set_language(language_code)
            
            logger.info(f"Language set to: {language_code}")
            
            # Reload UI text
            self.reload_ui_text()
            
            # Emit signal for other components
            self.language_changed.emit()
            
            # Get language display name
            lang_display = self.languageComboBox.currentText()
            
            InfoBar.success(
                title=self.lang_manager.get_text("settings.settings_saved"),
                content=self.lang_manager.format_text("settings.language_updated", language=lang_display),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
    
    def reload_ui_text(self):
        """Reload all UI text with current language."""
        lang = self.lang_manager
        
        # Update group titles
        self.generalGroup.titleLabel.setText(lang.get_text("settings.general"))
        self.updatesGroup.titleLabel.setText(lang.get_text("settings.updates"))
        
        # Update Execution Mode card
        self.executionModeCard.titleLabel.setText(lang.get_text("settings.execution_mode"))
        self.executionModeCard.contentLabel.setText(lang.get_text("settings.execution_mode_desc"))
        self.modeComboBox.clear()
        self.modeComboBox.addItems([
            lang.get_text("settings.execution_mode_auto"),
            lang.get_text("settings.execution_mode_ask"),
            lang.get_text("settings.execution_mode_run")
        ])
        # Restore selection
        mode = self.settings_manager.get('execution_mode', 'ask')
        mode_map = {'auto': 0, 'ask': 1, 'run': 2}
        self.modeComboBox.setCurrentIndex(mode_map.get(mode, 1))
        
        # Update Pre-wake card
        self.preWakeCard.titleLabel.setText(lang.get_text("settings.pre_wake"))
        self.preWakeCard.contentLabel.setText(lang.get_text("settings.pre_wake_desc"))
        # Note: ComboBox items are numbers, so translation might not be strictly needed unless we add "minutes" text dynamically
        # For now, we keep them hardcoded or we could rebuild the list.
        # Let's rebuild to be safe if we want to translate "minute(s)"
        self.preWakeComboBox.clear()
        self.preWakeComboBox.addItems([
            f"1 {lang.get_text('settings.minute')}",
            f"3 {lang.get_text('settings.minutes')}",
            f"5 {lang.get_text('settings.minutes')}",
            f"10 {lang.get_text('settings.minutes')}",
            f"15 {lang.get_text('settings.minutes')}"
        ])
        pre_wake = self.settings_manager.get('pre_wake_minutes', 5)
        pre_wake_map = {1: 0, 3: 1, 5: 2, 10: 3, 15: 4}
        self.preWakeComboBox.setCurrentIndex(pre_wake_map.get(pre_wake, 2))
        
        # Update Date Format card
        self.dateFormatCard.titleLabel.setText(lang.get_text("settings.date_format"))
        self.dateFormatCard.contentLabel.setText(lang.get_text("settings.date_format_desc"))
        
        # Update Time Format card
        self.timeFormatCard.titleLabel.setText(lang.get_text("settings.time_format"))
        self.timeFormatCard.contentLabel.setText(lang.get_text("settings.time_format_desc"))
        self.timeFormatComboBox.clear()
        self.timeFormatComboBox.addItems([
            lang.get_text("settings.time_format_24h"),
            lang.get_text("settings.time_format_12h")
        ])
        # Restore selection
        time_format = self.settings_manager.get('time_format', '24h')
        format_map = {'24h': 0, '12h': 1}
        self.timeFormatComboBox.setCurrentIndex(format_map.get(time_format, 0))
        
        # Update Language card
        self.languageCard.titleLabel.setText(lang.get_text("settings.language"))
        self.languageCard.contentLabel.setText(lang.get_text("settings.language_desc"))
        
        # Update Auto-Update card
        self.autoUpdateCard.titleLabel.setText(lang.get_text("settings.auto_update_mode"))
        self.autoUpdateCard.contentLabel.setText(lang.get_text("settings.auto_update_mode_desc"))
        self.updateFrequencyComboBox.clear()
        self.updateFrequencyComboBox.addItems([
            lang.get_text("settings.auto_update_startup"),
            lang.get_text("settings.auto_update_manual"),
            lang.get_text("settings.auto_update_automatic")
        ])
        # Restore selection
        frequency = self.settings_manager.get('auto_update_frequency', 'startup')
        frequency_map = {'startup': 0, 'manual': 1, 'automatic': 2}
        self.updateFrequencyComboBox.setCurrentIndex(frequency_map.get(frequency, 0))
        
        logger.debug("UI text reloaded for new language")
