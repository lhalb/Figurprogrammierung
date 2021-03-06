# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\buildGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(781, 541)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.but_load_folders = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.but_load_folders.sizePolicy().hasHeightForWidth())
        self.but_load_folders.setSizePolicy(sizePolicy)
        self.but_load_folders.setMinimumSize(QtCore.QSize(50, 50))
        self.but_load_folders.setMaximumSize(QtCore.QSize(60, 60))
        self.but_load_folders.setAutoDefault(False)
        self.but_load_folders.setObjectName("but_load_folders")
        self.horizontalLayout_3.addWidget(self.but_load_folders)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_open_folders = QtWidgets.QTableWidget(self.groupBox)
        self.tab_open_folders.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked)
        self.tab_open_folders.setDragEnabled(True)
        self.tab_open_folders.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tab_open_folders.setAlternatingRowColors(True)
        self.tab_open_folders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tab_open_folders.setCornerButtonEnabled(True)
        self.tab_open_folders.setRowCount(0)
        self.tab_open_folders.setColumnCount(9)
        self.tab_open_folders.setObjectName("tab_open_folders")
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tab_open_folders.setHorizontalHeaderItem(8, item)
        self.tab_open_folders.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_open_folders.horizontalHeader().setDefaultSectionSize(50)
        self.tab_open_folders.horizontalHeader().setHighlightSections(False)
        self.tab_open_folders.horizontalHeader().setMinimumSectionSize(25)
        self.tab_open_folders.horizontalHeader().setSortIndicatorShown(True)
        self.tab_open_folders.horizontalHeader().setStretchLastSection(True)
        self.tab_open_folders.verticalHeader().setVisible(False)
        self.tab_open_folders.verticalHeader().setCascadingSectionResizes(False)
        self.tab_open_folders.verticalHeader().setDefaultSectionSize(25)
        self.tab_open_folders.verticalHeader().setHighlightSections(False)
        self.tab_open_folders.verticalHeader().setSortIndicatorShown(False)
        self.horizontalLayout.addWidget(self.tab_open_folders)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_user_order = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_user_order.setFrame(False)
        self.txt_user_order.setObjectName("txt_user_order")
        self.verticalLayout.addWidget(self.txt_user_order)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cb_hatch_first = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_hatch_first.setObjectName("cb_hatch_first")
        self.horizontalLayout_5.addWidget(self.cb_hatch_first)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.txt_destination = QtWidgets.QLineEdit(Dialog)
        self.txt_destination.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_destination.setFont(font)
        self.txt_destination.setObjectName("txt_destination")
        self.horizontalLayout_4.addWidget(self.txt_destination)
        self.but_destination = QtWidgets.QToolButton(Dialog)
        self.but_destination.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.but_destination.setAutoRaise(False)
        self.but_destination.setArrowType(QtCore.Qt.NoArrow)
        self.but_destination.setObjectName("but_destination")
        self.horizontalLayout_4.addWidget(self.but_destination)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.cb_oldfilename = QtWidgets.QCheckBox(Dialog)
        self.cb_oldfilename.setObjectName("cb_oldfilename")
        self.horizontalLayout_2.addWidget(self.cb_oldfilename)
        self.but_generate_build_job = QtWidgets.QPushButton(Dialog)
        self.but_generate_build_job.setMinimumSize(QtCore.QSize(120, 60))
        self.but_generate_build_job.setAutoDefault(False)
        self.but_generate_build_job.setDefault(False)
        self.but_generate_build_job.setObjectName("but_generate_build_job")
        self.horizontalLayout_2.addWidget(self.but_generate_build_job)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Generate Build Job"))
        self.but_load_folders.setToolTip(_translate("Dialog", "(Strg + O)"))
        self.but_load_folders.setText(_translate("Dialog", "Load\n"
"Folders"))
        self.but_load_folders.setShortcut(_translate("Dialog", "Ctrl+O"))
        self.groupBox.setTitle(_translate("Dialog", "Folders"))
        self.tab_open_folders.setSortingEnabled(True)
        item = self.tab_open_folders.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Pos."))
        item.setToolTip(_translate("Dialog", "Position (f??r Wahl der Reihenfolge)"))
        item = self.tab_open_folders.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "PVZ-C"))
        item.setToolTip(_translate("Dialog", "Punktverz??gerung Kontur [ns]"))
        item = self.tab_open_folders.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "IB-C"))
        item.setToolTip(_translate("Dialog", "Strahlstrom Kontur [mA]"))
        item = self.tab_open_folders.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "IL-C"))
        item.setToolTip(_translate("Dialog", "Linsenstrom Kontur [mA]"))
        item = self.tab_open_folders.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "PVZ-H"))
        item.setToolTip(_translate("Dialog", "Punktverz??gerung Hatch [ns]"))
        item = self.tab_open_folders.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "IB-H"))
        item.setToolTip(_translate("Dialog", "Strahlstrom Hatch [mA]"))
        item = self.tab_open_folders.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "IL-H"))
        item.setToolTip(_translate("Dialog", "Linsenstrom Hatch [mA]"))
        item = self.tab_open_folders.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "SIZE"))
        item.setToolTip(_translate("Dialog", "Arbeitsfeldgr????e [mm]"))
        item = self.tab_open_folders.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "Name"))
        item.setToolTip(_translate("Dialog", "Pfad zur Datei"))
        self.groupBox_2.setTitle(_translate("Dialog", "Order Settings"))
        self.cb_hatch_first.setToolTip(_translate("Dialog", "Bearbeitet die Dateien so, dass Hatches VOR Konturen geschmolzen werden"))
        self.cb_hatch_first.setText(_translate("Dialog", "Hatches first"))
        self.label.setText(_translate("Dialog", "Ziel"))
        self.but_destination.setToolTip(_translate("Dialog", "(Strg + S)"))
        self.but_destination.setText(_translate("Dialog", "..."))
        self.but_destination.setShortcut(_translate("Dialog", "Ctrl+S"))
        self.cb_oldfilename.setToolTip(_translate("Dialog", "Erzeugt .b00 statt .bxy Dateien (f??r alte MMC-Software)"))
        self.cb_oldfilename.setText(_translate("Dialog", "Old Filename"))
        self.but_generate_build_job.setToolTip(_translate("Dialog", "(Strg + Alt + G)"))
        self.but_generate_build_job.setText(_translate("Dialog", "Generate Build Job"))
        self.but_generate_build_job.setShortcut(_translate("Dialog", "Ctrl+Alt+G"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
