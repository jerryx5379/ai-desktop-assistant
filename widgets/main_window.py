from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser
)
from PySide6.QtCore import Qt


import pathlib
import json

from .chat_box import ChatBox
from .user_input import UserInput
from widgets.chat_box import ChatBubble

class MainWindow(QWidget):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant")
        self.setMinimumSize(150,250) 
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.main_layout = QVBoxLayout(self)

        self.chat_box = ChatBox()
        self.user_input = UserInput(self.chat_box) 

        self.main_layout.addWidget(self.chat_box)
        self.main_layout.addLayout(self.user_input)

       
        
    def showEvent(self, event): 
        super().showEvent(event)

        # reopen the window in the location it was last closed
        self.config_path = pathlib.Path.home() / ".Ollama_project_config.json"
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                settings = json.load(f)
                self.move(*settings["pos"])
                self.resize(*settings["size"])

    def closeEvent(self, event):  # just need to change thhis one
        settings = {
            "pos": [self.pos().x(), self.pos().y()],
            "size": [self.size().width(), self.size().height()]
        }
        with open(self.config_path, "w") as f:
            json.dump(settings, f)
        event.accept()  



    




