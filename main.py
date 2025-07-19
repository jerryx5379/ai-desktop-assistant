"""
This is the entry point to the application.
This file creates the application and starts the event loop
It also sets application level details like system name of this app, application style

This project is structured based on ui components (widgets)
The MainWindow has the ChatBox and UserInput components
The ChatBox holds the messages(ChatBubble) between the user and llm(assistant) 
THe UserInput has a InputTextBox and send_message button

The UserInput class handles the inference with Ollama
"""

# TODO: add load model and unload model on program start and end

# This version TODO: Better user experience
# 1. Make the height of the ChatBubbles better and on resizeEvent
# 2. Make the markdown to html look better (make response of llm better)
# 3. add settings to allow user to control font size etc
# 4. make the theme update automatically
# 5. let OllamaWorker have memory

from PySide6.QtWidgets import QApplication
import sys

from widgets import MainWindow



def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Desktop Assistant")
    app.setStyle("Fusion")

    window = MainWindow() 
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


    