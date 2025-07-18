import yaml
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette

class Theme:
    def __init__(self):
        config_path = Path(__file__).parent.parent / 'theme.yaml'
        with open(config_path, 'r') as f:
            self._data = yaml.safe_load(f)['themes']

        if self.is_dark_theme():
            theme_data = self._data['dark']
        else:
            theme_data = self._data['light']

        self.text_color = theme_data['text_color']
        self.chat_bubble_color = theme_data['chat_bubble_color']

    def is_dark_theme(self):
        app = QApplication.instance()
        if not app:
            raise RuntimeError("QApplication must be initialized before checking theme.")
        
        palette = app.palette()
        window_color = palette.color(QPalette.Window)
        brightness = (
            window_color.red() * 0.299 +
            window_color.green() * 0.587 +
            window_color.blue() * 0.114
        )
        return brightness < 128
