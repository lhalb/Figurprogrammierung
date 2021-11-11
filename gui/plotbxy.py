from PyQt5 import QtWidgets
import gui.boxes as BOX
import gui.plotbxyGUI as pG
from lib import cli_converter as cli
from lib import bxy_converter as bxy
import random


class XyPlot(QtWidgets.QDialog, pG.Ui_Dialog):
    def __init__(self):
        super(XyPlot, self).__init__()
        self.setupUi(self)
        self.call_buttons()

    def call_buttons(self):
        self.but_load_files.clicked.connect(self.open_files)
        self.but_plot.clicked.connect(self.plot_files)
        self.but_del_entry.clicked.connect(self.remove_items)

    def remove_items(self):
        lw = self.lst_files
        sel_items = lw.selectedItems()
        if not sel_items:
            return
        for item in sel_items:
            lw.takeItem(lw.row(item))


    def open_files(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Wähle die .bxy Dateien aus.', '',
                                                       'Figurdateien (*.bxy *.b00)')[0]
        if not files:
            return

        lw = self.lst_files
        lw.addItems(files)
        BOX.show_info_box('Dateien erfolgreich geladen.')

    def plot_files(self):
        lw = self.lst_files
        files = [str(lw.item(i).text()) for i in range(lw.count())]

        cli.init_plot(unit='V', x_lim=(-1, 1), y_lim=(-1, 1))
        if len(files) > 1:
            alpha = 0.5
        else:
            alpha = 1.0

        for f in files:
            bxy_data = bxy.convert_bxy(f)

            r = random.random()
            b = random.random()
            g = random.random()
            color = (r, g, b)
            cli.plot_arrows(bxy_data, color=color, a=alpha)

        cli.show_plot()

