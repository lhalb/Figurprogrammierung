from PyQt5 import QtGui, QtWidgets
from gui import plotting as pg


class PlotDialog(QtWidgets.QDialog, pg.Ui_Dialog):
    def __init__(self, data):
        super(PlotDialog, self).__init__()
        self.setupUi(self)
        self.data = data
