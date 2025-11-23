"""
Log Dialog Module
Displays the task execution log.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    TableWidget,
    PushButton,
    FluentIcon
)

from execution_logger import ExecutionLogger
from logger import get_logger

logger = get_logger(__name__)

class LogDialog(MessageBoxBase):
    """Dialog to display execution logs."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.execution_logger = ExecutionLogger()
        
        # UI Setup
        self.titleLabel = SubtitleLabel("Execution Log", self)
        self.viewLayout.addWidget(self.titleLabel)
        
        # Table
        self.logTable = TableWidget(self)
        self.logTable.setColumnCount(4)
        self.logTable.setHorizontalHeaderLabels(["Time", "Task", "Event", "Details"])
        self.logTable.verticalHeader().hide()
        self.logTable.setBorderVisible(True)
        self.logTable.setBorderRadius(8)
        self.logTable.setWordWrap(False)
        self.logTable.setMinimumHeight(400)
        self.logTable.setMinimumWidth(700)
        
        # Resize columns
        self.logTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) # Time
        self.logTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) # Task
        self.logTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) # Event
        self.logTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)          # Details
        
        self.viewLayout.addWidget(self.logTable)
        
        # Buttons
        # We use the standard button layout provided by MessageBoxBase
        self.yesButton.setText("Refresh")
        self.yesButton.setIcon(FluentIcon.SYNC)
        self.yesButton.clicked.disconnect()
        self.yesButton.clicked.connect(self._load_logs)
        
        self.cancelButton.setText("Close")
        self.cancelButton.clicked.disconnect()
        self.cancelButton.clicked.connect(self.accept) # Close dialog
        
        # Add a custom "Clear Log" button to the button layout
        self.clearButton = PushButton(FluentIcon.DELETE, "Clear Log", self.buttonGroup)
        self.clearButton.clicked.connect(self._clear_logs)
        self.buttonLayout.insertWidget(1, self.clearButton) # Insert between Refresh and Close
        
        # Load data
        self._load_logs()
        
        # Adjust dialog size
        self.widget.setMinimumWidth(750)
        
    def _load_logs(self):
        """Load logs into the table."""
        logs = self.execution_logger.get_logs(limit=100)
        self.logTable.setRowCount(len(logs))
        
        for i, entry in enumerate(logs):
            # Format timestamp
            try:
                dt = datetime.fromisoformat(entry['timestamp'])
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_str = entry['timestamp']
                
            self.logTable.setItem(i, 0, QTableWidgetItem(time_str))
            self.logTable.setItem(i, 1, QTableWidgetItem(str(entry['task_name'])))
            self.logTable.setItem(i, 2, QTableWidgetItem(str(entry['event_type'])))
            self.logTable.setItem(i, 3, QTableWidgetItem(str(entry['details'])))
            
    def _clear_logs(self):
        """Clear the logs."""
        self.execution_logger.clear_logs()
        self._load_logs()

from datetime import datetime
