# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/simsettings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(338, 74)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.spinBoxOxMass = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinBoxOxMass.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxOxMass.setDecimals(3)
        self.spinBoxOxMass.setMaximum(1000.0)
        self.spinBoxOxMass.setSingleStep(0.05)
        self.spinBoxOxMass.setObjectName("spinBoxOxMass")
        self.verticalLayout_3.addWidget(self.spinBoxOxMass)
        self.spinBoxTankTemp = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinBoxTankTemp.setDecimals(3)
        self.spinBoxTankTemp.setMinimum(-90.82)
        self.spinBoxTankTemp.setMaximum(36.37)
        self.spinBoxTankTemp.setObjectName("spinBoxTankTemp")
        self.verticalLayout_3.addWidget(self.spinBoxTankTemp)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.buttonBox.rejected.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulation Settings"))
        self.label.setText(_translate("MainWindow", "Oxidizer Mass (kg)"))
        self.label_2.setText(_translate("MainWindow", "Tank Temperature (°C)"))

