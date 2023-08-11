import sys
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.data_viewer.uic.ui_viewer import Ui_MainWindow


class ViewerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, dataset) -> None:
        super().__init__()
        self.setupUi(self)
        self.create_table()
        self.AddButton.clicked.connect(self.add_new_row)
        
        # self.fill_annotation_panel()

    def create_table(self):
        self.table = ViewerTable(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['x1', 'y1', 'x2', 'y2', 'language', 'word'])
        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.table_changed)
        # self.table.model()
        self.table.rowCountChanged()
        self.TableLayout.addWidget(self.table)

    def add_new_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem('1000'))
        self.table.setItem(row_count, 1, QTableWidgetItem('2000'))
        self.table.setItem(row_count, 2, QTableWidgetItem('3000'))
        self.table.setItem(row_count, 3, QTableWidgetItem('4000'))
        self.table.setItem(row_count, 4, QTableWidgetItem('english'))
        self.table.setItem(row_count, 5, QTableWidgetItem('aboba'))

    def table_changed(self):
        print('aboba')
        
    # def fill_annotation_panel(self, example: MSRA_TD500_example=0):
    #     # print(self.scrollAreaWidgetContents.)
    #     pass


class ViewerTable(QTableWidget):

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            row = self.currentRow()
            if row == -1:
                return
            self.removeRow(row)
        else:
            return super().keyPressEvent(event)
