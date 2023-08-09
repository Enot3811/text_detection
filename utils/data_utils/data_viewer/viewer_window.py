import sys
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QCheckBox, QLineEdit

sys.path.append(Path(__file__).parents[1])
from utils.data_utils.data_viewer.uic.ui_viewer import Ui_MainWindow
from utils.data_utils.datasets.MSRA_TD500 import (
    MSRA_TD500_dataset, MSRA_TD500_example, MSRA_TD500_annotation)


class ViewerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, dataset) -> None:
        super().__init__()
        self.setupUi(self)

        self.check_x = 10
        self.check_y = 10
        self.x1_x = 90
        self.x1_y = 10
        self.y1_x = 140
        self.y1_y = 10
        self.x2_x = 190
        self.x2_y = 10
        self.y2_x = 240
        self.y2_y = 10
        self.fill_annotation_panel()

    def fill_annotation_panel(self, example: MSRA_TD500_example=0):
        print(self.scrollAreaWidgetContents.)

