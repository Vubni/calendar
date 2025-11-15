from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6 import QtWidgets as QtW
from PyQt6 import uic
import os
import sys
from database.functions import init_db
import asyncio
import functions as func
import qasync
from datetime import date
import datetime
import pandas as pd
import subprocess
import time
from PyQt6.QtCore import QTimer

current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(current_dir, "src-ui", "mainwindow.ui")
if not os.path.exists(ui_file):
    raise FileNotFoundError(f"UI file not found: {ui_file}")

def clear_layout(layout):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        
        if item.widget():
            widget = item.widget()
            widget.setParent(None)
            widget.deleteLater() 
        elif item.layout(): 
            clear_layout(item.layout()) 
            layout.removeItem(item)
        else:
            layout.removeItem(item)

class WorkWidget(QtW.QWidget):
    def __init__(self, id:int, title:str, time:str, parent=None):
        super().__init__(parent)
        uic.loadUi('./src-ui/work_widget.ui', self)

        self.id = id
        
        self.title = self.findChild(QtW.QCheckBox, 'checkBox_work')
        self.time_label = self.findChild(QtW.QLabel, 'label_work_time')
        self.edit_btn = self.findChild(QtW.QPushButton, 'pushButton_work_edit')
        self.edit_btn.setEnabled(False)
        self.delete_btn = self.findChild(QtW.QPushButton, 'pushButton_work_del')
        
        self.title.setText(title)
        self.time_label.setText(time)
        
        self.delete_btn.clicked.connect(self.delete_self)
    
    def delete_self(self):
        self.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file, self)

        self.calendar = self.findChild(QtW.QCalendarWidget, 'calendar')
        self.calendar.selectionChanged.connect(self.sync_on_date_selected)

        self.button_create = self.findChild(QtW.QPushButton, 'new_create')
        self.button_create.clicked.connect(self.sync_create_event)
        self.button_create.setEnabled(False)

        self.import_button = self.findChild(QtW.QPushButton, 'import_button')
        self.import_button.setHidden(True)
        self.export_button = self.findChild(QtW.QPushButton, 'export_button')
        self.export_button.clicked.connect(self.sync_expot)

        self.new_title = self.findChild(QtW.QPlainTextEdit, 'new_title')
        self.new_date = self.findChild(QtW.QDateEdit, 'new_date')
        self.new_date.setMinimumDate(date.today())
        self.new_time_start = self.findChild(QtW.QTimeEdit, 'new_time_start')
        self.new_time_over = self.findChild(QtW.QTimeEdit, 'new_time_over')

        self.initial_time_start = self.new_time_start.time()
        self.initial_time_over = self.new_time_over.time()

        self.new_title.textChanged.connect(self.check_create_button_state)
        self.new_date.dateChanged.connect(self.check_create_button_state)
        self.new_time_start.timeChanged.connect(self.check_create_button_state)
        self.new_time_over.timeChanged.connect(self.check_create_button_state)

        self.all_works = self.findChild(QtW.QScrollArea, 'all_works')

        # Создаем контейнер и layout для виджетов
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.addStretch()
        self.all_works.setWidget(scroll_widget)
        QTimer.singleShot(0, self.start_async_tasks)


    def start_async_tasks(self):
        asyncio.create_task(self.set_date_mero())

    async def set_date_mero(self):
        mero = await func.get_mero(date.today())
        for m in mero:
            self.add_work_widget(m["id"], m["title"], m["time_start"], m["time_stop"])
        await func.add_activity()
        
    def check_create_button_state(self):
        """Проверяет условия и разблокирует кнопку только когда все условия выполнены"""
        title = self.new_title.toPlainText()
        has_title = len(title) > 3
        has_date = self.new_date.date().isValid()
        
        time_start_changed = self.new_time_start.time() != self.initial_time_start
        time_over_changed = self.new_time_over.time() != self.initial_time_over
        
        self.button_create.setEnabled(
            has_title and 
            has_date and 
            time_start_changed and 
            time_over_changed
        )

    def sync_create_event(self):
        title = self.new_title.toPlainText()
        date = self.new_date.date().toPyDate()
        time_start = self.new_time_start.time().toPyTime()
        time_over = self.new_time_over.time().toPyTime()
        asyncio.create_task(self.create_event(title, date, time_start, time_over))
        self.new_title.clear()
        self.new_date.clear()
        self.new_time_start.clear()
        self.new_time_over.clear()

    async def create_event(self,title, date, time_start, time_over):
        await func.insert_mero(title, date, time_start, time_over)

    def sync_expot(self):
        asyncio.create_task(self.export())

    async def export(self):
        data = await func.get_mero(export=True)
        df = pd.DataFrame(data)
        df.to_csv("tasks.csv", index=False)  
        subprocess.call(['open', 'tasks.csv'])  

    def sync_on_date_selected(self):
        asyncio.create_task(self.on_date_selected())

    async def on_date_selected(self):
        selected_date = self.calendar.selectedDate().toPyDate()
        clear_layout(self.scroll_layout)
        self.scroll_layout.addStretch()
        mero = await func.get_mero(selected_date)
        for m in mero:
            self.add_work_widget(m["id"], m["title"], m["time_start"], m["time_stop"])

    def add_work_widget(self, id:int, title:str, time_start:datetime.time, time_over:datetime.time):
        """Добавляет новый виджет работы"""
        work_widget = WorkWidget(id, title, f"{time_start.strftime('%H:%M')}-{time_over.strftime('%H:%M')}")
        self.scroll_layout.insertWidget(0, work_widget)
    
    def clear_all_widgets(self):
        """Очищает все виджеты"""
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()


async def main():
    """Асинхронная главная функция"""
    await init_db()
    
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application interrupted")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        print("Application closed")