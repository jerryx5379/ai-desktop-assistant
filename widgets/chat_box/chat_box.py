from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt

# this is the area where the user and assistant message show up
class ChatBox(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)  # Automatically resize the QWidget inside the scrollarea to the scrollarea viewport size
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget() # This is the "div" that is inside scroll_area
        self.scroll_layout = QVBoxLayout(self.scroll_content) # This is the vertical layoutbox inside that "div"
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.setWidget(self.scroll_content)

        