# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mq/Projects/workover/design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1010, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plot = MplWidget(self.centralwidget)
        self.plot.setGeometry(QtCore.QRect(0, 0, 681, 381))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(680, 0, 121, 121))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.per_all_rb = QtWidgets.QRadioButton(self.groupBox)
        self.per_all_rb.setGeometry(QtCore.QRect(10, 30, 121, 20))
        self.per_all_rb.setChecked(True)
        self.per_all_rb.setObjectName("per_all_rb")
        self.per_month_rb = QtWidgets.QRadioButton(self.groupBox)
        self.per_month_rb.setGeometry(QtCore.QRect(10, 90, 98, 20))
        self.per_month_rb.setObjectName("per_month_rb")
        self.per_week_rb = QtWidgets.QRadioButton(self.groupBox)
        self.per_week_rb.setGeometry(QtCore.QRect(10, 60, 98, 20))
        self.per_week_rb.setObjectName("per_week_rb")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(680, 150, 321, 211))
        self.calendarWidget.setObjectName("calendarWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(810, 20, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(810, 50, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(810, 110, 91, 16))
        self.label_3.setObjectName("label_3")
        self.required_label = QtWidgets.QLabel(self.centralwidget)
        self.required_label.setGeometry(QtCore.QRect(920, 20, 57, 15))
        self.required_label.setText("")
        self.required_label.setObjectName("required_label")
        self.done_label = QtWidgets.QLabel(self.centralwidget)
        self.done_label.setGeometry(QtCore.QRect(920, 50, 57, 15))
        self.done_label.setText("")
        self.done_label.setObjectName("done_label")
        self.workover_label = QtWidgets.QLabel(self.centralwidget)
        self.workover_label.setGeometry(QtCore.QRect(920, 110, 57, 15))
        self.workover_label.setText("")
        self.workover_label.setObjectName("workover_label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(810, 80, 81, 16))
        self.label_4.setObjectName("label_4")
        self.done_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.done_label_2.setGeometry(QtCore.QRect(920, 80, 57, 15))
        self.done_label_2.setText("")
        self.done_label_2.setObjectName("done_label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1010, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Workover"))
        self.per_all_rb.setText(_translate("MainWindow", "За всё время"))
        self.per_month_rb.setText(_translate("MainWindow", "За месяц"))
        self.per_week_rb.setText(_translate("MainWindow", "За неделю"))
        self.label.setText(_translate("MainWindow", "Требовалось:"))
        self.label_2.setText(_translate("MainWindow", "Выполнено:"))
        self.label_3.setText(_translate("MainWindow", "Переработка:"))
        self.label_4.setText(_translate("MainWindow", "За сутки:"))

from mplwidget import MplWidget
