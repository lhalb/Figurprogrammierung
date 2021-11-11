from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem as QTI
from gui import multiImportGUI as mIG
from lib import helperFunctions as hF
from lib import cli_converter as cli
from lib import config as cfg
from gui import boxes as BOX
import os
import numpy as np


class MultiImport(QtWidgets.QDialog, mIG.Ui_Dialog):
    def __init__(self):
        super(MultiImport, self).__init__()
        self.setupUi(self)
        self.setup_buttons()

    def setup_buttons(self):
        self.but_load_files.clicked.connect(self.open_files)
        self.but_output_folder.clicked.connect(self.get_save_directory)
        self.but_convert_files.clicked.connect(self.convert_files)
        self.but_save_set.clicked.connect(self.save_settings)
        self.but_load_set.clicked.connect(self.load_from_settings)

    def open_files(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Wähle die CLI-Dateien aus', '', 'CLI-Files (*.cli)')[0]
        if not files:
            return

        self.write_to_table(files)
        self.txt_output_folder.setText('output/multifigures')

    def load_from_settings(self):
        ini_file = QtWidgets.QFileDialog.getOpenFileName(self, "Pfad zur .ini-Datei", '', 'INI-Files (*.ini)')[0]
        if not ini_file:
            return
        folder = hF.get_foldername(ini_file)

        para = cfg.load_parameters(folder, filename=hF.get_file_with_extension(ini_file))
        fl = para.sections()
        self.write_to_table(filelist=fl, params=para)
        BOX.show_info_box('Daten erfolgreich importiert')

    def save_settings(self):
        outfile = QtWidgets.QFileDialog.getSaveFileName(self, 'Wo sollen die Einstellungen gespeichert werden?',
                                                        'multi_settings.ini', 'INI-Files (*.ini)')[0]
        if not outfile:
            return

        file_exists = hF.check_for_existing_file(outfile)
        if file_exists:
            ret_val = BOX.show_msg_box('Datei existiert bereits.\nÜberschreiben?')
            if not ret_val:
                return
            else:
                os.remove(outfile)

        tab = self.table_parameters
        para = {}
        for i in range(tab.rowCount()):
            secname = tab.item(i, 9).text().lower()
            settings = ['v-C', 'PVZ-C', 'IB-C', 'IL-C', 'v-H', 'PVZ-H', 'IB-H', 'IL-H', 'SIZE', 'Name', 'Path']
            para[secname] = {}
            for j, s in enumerate(settings):
                para[secname][s] = tab.item(i, j).text()

        outfolder = hF.get_foldername(outfile)
        fname = hF.get_file_with_extension(outfile)

        cfg.save_parameters(para, outfolder, filename=fname)

        BOX.show_info_box('Einstellungen erfolgreich gespeichert')

    def write_to_table(self, filelist, params=None):
        tab = self.table_parameters
        tab.setRowCount(len(filelist))
        if not params:
            for i, file in enumerate(filelist):
                foldername = hF.get_filename(file)
                for j in range(9):
                    tab.setItem(i, j, QTI('-'))
                tab.setItem(i, 9, QTI(foldername))
                tab.setItem(i, 10, QTI(file))
        else:
            for i, sec in enumerate(params.keys()):
                for j, par in enumerate(params[sec].keys()):
                    tab.setItem(i-1, j, QTI(str(params[sec][par])))

    def get_save_directory(self):
        outfolder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Wo sollen die Dateien gespeichert werden?')
        if not outfolder:
            return

        self.txt_output_folder.setText(outfolder)

    def convert_files(self):
        tab = self.table_parameters
        if tab.rowCount() == 0:
            BOX.show_error_box('Keine Dateien geladen!')
            return

        for line in range(tab.rowCount()):
            success = True
            fname = tab.item(line, 10).text()
            cli_name = tab.item(line, 9).text()
            vec_dir = self.txt_output_folder.text()
            save_dir = vec_dir + '/' + cli_name

            hF.create_directory_if_needed(save_dir)

            if any(hF.test_for_matching_files([save_dir], ['.bxy', '.ini'])):
                accepted = BOX.show_msg_box(f'Das Verzeichnis {save_dir} ist nicht leer.\n\nLöschen?')
                if accepted:
                    hF.delete_all_files_in_directory(save_dir)
                else:
                    continue

            lays, h_list, p_list = cli.load_data(fname)

            try:
                build_dimension = int(tab.item(line, 8).text()) / 2
            except ValueError:
                BOX.show_error_box(f'Bei Datei {fname} fehlt die Plattformgröße')
                success = False
                continue

            parameters = {
                'general': {
                    'plate_size': int(tab.item(line, 8).text())
                }
            }

            figs = []
            if p_list:
                figs.append('contours')
                pl, p_arr = cli.convert_polylines(lays, p_list)
                try:
                    v_contour = float(tab.item(line, 0).text())
                except ValueError:
                    BOX.show_error_box(f'Bei Datei {fname}\n'
                                       f'ist eine fehlerhafte Geschwindigkeit der Kontur angegeben.')
                    success = False
                    continue
                try:
                    pvz_contour = int(tab.item(line, 1).text())
                except ValueError:
                    BOX.show_error_box(f'Bei Datei {fname}\n'
                                       f'ist eine fehlerhafte Punktverzögerung der Kontur angegeben.')
                    success = False
                    continue
                ib_contour = tab.item(line, 2).text()
                il_contour = tab.item(line, 3).text()
                parameters['contours'] = {
                    'pvz': pvz_contour,
                    'v': v_contour,
                    'IB': ib_contour,
                    'IL': il_contour
                }

            if h_list:
                figs.append('hatches')
                hl, arr = cli.convert_hatches(lays, h_list)
                try:
                    v_hatch = float(tab.item(line, 4).text())
                except ValueError:
                    BOX.show_error_box(f'Bei Datei {fname}\n'
                                       f'ist eine fehlerhafte Geschwindigkeit im Hatch angegeben.')
                    success = False
                    continue
                try:
                    pvz_hatch = int(tab.item(line, 5).text())
                except ValueError:
                    BOX.show_error_box(f'Bei Datei {fname}\n'
                                       f'ist eine fehlerhafte Punktverzögerung im Hatch angegeben.')
                    success = False
                    continue
                ib_hatch = tab.item(line, 6).text()
                il_hatch = tab.item(line, 7).text()
                parameters['hatches'] = {
                    'pvz': pvz_hatch,
                    'v': v_hatch,
                    'IB': ib_hatch,
                    'IL': il_hatch
                }

            if not figs:
                BOX.show_info_box('Es wurden keine passenden Figuren gefunden.')
                success = False
                return

            cfg.save_parameters(parameters, save_dir)

            for fig_type in figs:
                for lay in range(lays):
                    l_name = cli_name + f'_{lay}_{fig_type}'

                    outlist = []
                    if fig_type == 'contours':
                        arrow = p_arr[lay]
                    else:
                        arrow = arr[lay]

                    arr_strt = cli.convert_to_volt_abs(arrow[:, :2], build_dimension)
                    arr_end = cli.convert_to_volt_rel(arrow[:, 2:], build_dimension)

                    # arrow_conv = cli.rotate(np.hstack((arr_strt, arr_end)), degrees=270)
                    arrow_conv = np.hstack((arr_strt, arr_end))
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
        if success:
            BOX.show_info_box('Konvertierung erfolgreich')
        else:
            BOX.show_info_box('Konvertierung nicht erfolgreich')


