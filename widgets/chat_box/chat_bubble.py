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

    def update_height(self):
        doc_height = self.document().size().toSize().height()
        margins = self.contentsMargins()
        new_height = doc_height + margins.top() + margins.bottom()
        # self.setFixedHeight(new_height)
        
        per_line_height = self.fontMetrics().lineSpacing()
        
        if not hasattr(self, 'current_height'):
            self.current_height = new_height

        # only change the height when the new height is not drastically different than the current height (to avoid glitchy ui)
        if new_height < self.current_height + (2)*per_line_height:
            self.setFixedHeight(new_height)
            self.current_height = new_height
        

       


    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.update_height()

    def wheelEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        # Ignore key events that could cause scrolling
        if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
            event.ignore()
        else:
            super().keyPressEvent(event)

            
        