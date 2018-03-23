# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1189, 672)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 430, 1161, 181))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(50, 40, 194, 122))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.algorithm_selection = QtWidgets.QComboBox(self.widget)
        self.algorithm_selection.setObjectName("algorithm_selection")
        self.algorithm_selection.addItem("")
        self.algorithm_selection.addItem("")
        self.horizontalLayout_2.addWidget(self.algorithm_selection)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_2)
        self.detect_features_btn = QtWidgets.QPushButton(self.widget)
        self.detect_features_btn.setObjectName("detect_features_btn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.detect_features_btn)
        self.refine_btn = QtWidgets.QPushButton(self.widget)
        self.refine_btn.setObjectName("refine_btn")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.refine_btn)
        self.select_keypoints_btn = QtWidgets.QPushButton(self.widget)
        self.select_keypoints_btn.setObjectName("select_keypoints_btn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.select_keypoints_btn)
        self.widget1 = QtWidgets.QWidget(self.centralWidget)
        self.widget1.setGeometry(QtCore.QRect(22, 2, 1151, 431))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reference_image_view = GraphicsView(self.widget1)
        self.reference_image_view.setObjectName("reference_image_view")
        self.horizontalLayout.addWidget(self.reference_image_view)
        self.offset_image_view = GraphicsView(self.widget1)
        self.offset_image_view.setObjectName("offset_image_view")
        self.horizontalLayout.addWidget(self.offset_image_view)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1189, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Image Alignment Toolbox"))
        self.label.setText(_translate("MainWindow", "Features"))
        self.algorithm_selection.setItemText(0, _translate("MainWindow", "BRIEF"))
        self.algorithm_selection.setItemText(1, _translate("MainWindow", "CENSURE"))
        self.detect_features_btn.setText(_translate("MainWindow", "Detect Features"))
        self.refine_btn.setText(_translate("MainWindow", "Refine"))
        self.select_keypoints_btn.setText(_translate("MainWindow", "Manually Select Keypoints"))

from pyqtgraph import GraphicsView
