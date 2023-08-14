# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewer.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1113, 450)
        self.DsetOpener = QAction(MainWindow)
        self.DsetOpener.setObjectName(u"DsetOpener")
        self.action_open_dset = QAction(MainWindow)
        self.action_open_dset.setObjectName(u"action_open_dset")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.picture_box = QLabel(self.centralwidget)
        self.picture_box.setObjectName(u"picture_box")
        self.picture_box.setGeometry(QRect(10, 10, 531, 351))
        self.picture_box.setPixmap(QPixmap(u"utils/data_utils/data_viewer/resources/default_img.jpg"))
        self.picture_box.setScaledContents(True)
        self.BackButton = QPushButton(self.centralwidget)
        self.BackButton.setObjectName(u"BackButton")
        self.BackButton.setEnabled(False)
        self.BackButton.setGeometry(QRect(10, 380, 89, 25))
        self.NextButton = QPushButton(self.centralwidget)
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setEnabled(False)
        self.NextButton.setGeometry(QRect(450, 380, 89, 25))
        self.IdxLineEdit = QLineEdit(self.centralwidget)
        self.IdxLineEdit.setObjectName(u"IdxLineEdit")
        self.IdxLineEdit.setEnabled(False)
        self.IdxLineEdit.setGeometry(QRect(300, 380, 71, 25))
        self.IdxLineEdit.setReadOnly(True)
        self.SetComboBox = QComboBox(self.centralwidget)
        self.SetComboBox.setObjectName(u"SetComboBox")
        self.SetComboBox.setEnabled(False)
        self.SetComboBox.setGeometry(QRect(190, 380, 81, 25))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(560, 10, 551, 351))
        self.table_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.table_layout.setSpacing(0)
        self.table_layout.setObjectName(u"table_layout")
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(670, 370, 331, 27))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.save_btn = QPushButton(self.widget)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.save_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.add_btn = QPushButton(self.widget)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.add_btn)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1113, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_open_dset)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.DsetOpener.setText(QCoreApplication.translate("MainWindow", u"Open dataset", None))
        self.action_open_dset.setText(QCoreApplication.translate("MainWindow", u"Open dataset", None))
        self.picture_box.setText("")
        self.BackButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.NextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.IdxLineEdit.setText("")
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Save changes", None))
        self.add_btn.setText(QCoreApplication.translate("MainWindow", u"Add annotation", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

