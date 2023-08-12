import sys
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.data_viewer.uic.ui_viewer import Ui_MainWindow
from utils.data_utils.datasets import (
    ICDAR2003_dataset, MSRA_TD500_dataset, NEOCR_dataset, SVT_dataset)


# Available datasets and its directories names
DATASETS = {
    'ICDAR2003': ICDAR2003_dataset,
    'MSRA_TD500': MSRA_TD500_dataset,
    'NEOCR': NEOCR_dataset,
    'StreetViewText': SVT_dataset
}

# TODO
# pythonguis.com/tutorials/pyqt-actions-toolbars-menus/
class ViewerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.create_table()
        self.AddButton.clicked.connect(self.add_new_row)
        self.DsetOpener.
        
        # self.fill_annotation_panel()

    def create_table(self):
        self.table = ViewerTable(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['x1', 'y1', 'x2', 'y2', 'language', 'word'])
        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.table_changed)
        self.TableLayout.addWidget(self.table)

    def add_new_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem('0'))
        self.table.setItem(row_count, 1, QTableWidgetItem('0'))
        self.table.setItem(row_count, 2, QTableWidgetItem('1'))
        self.table.setItem(row_count, 3, QTableWidgetItem('1'))
        self.table.setItem(row_count, 4, QTableWidgetItem('english'))
        self.table.setItem(row_count, 5, QTableWidgetItem('word'))

    def table_changed(self):
        # If event is fired when row is added
        if self.table.row_adding:
            return
        row_idx = self.table.currentRow()
        x1 = int(self.table.item(row_idx, 0).text())
        y1 = int(self.table.item(row_idx, 1).text())
        x2 = int(self.table.item(row_idx, 2).text())
        y2 = int(self.table.item(row_idx, 3).text())
        language = self.table.item(row_idx, 4).text()
        word = self.table.item(row_idx, 5).text()

        row = [x1, y1, x2, y2, language, word]

        # TODO сюда вызов отрисовки картинки
        print(row)

        
    # def fill_annotation_panel(self, example: MSRA_TD500_example=0):
    #     # print(self.scrollAreaWidgetContents.)
    #     pass


class ViewerTable(QTableWidget):

    def __init__(self, *args, **kwargs):
        self.row_adding: bool = False
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            row = self.currentRow()
            if row == -1:
                return
            self.removeRow(row)
        else:
            return super().keyPressEvent(event)
        
    def setItem(self, row: int, column: int, item: QTableWidgetItem) -> None:
        # setItem is used only when new row is adding
        # So row_adding flag is needed to disarm itemChanged event
        # if it is fired up during new row adding
        self.row_adding = True
        super().setItem(row, column, item)
        self.row_adding = False
