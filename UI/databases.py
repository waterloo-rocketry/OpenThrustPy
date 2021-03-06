# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'databases.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DatabasesWindow(object):
    def setupUi(self, DatabasesWindow):
        DatabasesWindow.setObjectName("DatabasesWindow")
        DatabasesWindow.resize(420, 150)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DatabasesWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(DatabasesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonNosPres = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNosPres.sizePolicy().hasHeightForWidth())
        self.pushButtonNosPres.setSizePolicy(sizePolicy)
        self.pushButtonNosPres.setObjectName("pushButtonNosPres")
        self.gridLayout.addWidget(self.pushButtonNosPres, 3, 2, 1, 1)
        self.labelNosPres = QtWidgets.QLabel(self.centralwidget)
        self.labelNosPres.setObjectName("labelNosPres")
        self.gridLayout.addWidget(self.labelNosPres, 3, 0, 1, 1)
        self.labelRpaTable = QtWidgets.QLabel(self.centralwidget)
        self.labelRpaTable.setObjectName("labelRpaTable")
        self.gridLayout.addWidget(self.labelRpaTable, 0, 0, 1, 1)
        self.pushButtonRpaTable = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRpaTable.sizePolicy().hasHeightForWidth())
        self.pushButtonRpaTable.setSizePolicy(sizePolicy)
        self.pushButtonRpaTable.setObjectName("pushButtonRpaTable")
        self.gridLayout.addWidget(self.pushButtonRpaTable, 0, 2, 1, 1)
        self.lineEditNosPres = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditNosPres.sizePolicy().hasHeightForWidth())
        self.lineEditNosPres.setSizePolicy(sizePolicy)
        self.lineEditNosPres.setObjectName("lineEditNosPres")
        self.gridLayout.addWidget(self.lineEditNosPres, 3, 1, 1, 1)
        self.lineEditRpaTable = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRpaTable.sizePolicy().hasHeightForWidth())
        self.lineEditRpaTable.setSizePolicy(sizePolicy)
        self.lineEditRpaTable.setObjectName("lineEditRpaTable")
        self.gridLayout.addWidget(self.lineEditRpaTable, 0, 1, 1, 1)
        self.labelNosTemp = QtWidgets.QLabel(self.centralwidget)
        self.labelNosTemp.setObjectName("labelNosTemp")
        self.gridLayout.addWidget(self.labelNosTemp, 4, 0, 1, 1)
        self.lineEditNosTemp = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditNosTemp.sizePolicy().hasHeightForWidth())
        self.lineEditNosTemp.setSizePolicy(sizePolicy)
        self.lineEditNosTemp.setObjectName("lineEditNosTemp")
        self.gridLayout.addWidget(self.lineEditNosTemp, 4, 1, 1, 1)
        self.pushButtonNosTemp = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNosTemp.sizePolicy().hasHeightForWidth())
        self.pushButtonNosTemp.setSizePolicy(sizePolicy)
        self.pushButtonNosTemp.setObjectName("pushButtonNosTemp")
        self.gridLayout.addWidget(self.pushButtonNosTemp, 4, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.SaveAll)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 2, 1, 1)
        DatabasesWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DatabasesWindow)
        self.statusbar.setObjectName("statusbar")
        DatabasesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DatabasesWindow)
        QtCore.QMetaObject.connectSlotsByName(DatabasesWindow)

    def retranslateUi(self, DatabasesWindow):
        _translate = QtCore.QCoreApplication.translate
        DatabasesWindow.setWindowTitle(_translate("DatabasesWindow", "Databases"))
        self.pushButtonNosPres.setText(_translate("DatabasesWindow", "Open"))
        self.labelNosPres.setText(_translate("DatabasesWindow", "NOs Data, Pressure Sorted"))
        self.labelRpaTable.setText(_translate("DatabasesWindow", "RPA Table"))
        self.pushButtonRpaTable.setText(_translate("DatabasesWindow", "Open"))
        self.labelNosTemp.setText(_translate("DatabasesWindow", "NOs Data, Temperature Sorted"))
        self.pushButtonNosTemp.setText(_translate("DatabasesWindow", "Open"))

