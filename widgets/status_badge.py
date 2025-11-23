"""
StatusBadge Widget
Colored badge indicating task status (Active/Paused).
"""

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget


class StatusBadge(QWidget):
    """
    Visual status indicator with color and animation.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 24)
        self._status = "Active"
        self._pulse_opacity = 1.0
        
        # Pulse animation for active status
        self._pulse_animation = QPropertyAnimation(self, b"pulseOpacity")
        self._pulse_animation.setDuration(1000)
        self._pulse_animation.setStartValue(1.0)
        self._pulse_animation.setEndValue(0.5)
        self._pulse_animation.setEasingCurve(QEasingCurve.InOutSine)
        self._pulse_animation.setLoopCount(-1)  # Infinite loop
    
    @pyqtProperty(float)
    def pulseOpacity(self):
        return self._pulse_opacity
    
    @pulseOpacity.setter
    def pulseOpacity(self, value):
        self._pulse_opacity = value
        self.update()
    
    def set_status(self, status):
        """Set status: 'Active' or 'Paused'."""
        self._status = status
        
        if status == "Active":
            self._pulse_animation.start()
        else:
            self._pulse_animation.stop()
            self._pulse_opacity = 1.0
        
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for status badge."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Status colors
        if self._status == "Active":
            bg_color = QColor(76, 175, 80, int(255 * self._pulse_opacity))  # Green
            text_color = QColor(255, 255, 255)
        else:  # Paused
            bg_color = QColor(255, 152, 0)  # Orange
            text_color = QColor(255, 255, 255)
        
        # Draw rounded rectangle
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        
        # Draw text
        painter.setPen(text_color)
        font = QFont("Segoe UI", 8, QFont.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, self.width(), self.height(), Qt.AlignCenter, self._status)
