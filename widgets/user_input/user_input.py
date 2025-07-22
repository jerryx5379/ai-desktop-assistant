from PySide6.QtWidgets import (
    QHBoxLayout,QPushButton,QTextBrowser
)
from PySide6.QtGui import QTextCursor, QFontMetrics
from PySide6.QtCore import QThread, QTimer, Qt

import markdown
from pygments.formatters.html import HtmlFormatter

from threads import OllamaWorker
from widgets.chat_box import ChatBubble
from .input_text_box import InputTextBox
from utils import Theme

class UserInput(QHBoxLayout):
    def __init__(self, chat_box):
        super().__init__()
        self.chat_box = chat_box
        
        self.send_button = QPushButton("Send") 
        self.send_button.clicked.connect(self.send_message) # starts main logic of sending message to llm

        self.input_text = InputTextBox(send_button=self.send_button, send_message=self.send_message)

        self.addWidget(self.input_text) 
        self.addWidget(self.send_button) 

        self.total_chat_bubbles_height = 0
        self.layout_spacing = self.chat_box.scroll_layout.spacing()
        self.total_scroll_content_height = 0

        sample_chat_bubble = ChatBubble(text="1",sender="user")
        QTimer.singleShot(0,lambda: self.get_indiv_line_height(sample_chat_bubble))

    def send_message(self):
        text = self.input_text.toPlainText().strip() 
        if not text:
            return

        self.send_button.setEnabled(False) 

        # This adds the user's text message to the chat_box
        self.chat_bubble = ChatBubble(text=text, sender= "user")
        self.chat_box.scroll_layout.insertWidget(self.chat_box.scroll_layout.count(), self.chat_bubble)
        self.chat_box.update_chat_context(role = "user", message = text)
        self.input_text.clear()

        sample_chat_bubble = ChatBubble(text="1",sender="user") # used to get unit height of a chat bubble
        QTimer.singleShot(0,lambda: self.add_preview_height(sample_chat_bubble))

        # This adds the llm's response to chatbox. while the response is being streamed on another thread, user cannot send another message
        self.chat_bubble = ChatBubble(text=text,sender = "assistant")
        self.chat_box.scroll_layout.insertWidget(self.chat_box.scroll_layout.count(), self.chat_bubble)

        self.thread = QThread()
        self.thread.setObjectName("Ollama_inference_thread")

        url = "http://localhost:11434/api/chat"
        data = self.chat_box.get_data()
        self.worker = OllamaWorker(url=url, data=data)
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

        if self.chat_bubble.height() + self.total_chat_bubbles_height + self.layout_spacing > self.total_scroll_content_height:
            self.total_scroll_content_height += 8*self.layout_spacing
            self.chat_box.scroll_content.setMinimumHeight(self.total_scroll_content_height)

    def worker_finished(self, response):
        self.chat_box.update_chat_context(role = "assistant", message = response)

        # basic formatting: get the plain text, convert it to html then set html
        text_html = markdown.markdown(text=response,extensions=['fenced_code','tables','codehilite'])
        theme = Theme()
        if theme.is_dark_theme():
            style = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
        else:
            style = HtmlFormatter(style='manni').get_style_defs('.codehilite')


        text_html = f"""
<style>
{style}
.codehilite {{
    font-family: {self.chat_bubble.code_block_font};
    background-color: transparent !important;

}}
</style>
{text_html}
"""
        self.chat_bubble.setHtml(text_html)

        if '<code' in text_html and '</code>' in text_html:
            self.chat_bubble.ignore_keypress_scrolling = False
            self.chat_bubble.ignore_wheel_event = False

        #adjust_height = self.chat_bubble.height() + 2*self.layout_spacing + self.total_chat_bubbles_height
        #self.chat_box.scroll_content.setMinimumHeight(adjust_height)
        
        self.send_button.setEnabled(True) 

    def add_preview_height(self, sample_chat_bubble:QTextBrowser):
        self.add_to_chat_bubbles_total_height()

        unit_height_of_chat_bubble = sample_chat_bubble.height()
        viewport_height = self.chat_box.viewport().height()
        padding_height = viewport_height - unit_height_of_chat_bubble

        self.total_scroll_content_height = self.total_chat_bubbles_height + padding_height

        self.chat_box.scroll_content.setMinimumHeight(self.total_scroll_content_height)

        self.chat_box.verticalScrollBar().setValue( 
            self.chat_box.verticalScrollBar().maximum()
        )
        

    ### Helper Functions ###
    def add_to_chat_bubbles_total_height(self):
        layout = self.chat_box.scroll_layout

        if layout.count() == 2: 
            height = layout.itemAt(0).widget().height()
            self.total_chat_bubbles_height += height 
            self.indexes_added = [0]
        else:
            last_index = self.indexes_added[-1]
            new_indexes = [last_index+1,last_index+2]
            for index in new_indexes:
                height = layout.itemAt(index).widget().height()
                self.total_chat_bubbles_height += height + self.layout_spacing
                self.indexes_added.append(index)

    def get_indiv_line_height(self, sample_chat_bubble:QTextBrowser):
        line_height = QFontMetrics(sample_chat_bubble.font()).lineSpacing()
        self.indiv_line_height = line_height

    

        
        

        


        

        
    
