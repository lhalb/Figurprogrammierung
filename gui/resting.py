from PyQt5 import QtWidgets, QtGui
from gui import restGUI as rG
from lib import cli_converter as cli
from gui import boxes as BOX
from time import time


class RestDialog(QtWidgets.QDialog, rG.Ui_Dialog):
    def __init__(self, data, layers=None):
        super(RestDialog, self).__init__()
        self.data = data
        if layers is not None:
            self.layers = layers
        else:
            self.layers = range(self.data['max_layers'])
        self.setupUi(self)
        self.check_for_rest()

        self.setup_triggers()

        self.progressBar.hide()
        self.resize_dialog()

    def setup_triggers(self):
        self.but_clear_rast.clicked.connect(self.clear_rast)
        self.but_rast.clicked.connect(self.add_rest_layers)

    def clear_rast(self):
        self.data['rest'] = [None, None]
        self.check_for_rest()

    def add_rest_layers(self):
        #
        proc_layers = self.layers
        #
        if not proc_layers:
            return

        critical_number_of_layers = 30
        if len(proc_layers) > critical_number_of_layers:
            ret_val = BOX.show_msg_box(f'Es sind mehr als {critical_number_of_layers} ausgewählt.\n'
                                       f'Die Berechnung wird ggf. länger dauern.\n'
                                       f'Fortfahren?')
            if not ret_val:
                return

        self.init_progress_bar(proc_layers)
        self.resize_dialog()

        v_rast = float(self.txt_v_rast.text().replace(',', '.'))
        t_rast = float(self.txt_t_rast.text().replace(',', '.'))
        r_min = float(self.txt_r_min.text().replace(',', '.'))
        r_max = float(self.txt_r_max.text().replace(',', '.'))
        acc = int(self.txt_accuracy.text())

        self.data['rest'] = [[None]*len(proc_layers), [None]*len(proc_layers)]

        count = 0
        t1 = time()
        for lay in proc_layers:
            d = cli.get_outbox(self.data['hatches'][0][lay])
            rp_points, rp_arrows = cli.make_rest_positions(d,
                                                           v=v_rast,
                                                           time=t_rast,
                                                           rp_min=r_min,
                                                           rp_max=r_max,
                                                           exact=acc)

            self.data['rest'][0][lay] = rp_points
            self.data['rest'][1][lay] = rp_arrows

            count += 1
            self.progressBar.setValue(count)
        t2 = time()
        dt = t2 - t1
        self.check_for_rest()
        self.progressBar.hide()
        self.resize_dialog()

        BOX.show_msg_box(f'Rastfiguren erfolgreich erzeugt\n\nZeit:{dt:.2f}s')

    def check_for_rest(self):
        on_icon = QtGui.QIcon(":/img/img/green_light.png")
        off_icon = QtGui.QIcon(":/img/img/red_light.png")
        if any(self.data['rest']):
            self.info_rp.setIcon(on_icon)
            self.but_clear_rast.setEnabled(True)
        else:
            self.info_rp.setIcon(off_icon)
            self.but_clear_rast.setEnabled(False)

    def resize_dialog(self):
        self.resize(self.sizeHint().width(), self.sizeHint().height())

    def init_progress_bar(self, pl):
        max_val = len(pl)
        pb = self.progressBar
        pb.setValue(0)
        pb.setMinimum(0)
        pb.setMaximum(max_val)

        pb.show()

