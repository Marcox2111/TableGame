# Form implementation generated from reading ui file 'hand.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Hand(object):
    def setupUi(self, Hand):
        Hand.setObjectName("Hand")
        Hand.resize(500, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Hand)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 481, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Hand)
        QtCore.QMetaObject.connectSlotsByName(Hand)

    def retranslateUi(self, Hand):
        _translate = QtCore.QCoreApplication.translate
        Hand.setWindowTitle(_translate("Hand", "Hand"))
        self.pushButton.setText(_translate("Hand", "Draw"))
