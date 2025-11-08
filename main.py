from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
import os
import sys

# Проверка пути к UI-файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(current_dir, "src-ui", "mainwindow.ui")
if not os.path.exists(ui_file):
    raise FileNotFoundError(f"UI file not found: {ui_file}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file, self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())