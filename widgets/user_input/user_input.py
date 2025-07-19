from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QThread

import markdown

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from .input_text_box import InputTextBox

class UserInput(QHBoxLayout):
    def __init__(self, chat_box):
        super().__init__()
        self.chat_box = chat_box
        
        self.send_button = QPushButton("Send") 
        self.send_button.clicked.connect(self.send_message) # starts main logic of sending message to llm

        self.input_text = InputTextBox(send_button=self.send_button, send_message=self.send_message)

        self.addWidget(self.input_text) 
        self.addWidget(self.send_button) 


    def send_message(self):
        text = self.input_text.toPlainText().strip() 
        if not text:
            return

        self.send_button.setEnabled(False) 

        # This adds the user's text message to the chat_box
        self.chat_bubble = ChatBubble(text=text, sender= "user")
        self.chat_box.scroll_layout.insertWidget(self.chat_box.scroll_layout.count(), self.chat_bubble)
        self.input_text.clear()

        self.chat_box.verticalScrollBar().setValue( # scroll down
            self.chat_box.verticalScrollBar().maximum()
        )

        # This adds the llm's response to chatbox. while the response is being streamed on another thread, user cannot send another message
        self.chat_bubble = ChatBubble(text=text,sender = "assistant")
        self.chat_box.scroll_layout.insertWidget(self.chat_box.scroll_layout.count(), self.chat_bubble)

        self.thread = QThread()
        self.thread.setObjectName("Ollama_inference_thread")
        self.worker = OllamaWorker(user_prompt=text)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.stream_ollama)
        self.worker.text_chunk.connect(self.handle_output_chunk)
        self.worker.finished.connect(self.worker_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def handle_output_chunk(self, chunk):
        # Append new chunk to chat_bubble, keeping existing text
        self.chat_bubble.moveCursor(QTextCursor.End)
        self.chat_bubble.insertPlainText(chunk)
        self.chat_bubble.ensureCursorVisible()

    def worker_finished(self):
        # basic formatting: get the plain text, convert it to html then set html
        text = self.chat_bubble.toPlainText()
        text_html = markdown.markdown(text=text,extensions=['fenced_code','tables'])
        self.chat_bubble.setHtml(text_html)

        self.send_button.setEnabled(True) 

        
    
