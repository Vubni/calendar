from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import loadUiType
import os
import sys

# Проверка пути к UI-файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(current_dir, "src-ui", "mainwindow.ui")
if not os.path.exists(ui_file):
    raise FileNotFoundError(f"UI file not found: {ui_file}")

# Загрузка UI
Ui_MainWindow, QMainWindowBase = loadUiType(ui_file)

class MainWindow(QMainWindowBase, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())