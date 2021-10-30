from PyQt5 import QtWidgets
from gui import plotGUI as pg


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
            if self.data[k]:
                max_val = len(self.data[k][1])

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
        if self.data['hatches']:
            self.cb_hatch.setEnabled(True)
        else:
            self.cb_hatch.setEnabled(False)
        if self.data['polylines']:
            self.cb_poly.setEnabled(True)
        else:
            self.cb_poly.setEnabled(False)
        if self.data['rest']:
            self.cb_rest.setEnabled(True)
        else:
            self.cb_rest.setEnabled(False)

    def plot_data(self):
        def plot_arrows(ax, d, color='k', a=1.0):
            x = d[:, 0]
            y = d[:, 1]
            u = d[:, 2]
            v = d[:, 3]

            ax.quiver(x, y, u, v,
                      color=color,
                      angles='xy',
                      scale_units='xy',
                      scale=1,
                      width=0.005,
                      headwidth=5,
                      alpha=a
                      )
        # lösche die alten Daten
        pax = self.data_ax
        pax.clear()

        cl = int(self.txt_curr_layer.text())
        if cl > self.max_layers:
            return

        if self.cb_poly.isChecked():
            data = self.data['polylines'][1][cl]
            plot_arrows(pax, data, color='tab:red')
            pax.plot(data[0, 0], data[0, 1],
                     marker='o', ms=5, mec='tab:red', mfc='w', mew=2)
        if self.cb_hatch.isChecked():
            data = self.data['hatches'][1][cl]
            plot_arrows(pax, data, color='k')
            pax.plot(data[0, 0], data[0, 1],
                     marker='o', ms=5, mec='k', mfc='w', mew=2)
        if self.cb_rest.isChecked():
            plot_arrows(pax, self.data['rest'][1][cl], color='tab:orange', a=0.1)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()

