from PySide6.QtWidgets import (
    QSizePolicy, QTextBrowser
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent


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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.document().contentsChanged.connect(self.update_height)

        if sender == "user":
            self.insertPlainText(text)

        self.ignore_wheel_event = True
        self.ignore_keypress_scrolling = True

        self.code_block_font = "'Consolas', monospace"

    def update_height(self):
        doc_height = self.document().size().toSize().height()
        margins = self.contentsMargins()
        new_height = doc_height + margins.top() + margins.bottom()
        self.setFixedHeight(new_height)
        
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.update_height()

    def wheelEvent(self, event):
        if self.ignore_wheel_event:
            event.ignore()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if self.ignore_keypress_scrolling:
            # Ignore key events that could cause scrolling
            if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
                event.ignore()
        else:
            super().keyPressEvent(event)

            
        