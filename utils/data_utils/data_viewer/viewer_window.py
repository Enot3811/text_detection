import sys
from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QImage, QPixmap
from numpy.typing import NDArray

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.data_viewer.uic.ui_viewer import Ui_MainWindow
from utils.data_utils.datasets import datasets, BaseAnnotation, BaseDataset


class ViewerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.create_table()
        self.add_btn.clicked.connect(self.add_new_row)
        self.action_open_dset.triggered.connect(self.load_dataset)

        self.dset: BaseDataset = None
        self.current_set: str = None
        self.current_idx: int = None

    def create_table(self):
        self.annots_table = ViewerTable(self)
        self.annots_table.setColumnCount(6)
        self.annots_table.setHorizontalHeaderLabels(
            ['x1', 'y1', 'x2', 'y2', 'language', 'word'])
        self.annots_table.resizeColumnsToContents()
        self.annots_table.itemChanged.connect(self.table_changed)
        self.table_layout.addWidget(self.annots_table)

    def add_new_row(self, annotation: Optional[BaseAnnotation] = None):
        if annotation:
            x1 = str(annotation.x1)
            y1 = str(annotation.y1)
            x2 = str(annotation.x2)
            y2 = str(annotation.y2)
            language = annotation.language
            word = annotation.word
        else:
            x1 = '0'
            y1 = '0'
            x2 = '1'
            y2 = '1'
            language = 'english'
            word = 'word'
        row_count = self.annots_table.rowCount()
        self.annots_table.insertRow(row_count)
        self.annots_table.setItem(row_count, 0, QTableWidgetItem(x1))
        self.annots_table.setItem(row_count, 1, QTableWidgetItem(y1))
        self.annots_table.setItem(row_count, 2, QTableWidgetItem(x2))
        self.annots_table.setItem(row_count, 3, QTableWidgetItem(y2))
        self.annots_table.setItem(row_count, 4, QTableWidgetItem(language))
        self.annots_table.setItem(row_count, 5, QTableWidgetItem(word))

    def enable_controls(self):
        self.NextButton.setEnabled(True)
        self.BackButton.setEnabled(True)
        self.SetComboBox.setEnabled(True)
        self.IdxLineEdit.setEnabled(True)
        self.add_btn.setEnabled(True)

    def table_changed(self):
        # If event is fired when row is added
        if self.annots_table.row_adding:
            return
        row_idx = self.annots_table.currentRow()
        x1 = int(self.annots_table.item(row_idx, 0).text())
        y1 = int(self.annots_table.item(row_idx, 1).text())
        x2 = int(self.annots_table.item(row_idx, 2).text())
        y2 = int(self.annots_table.item(row_idx, 3).text())
        language = self.annots_table.item(row_idx, 4).text()
        word = self.annots_table.item(row_idx, 5).text()

        row = [x1, y1, x2, y2, language, word]

        # TODO сюда вызов отрисовки картинки
        print(row)

    def show_image(self, img: NDArray):
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        q_img = QImage(
            img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.picture_box.setPixmap(QPixmap(q_img))

    def show_annotations(self, annots: List[BaseAnnotation]):
        self.annots_table.clear()
        for annot in annots:
            self.add_new_row(annot)

    def load_dataset(self):
        dset_pth = QFileDialog.getExistingDirectory(
            self, 'Select dataset directory')
        if dset_pth == '':
            return
        else:
            dset_pth = Path(dset_pth)
        self.dset = datasets[dset_pth.name](dset_pth)
        self.current_set = 'train'
        self.current_idx = 0
        self.enable_controls()
        self.load_sample()

    def load_sample(self):
        sample = self.dset[self.current_set][self.current_idx]
        img_to_show = sample.get_image_with_bboxes()
        annots = sample.get_annotations()
        self.show_image(img_to_show)
        self.show_annotations(annots)


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
