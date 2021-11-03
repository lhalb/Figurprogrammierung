'''
Autor: Halbauer
Date: 06.02.2019

Template zum Laden eines QT5 Fensters mit Tastaturkürzeln und Triggern

Erstellung des Layouts mit QT-Designer wird angenommen
Hierfür im Vorfeld .ui Datei in .py umwandlen und im gleichen VZ wie Template.py ablegen
Code für Umwandlung:
    pyuic5 -x template.ui -o template.py

'''
import sys
from PyQt5 import QtWidgets, QtGui
from gui import startGUI, plotting, building, resting, multiImport
from gui import boxes as BOX
import os
from lib import cli_converter as cli
import numpy as np
from lib import config as cf
from lib import bxy_converter as bxy
from lib import helperFunctions as hF
from lib.Database import DataBase


# in der Klasse muss noch einmal die Klasse des Templates übergeben werden,
# da sonst die Zuweisung der Trigger nicht funktioniert.
class MyApp(QtWidgets.QMainWindow, startGUI.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setup_triggers()  # lade Events für Buttons
        self.tabs.hide()
        self.resize(self.sizeHint().width(), self.sizeHint().height())
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(0, False)

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
        self.but_rest_dialog.clicked.connect(self.open_rest_dialog)
        self.but_plot.clicked.connect(self.open_plot_dialog)
        self.but_convert_cli.clicked.connect(self.save_vector_figures)
        self.but_buildgenerator.clicked.connect(self.open_buildgenerator)
        self.but_multi_import.clicked.connect(self.open_multi_import)

    def get_proc_layers(self):
        def max_or_min(vals, max_val, min_val=0):
            if [v for v in vals if v >= max_val]:
                BOX.show_error_box('Einer der Werte ist zu hoch')
                return True
            if [v for v in vals if v < min_val]:
                BOX.show_error_box('Einer der Werte ist zu niedrig')
                return True

        txt = self.txt_layer.text()
        max_layers = self.db.layers
        if txt == 'all':
            proc_layers = [i for i in range(max_layers)]
        # Wenn man eine Range angegeben hat
        elif ':' in txt:
            lay_range = txt.split(':')
            # Es gibt mehr oder weniger als zwei Werte
            if len(lay_range) != 2:
                BOX.show_error_box('Falsche Range-Angabe')
                return False
            # Wenn man nur ':' eingegeben hat
            elif lay_range[0] == '' and lay_range[1] == '':
                BOX.show_error_box('Keine Range angegeben')
                return False
            # Es gibt mindestens zwei Werte
            else:
                try:
                    if lay_range[0] == '':
                        start = 0
                    else:
                        start = int(lay_range[0])
                    if lay_range[1] == '':
                        end = max_layers - 1
                    else:
                        end = int(lay_range[1])
                except ValueError:
                    BOX.show_error_box('Fehler bei der INT-Konvertierung')
                    return False

                # Falls Werte übersetzt werden können
                # Falls aber einer der beiden Werte größer als die Layeranzahl ist
                if max_or_min([start, end], max_layers, 0):
                    return False

                proc_layers = [i for i in range(start, end + 1)]

        # Wenn man eine Zahlenreihe angegeben hat
        else:
            try:
                proc_layers = list(map(int, self.txt_layer.text().split(',')))
                # Wenn einer der Layer größer als die Layeranzahl ist:
                if max_or_min(proc_layers, max_layers, 0):
                    return False
            except ValueError:
                BOX.show_error_box('Fehler bei der INT-Konvertierung')
                return False

        return proc_layers

    def plot_layers(self, hidden=False):
        proc_layers = self.get_proc_layers()
        if not proc_layers:
            return
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
                rp_arrows = self.db.rp_arrows[lay]
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
        check_flag = [False, False, False, False]

        # [
        #   (Hatchdaten, Hatchvektoren)
        #   (Polylinedaten, Polylinevektoren)
        #   (Restpositiondaten, Restpositionvektoren)
        #   (Layeranzahl)
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

    def get_transfer_data(self):
        check_data = self.check_data()
        transfer_data = {}
        # Teste, ob hatchlines enthalten sind
        if not check_data[0]:
            transfer_data['hatches'] = []
        else:
            transfer_data['hatches'] = [self.db.hatchlist, self.db.arrows]

        # Teste, ob es Polylines gibt
        if not check_data[1]:
            transfer_data['polylines'] = []
        else:
            transfer_data['polylines'] = [self.db.polylist, self.db.pl_arrows]

        # Teste, ob Rastpositionen erstellt wurden
        if not check_data[2]:
            transfer_data['rest'] = []
        else:
            transfer_data['rest'] = [self.db.rp_points, self.db.rp_arrows]

        return transfer_data

    def open_plot_dialog(self):
        data = self.get_transfer_data()

        pd = plotting.PlotDialog(data)
        pd.exec_()

    def open_rest_dialog(self):
        data = self.get_transfer_data()
        if self.txt_layer.text() != 'all':
            layers = self.get_proc_layers()
        else:
            layers = range(self.db.layers)
        rd = resting.RestDialog(data, layers)
        accepted = rd.exec_()
        if accepted:
            setattr(self.db, 'rp_points', rd.data['rest'][0])
            setattr(self.db, 'rp_arrows', rd.data['rest'][1])

        self.check_for_data(self.check_data())

    def get_parameters(self):
        parameters = {
            'rest': {
                'v': float(self.txt_v_rast.text())
            },
            'general': {
                'plate_size': float(self.txt_plate_size.text())
            },
            'contours': {
                'pvz': int(self.txt_pvz_contour.text()),
                'v': float(self.txt_v_contour.text()),
                'IB': float(self.txt_ib_contour.text()),
                'IL': int(self.txt_il_contour.text())
            },
            'hatches': {
                'pvz': int(self.txt_pvz_hatch.text()),
                'v': float(self.txt_v_hatch.text()),
                'IB': float(self.txt_ib_hatch.text()),
                'IL': int(self.txt_il_hatch.text())
            }
        }
        return parameters

    def check_infile(self):
        if self.txt_infile.text() == '':
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

            try:
                if p_list:
                    pl, p_arr = cli.convert_polylines(lays, p_list)
                    setattr(self.db, 'polylist', pl)
                    setattr(self.db, 'pl_arrows', p_arr)

                if h_list:
                    hl, arr = cli.convert_hatches(lays, h_list)
                    setattr(self.db, 'hatchlist', hl)
                    setattr(self.db, 'arrows', arr)

            except IndexError:
                BOX.show_error_box('Die Datei enthält leere Layer.')
                return False

            name, _ = os.path.splitext(os.path.basename(fname))

            self.txt_outname.setText(name)
            self.txt_save_plot_folder.setText('output/plots')
            self.txt_save_vec_folder.setText('output/figures')

            self.check_for_data(self.check_data())

        else:
            return False

    def save_vector_figures(self):
        proc_layers = self.get_proc_layers()
        if not proc_layers:
            return

        cli_name = self.txt_outname.text()
        vec_dir = self.txt_save_vec_folder.text()
        save_dir = vec_dir + '/' + cli_name
        save = self.cb_save_figures.isChecked()
        s_only = self.cb_save_only_plot.isChecked()

        hF.create_directory_if_needed(save_dir)

        if any(hF.test_for_matching_files([save_dir], ['.bxy', '.ini'])):
            accepted = BOX.show_msg_box('Das gewählte Verzeichnis ist nicht leer.\n\nLöschen?')
            if accepted:
                hF.delete_all_files_in_directory(save_dir)
            else:
                return

        if save or s_only:
            self.plot_layers(hidden=True)
            if s_only:
                return

        # hole Parameter ab
        para = self.get_parameters()
        # speichere alle Parameter
        cf.save_parameters(para, save_dir)

        v_hatch = para['hatches']['v']
        pvz_hatch = para['hatches']['pvz']

        v_contour = para['contours']['v']
        pvz_contour = para['contours']['pvz']

        v_rast = para['rest']['v']
        build_dimension = para['general']['plate_size']/2

        for fig_type in ['contours', 'hatches']:
            for lay in proc_layers:
                l_name = cli_name + f'_{lay}_{fig_type}'

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
                                                       pvz=pvz_hatch)
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
                                                    pvz=pvz_contour)
                else:
                    vec = cli.generate_hatch_data(arrow_conv,
                                                  v=v_hatch,
                                                  pvz=pvz_contour)
                outlist.append(vec)

                output = cli.generate_output(outlist)

                cli.write_data(f'{l_name}.bxy', save_dir, output)

            if not self.cb_quiet.isChecked():
                BOX.show_info_box(f'Datei "{fig_type}" erfolgreich gespeichert')

        BOX.show_info_box('Konvertierung erfolgreich')

    def debug(self, hidden=False):
        return

    def plot_bxy(self):
        bxy_data = bxy.convert_bxy(self.txt_infile.text())

        cli.init_plot()
        cli.plot_arrows(bxy_data)
        cli.show_plot()

    def open_buildgenerator(self):
        bg = building.BuildGenerator()
        bg.exec_()

    def open_multi_import(self):
        mi = multiImport.MultiImport()
        mi.exec_()

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
            ret_val = self.load_cli_file()
            if not ret_val:
                return

            self.tabs.show()
            # self.setFixedSize(self.full_window.sizeHint())
            self.tabs.setCurrentIndex(0)
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, False)

            BOX.show_info_box(f'Datei erfolgreich geladen.')

        elif '.b' in file_extension:
            self.tabs.show()
            # self.setFixedSize(self.full_window.sizeHint())
            self.tabs.setCurrentIndex(1)
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, True)
        else:
            BOX.show_error_box('Dieser Dateityp wird nicht unterstützt')



    def proc_path(self, receiver, text):
        # Hier wird der Pfad in das Textfeld des 'receivers' geschrieben
        receiver.setText(text)

    def check_for_data(self, data):
        on_icon = QtGui.QIcon(":/img/img/green_light.png")
        off_icon = QtGui.QIcon(":/img/img/red_light.png")

        check_fields = [self.but_info_hatches, self.but_info_contours, self.but_info_rest]
        check_data = data[:3]

        for field, dat in zip(check_fields, check_data):
            if dat:
                field.setIcon(on_icon)
            else:
                field.setIcon(off_icon)


