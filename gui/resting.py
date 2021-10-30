from PyQt5 import QtWidgets
from gui import restGUI as rG
from lib import cli_converter as cli
from gui import boxes as BOX


class RestDialog(QtWidgets.QDialog, rG.Ui_Dialog):
    def __init__(self, data, para, layers=None):
        super(RestDialog, self).__init__()
        self.db = data
        self.para = para
        if layers is not None:
            self.layers = layers
        else:
            self.layers = self.db.layers
        self.setupUi(self)

    def clear_rast(self):
        self.but_rast.setEnabled(True)
        self.but_clear_rast.setEnabled(False)
        setattr(self.db, 'rp_points', None)
        setattr(self.db, 'rp_arrows', None)

    def add_rest_layers(self):
        #
        proc_layers = self.layers
        #
        if not proc_layers:
            return

        v_rast = float(self.txt_v_rast.text().replace(',', '.'))
        t_rast = float(self.txt_t_rast.text().replace(',', '.'))
        r_min = float(self.txt_r_min.text().replace(',', '.'))
        r_max = float(self.txt_r_max.text().replace(',', '.'))
        acc = int(self.txt_accuracy.text())

        setattr(self.db, 'rp_points', [None]*len(proc_layers))
        setattr(self.db, 'rp_arrows', [None]*len(proc_layers))

        for lay in proc_layers:
            hatch = self.db.hatchlist[lay]
            d = cli.get_outbox(hatch)
            rp_points, rp_arrows = cli.make_rest_positions(d,
                                                           v=v_rast,
                                                           time=t_rast,
                                                           rp_min=r_min,
                                                           rp_max=r_max,
                                                           exact=acc)

            self.db.rp_arrows[lay] = rp_arrows
            self.db.rp_points[lay] = rp_points

            self.but_rast.setEnabled(False)
            self.but_clear_rast.setEnabled(True)

            BOX.show_msg_box('Rastfiguren erfolgreich erzeugt')
