from PyQt5 import QtWidgets
from gui import plotting as pg


class PlotDialog(QtWidgets.QDialog, pg.Ui_Dialog):
    def __init__(self, data):
        super(PlotDialog, self).__init__()
        self.setupUi(self)
        self.data = data
        self.check_data()

        # Init Data-Plot
        self.pw = self.plotwidget.canvas
        self.data_ax = self.pw.fig.add_subplot(111)

        max_val = 1
        for k in self.data.keys():
            if self.data[k] is not None:
                max_val = len(self.data[k])

        self.max_layers = max_val - 1

        self.init_slider()
        self.setup_triggers()

    def setup_triggers(self):
        self.txt_curr_layer.returnPressed.connect(self.update_slider)
        self.slider_layer.valueChanged.connect(self.update_label)
        self.but_layer_minus.clicked.connect(self.switch_layer)
        self.but_layer_plus.clicked.connect(self.switch_layer)
        self.cb_poly.clicked.connect(self.plot_data)
        self.cb_rest.clicked.connect(self.plot_data)
        self.cb_hatch.clicked.connect(self.plot_data)

    def init_slider(self):
        sli = self.slider_layer

        sli.setMinimum(0)
        sli.setMaximum(self.max_layers)

        sli.setValue(0)

        self.update_label()

    def update_label(self):
        curr_val = self.slider_layer.value()
        self.txt_curr_layer.setText(str(curr_val))
        self.plot_data()

    def update_slider(self):
        curr_val = int(self.txt_curr_layer.text())
        self.slider_layer.setValue(curr_val)
        self.plot_data()

    def switch_layer(self):
        sli = self.slider_layer
        curr_val = int(sli.value())

        if self.sender() == self.but_layer_plus:
            if curr_val < self.max_layers:
                sli.setValue(curr_val + 1)

        if self.sender() == self.but_layer_minus:
            if curr_val > 0:
                sli.setValue(curr_val - 1)

        self.update_label()

    def check_data(self):
        if self.data['hatches'] is None:
            self.cb_hatch.setEnabled(False)
        else:
            self.cb_hatch.setEnabled(True)
        if self.data['polylines'] is None:
            self.cb_poly.setEnabled(False)
        else:
            self.cb_poly.setEnabled(True)
        if self.data['rest'] is None:
            self.cb_rest.setEnabled(False)
        else:
            self.cb_rest.setEnabled(True)

    def plot_data(self):
        def plot_arrows(data, color='k', a=1.0):
            x = data[:, 0]
            y = data[:, 1]
            u = data[:, 2]
            v = data[:, 3]

            self.data_ax.quiver(x, y, u, v,
                                color=color,
                                angles='xy',
                                scale_units='xy',
                                scale=1,
                                width=0.005,
                                headwidth=5,
                                alpha=a
                                )
        # lösche die alten Daten
        self.data_ax.clear()

        cl = int(self.txt_curr_layer.text())
        if cl > self.max_layers:
            return
        if self.cb_poly.isChecked():
            plot_arrows(self.data['polylines'][cl], color='tab:red')
        if self.cb_hatch.isChecked():
            plot_arrows(self.data['hatches'][cl], color='k')
        if self.cb_rest.isChecked():
            plot_arrows(self.data['rest'][cl], color='tab:orange', a=0.1)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()

