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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1113, 450)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.picture_box = QLabel(self.centralwidget)
        self.picture_box.setObjectName(u"picture_box")
        self.picture_box.setGeometry(QRect(10, 10, 531, 351))
        self.BackButton = QPushButton(self.centralwidget)
        self.BackButton.setObjectName(u"BackButton")
        self.BackButton.setGeometry(QRect(10, 380, 89, 25))
        self.NextButton = QPushButton(self.centralwidget)
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setGeometry(QRect(450, 380, 89, 25))
        self.IdxLineEdit = QLineEdit(self.centralwidget)
        self.IdxLineEdit.setObjectName(u"IdxLineEdit")
        self.IdxLineEdit.setGeometry(QRect(300, 380, 71, 25))
        self.IdxLineEdit.setReadOnly(True)
        self.SetComboBox = QComboBox(self.centralwidget)
        self.SetComboBox.setObjectName(u"SetComboBox")
        self.SetComboBox.setGeometry(QRect(190, 380, 81, 25))
        self.AddButton = QPushButton(self.centralwidget)
        self.AddButton.setObjectName(u"AddButton")
        self.AddButton.setGeometry(QRect(810, 370, 89, 25))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(560, 10, 551, 351))
        self.TableLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.TableLayout.setSpacing(0)
        self.TableLayout.setObjectName(u"TableLayout")
        self.TableLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1113, 22))
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
        self.BackButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0430\u0434", None))
        self.NextButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043f\u0435\u0440\u0451\u0434", None))
        self.IdxLineEdit.setText("")
        self.AddButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

