import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.data_viewer.viewer_window import ViewerWindow
from utils.data_utils.datasets.MSRA_TD500 import MSRA_TD500_dataset


def main():
    app = QApplication()
    main_win = ViewerWindow(DATASET)
    main_win.show()
    app.exec()


if __name__ == '__main__':
    DATASET_DIR = Path(
        '/home/pc0/projects/text_detection/data/images/MSRA_TD500')
    DATASET = MSRA_TD500_dataset(DATASET_DIR)
    main()
