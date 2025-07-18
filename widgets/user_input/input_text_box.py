import sys
from PySide6.QtWidgets import (
    QTextEdit
)

from PySide6.QtCore import Qt


class InputTextBox(QTextEdit):
    def __init__(self, send_button, send_message):  
        super().__init__()
        self.setFixedHeight(32) # Initial height for the textbox
        self.textChanged.connect(self.adjust_input_height) # increase input box size based on how much the user types up to 3 times the normal

        self.send_button = send_button
        self.send_message = send_message

    def adjust_input_height(self): 
        doc = self.document()
        height = doc.size().height() + 10
        font_metrics = self.fontMetrics()
        line_height = font_metrics.lineSpacing()
        max_height = line_height * 3 + 10
        new_height = min(height, max_height)
        self.setFixedHeight(new_height)

    # When user in the inputtextbox, if they press enter/return, starts send_message. shift/ctrl + enter replaces its functionality
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() in (Qt.ShiftModifier, Qt.ControlModifier):
                super().keyPressEvent(event) 
            else:
                if self.send_button.isEnabled():
                    self.send_message()
        else:
            super().keyPressEvent(event)




