'''
Autor: Halbauer
Date: 06.02.2019

Template zum Laden eines QT5 Fensters mit Tastaturkürzeln und Triggern

Erstellung des Layouts mit QT-Designer wird angenommen
Hierfür im Vorfeld .ui Datei in .py umwandlen und im gleichen VZ wie Template.py ablegen
Code für Umwandlung:
    pyuic5 -x template.ui -o template.py

'''

from PyQt5 import QtWidgets
from gui import startGUI  # Hier den Namen der UI-Datei angeben
from gui import boxes as BOX
from gui import plotUI
import os
from lib import cli_converter as cli
import numpy as np
from lib import config as cf
from lib import bxy_converter as bxy
from lib.Database import DataBase


# in der Klasse muss noch einmal die Klasse des Templates übergeben werden,
# da sonst die Zuweisung der Trigger nicht funktioniert.
class MyApp(QtWidgets.QMainWindow, startGUI.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setup_triggers()  # lade Events für Buttons
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(0, False)
        self.but_clear_rast.setEnabled(False)

        self.db = DataBase()

    def setup_triggers(self):
        # Aktionen
        self.action_ffnen.triggered.connect(self.file_open)

        # Buttons
        self.but_open.clicked.connect(self.file_open)
        self.but_conv_bxy.clicked.connect(self.plot_bxy)
        self.but_outname.clicked.connect(self.save_destination)
        self.but_save_plot_folder.clicked.connect(self.save_destination)
        self.but_save_vec_folder.clicked.connect(self.save_destination)
        self.but_clear_rast.clicked.connect(self.clear_rast)
        self.but_rast.clicked.connect(self.add_rest_layers)
        # self.but_plot.clicked.connect(self.plot_layers)
        self.but_plot.clicked.connect(self.open_plot_dialog)
        self.but_convert_cli.clicked.connect(self.save_vector_figures)

        self.but_debug.clicked.connect(self.debug)

    def get_proc_layers(self):
        if self.txt_layer.text() == 'all':
            proc_layers = range(self.db.layers)
        else:
            proc_layers = list(map(int, self.txt_layer.text().split(',')))

        return proc_layers

    def add_rest_layers(self):
        if self.check_infile():
            pass
        else:
            return

        proc_layers = self.get_proc_layers()

        v_rast = float(self.txt_v_rast.text().replace(',', '.'))
        t_rast = float(self.txt_t_rast.text().replace(',', '.'))
        r_min = float(self.txt_r_min.text().replace(',', '.'))
        r_max = float(self.txt_r_max.text().replace(',', '.'))
        acc = int(self.txt_accuracy.text())

        setattr(self.db, 'rp_points', [None]*self.db.layers)
        setattr(self.db, 'rp_arrows', [None]*self.db.layers)

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

            print(f'Rastfigur erfolgreich erzeugt.')

    def plot_layers(self, hidden=False):
        proc_layers = self.get_proc_layers()
        save = self.cb_save_figures.isChecked()
        s_dir = self.txt_save_plot_folder.text()
        s_only = self.cb_save_only_plot.isChecked()

        if hidden:
            s_only = True

        for lay in proc_layers:
            # Plot initialisieren
            cli.init_plot(layer=lay)

            l_name = self.txt_outname.text() + f'_{lay}'
            try:
                rp_arrows = self.db.rp_arrows[lay].reshape(-1, 4)
                arrow = self.db.arrows[lay]

                cli.plot_arrows(arrow, color='tab:blue')
                cli.plot_arrows(rp_arrows, color='tab:orange', a=0.1)

                cli.show_plot(save=save,
                              sdir=s_dir,
                              s_name=l_name + '_hatch+rest',
                              s_only=s_only)
            except (AttributeError, IndexError, TypeError):
                try:
                    arrow = self.db.arrows[lay]
                    cli.plot_arrows(arrow, color='tab:blue')
                    cli.show_plot(save=save,
                                  sdir=s_dir,
                                  s_name=l_name + '_hatch',
                                  s_only=s_only)
                except IndexError:
                    BOX.show_error_box('Layer nicht in Schichten enthalten')
                    return

    def check_data(self):
        check_flag = [False, False, False]

        # [
        #   (Hatchdaten, Hatchvektoren)
        #   (Polylinedaten, Polylinevektoren)
        #   (Restpositiondaten, Restpositionvektoren)
        # ]

        checks = [(self.db.hatchlist, self.db.arrows),
                  (self.db.polylist, self.db.pl_arrows),
                  (self.db.rp_arrows, self.db.rp_points)]

        for count, check_data in enumerate(checks):
            if any([i is None for i in check_data]):
                check_flag[count] = False
            else:
                check_flag[count] = True

        return check_flag

    def open_plot_dialog(self):
        check_data = self.check_data()
        transfer_data = {}
        # Teste, ob hatchlines enthalten sind
        if not check_data[0]:
            transfer_data['hatches'] = None
        else:
            transfer_data['hatches'] = self.db.arrows

        # Teste, ob es Polylines gibt
        if not check_data[1]:
            transfer_data['polylines'] = None
        else:
            transfer_data['polylines'] = self.db.pl_arrows

        # Teste, ob Rastpositionen erstellt wurden
        if not check_data[2]:
            transfer_data['rest'] = None
        else:
            transfer_data['rest'] = self.db.rp_arrows

        pd = plotUI.PlotDialog(transfer_data)
        pd.exec_()

    def clear_rast(self):
        self.but_rast.setEnabled(True)
        self.but_clear_rast.setEnabled(False)
        setattr(self.db, 'rp_points', None)
        setattr(self.db, 'rp_arrows', None)

    def check_infile(self):
        if self.txt_infile.text() == '':
            self.highlight_field(self.txt_infile)
            BOX.show_error_box('Keine Datei angegeben.')
            return False
        else:
            return True

    def set_layer_anz(self, layers):
        self.txt_lab_layer.setText(f'von {layers-1}')

    def load_cli_file(self):
        if self.check_infile():
            fname = self.txt_infile.text()
            lays, h_list, p_list = cli.load_data(fname)

            setattr(self.db, 'layers', lays)
            self.set_layer_anz(lays)

            if p_list is not None:
                pl, p_arr = cli.convert_polylines(lays, p_list)
                setattr(self.db, 'polylist', pl)
                setattr(self.db, 'pl_arrows', p_arr)

            if h_list is not None:
                hl, arr = cli.convert_hatches(lays, h_list)
                setattr(self.db, 'hatchlist', hl)
                setattr(self.db, 'arrows', arr)

            name, _ = os.path.splitext(os.path.basename(fname))

            self.txt_outname.setText(name)
            self.txt_save_plot_folder.setText('output/plots')
            self.txt_save_vec_folder.setText('output/figures')

        else:
            return False

    def save_vector_figures(self):
        proc_layers = self.get_proc_layers()

        vec_dir = self.txt_save_vec_folder.text()
        save = self.cb_save_figures.isChecked()
        s_only = self.cb_save_only_plot.isChecked()

        if save or s_only:
            self.plot_layers(hidden=True)
            if s_only:
                return

        pvz = int(self.txt_pvz.text())
        v_hatch = float(self.txt_v_hatch.text())
        v_contour = float(self.txt_v_contour.text())
        v_rast = float(self.txt_v_rast.text())
        build_dimension = float(self.txt_plate_size.text())/2

        for fig_type in ['contours', 'hatches']:
            for lay in proc_layers:
                l_name = self.txt_outname.text() + f'_{lay}_{fig_type}'

                outlist = []
                if self.db.rp_arrows is not None:
                    rp_arrows = self.db.rp_arrows[lay]
                    # nehme nur die Startpunkte jedes Pfeils
                    arr_strt = rp_arrows[:, 0, :2].reshape(len(rp_arrows), -1)
                    # nehme die Richtungsvektoren
                    arr_end = rp_arrows[:, :, 2:].reshape(len(rp_arrows), -1)
                    # Füge beide zusammen
                    rp_arr = np.hstack((arr_strt, arr_end))

                    rp_arr_conv = cli.convert_to_volt(rp_arr, factor=build_dimension)
                    vec_rast = cli.generate_hatch_data(rp_arr_conv,
                                                       rest=True,
                                                       v=v_rast,
                                                       pvz=pvz)
                    outlist.append(vec_rast)
                else:
                    pass

                if self.db.pl_arrows is not None or self.db.arrows is not None:
                    if fig_type == 'contours':
                        arrow = self.db.pl_arrows[lay]
                    else:
                        arrow = self.db.arrows[lay]
                else:
                    continue

                arrow_conv = cli.convert_to_volt(arrow, factor=build_dimension)
                if fig_type == 'contours':
                    vec = cli.generate_contour_data(arrow_conv,
                                                    v=v_contour,
                                                    pvz=pvz)
                else:
                    vec = cli.generate_hatch_data(arrow_conv,
                                                  v=v_hatch,
                                                  pvz=pvz)
                outlist.append(vec)

                output = cli.generate_output(outlist)

                cli.write_data(f'{l_name}.bxy', vec_dir, output)

            BOX.show_info_box(f'Datei "{fig_type}" erfolgreich gespeichert')

    def debug(self, hidden=False):
        return

    def plot_bxy(self):
        bxy_data = bxy.convert_bxy(self.txt_infile.text())

        cli.init_plot()
        cli.plot_arrows(bxy_data)
        cli.show_plot()

    def file_open(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Gib den Pfad zur Datei an')[0]
        if path:
            self.proc_input(path)
        else:
            return

    def save_destination(self):
        name = self.sender().objectName()
        if name == 'but_outname':
            out = QtWidgets.QFileDialog.getSaveFileName(self,
                                                        'Speicherort wählen', '',
                                                        'Vector-Dateien (*.bxy);;All Files (*)')[0]
            if out:
                outname = os.path.basename(out)
                self.proc_path(self.txt_outname, outname)
            else:
                return

        elif name == 'but_save_plot_folder' or 'but_save_vec_folder':
            path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Wähle einen Quellordner')
            if path:
                if name == 'but_save_plot_folder':
                    dest = self.txt_save_plot_folder
                else:
                    dest = self.txt_save_vec_folder
                self.proc_path(dest, path)

    def proc_input(self, path):
        _, file_extension = os.path.splitext(path)

        # Hier wird der Pfad in das Textfeld "txt_name" geschrieben
        self.proc_path(self.txt_infile, path)

        # Hier wird getestet, welche Datei angegeben wurde.
        if file_extension == '.cli':
            self.tabs.setCurrentIndex(0)
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, False)

            self.load_cli_file()
            BOX.show_info_box(f'Datei erfolgreich geladen.')

        elif '.b' in file_extension:
            self.tabs.setCurrentIndex(1)
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, True)
        else:
            BOX.show_error_box('Dieser Dateityp wird nicht unterstützt')

    def proc_path(self, receiver, text):
        # Hier wird der Pfad in das Textfeld des 'receivers' geschrieben
        receiver.setText(text)

    def un_highlight(self, field):
        field.setStyleSheet('border: 1px solid black')
        self.statusBar().setStyleSheet('color:black; font-weight:normal')

    def highlight_field(self, field):
        field.setStyleSheet('border: 2px solid red;')
        self.statusBar().setStyleSheet('color:red; font-weight:bold')


