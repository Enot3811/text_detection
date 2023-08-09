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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(854, 452)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.picture_box = QLabel(self.centralwidget)
        self.picture_box.setObjectName(u"picture_box")
        self.picture_box.setGeometry(QRect(10, 10, 531, 351))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 380, 89, 25))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(450, 380, 89, 25))
        self.idx_lineEdit = QLineEdit(self.centralwidget)
        self.idx_lineEdit.setObjectName(u"idx_lineEdit")
        self.idx_lineEdit.setGeometry(QRect(300, 380, 71, 25))
        self.idx_lineEdit.setReadOnly(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(570, 10, 51, 17))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(650, 10, 21, 17))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(700, 10, 21, 17))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(750, 10, 21, 17))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(800, 10, 21, 17))
        self.annotations_scroll_panel = QScrollArea(self.centralwidget)
        self.annotations_scroll_panel.setObjectName(u"annotations_scroll_panel")
        self.annotations_scroll_panel.setGeometry(QRect(550, 30, 291, 371))
        self.annotations_scroll_panel.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 289, 369))
        self.lineEdit_4 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(240, 10, 41, 25))
        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(10, 10, 71, 23))
        self.lineEdit_3 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(190, 10, 41, 25))
        self.lineEdit_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 10, 41, 25))
        self.lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(90, 10, 41, 25))
        self.annotations_scroll_panel.setWidget(self.scrollAreaWidgetContents)
        self.set_comboBox = QComboBox(self.centralwidget)
        self.set_comboBox.setObjectName(u"set_comboBox")
        self.set_comboBox.setGeometry(QRect(190, 380, 81, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 854, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.picture_box.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0430\u0434", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043f\u0435\u0440\u0451\u0434", None))
        self.idx_lineEdit.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Include", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"X1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Y1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"X2", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Y2", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"1111", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"11111", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"1111", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"1111", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"1111", None))
    # retranslateUi

