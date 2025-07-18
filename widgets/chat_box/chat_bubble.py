from PySide6.QtWidgets import (
    QSizePolicy, QTextBrowser
)
from PySide6.QtCore import Qt

from utils import Theme

class ChatBubble(QTextBrowser):
    def __init__(self, text, sender): # sender can be "user" or "assistant"
        super().__init__()
        theme = Theme()

        self.setOpenExternalLinks(True)
        self.setStyleSheet(
            f"""
                background-color: {theme.chat_bubble_color if sender == "user" else 'transparent'};
                border-radius: 10px; 
                padding: 8px;
                margin: 4px;
                color: {theme.text_color};
                border: none;
            """
        )
        self.setFrameStyle(QTextBrowser.NoFrame)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        if sender == "user":
            self.insertPlainText(text)

    def wheelEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        # Ignore key events that could cause scrolling
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
            event.ignore()
        else:
            super().keyPressEvent(event)

            
        