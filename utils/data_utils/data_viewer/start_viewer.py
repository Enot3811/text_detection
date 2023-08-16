import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

sys.path.append(str(Path(__file__).parents[3]))
from utils.data_utils.data_viewer.viewer_modules import ViewerWindow


def main():
    app = QApplication()
    main_win = ViewerWindow()
    main_win.show()
    app.exec()


if __name__ == '__main__':
    main()
