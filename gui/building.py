from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem as QTI
from PyQt5.QtGui import QMovie
from gui import buildGUI as bG
from gui import boxes as BOX
from lib import config as cf
from lib import buildGen as bGe
from lib import helperFunctions as hF
import os


class BuildGenerator(QtWidgets.QDialog, bG.Ui_Dialog):
    def __init__(self):
        super(BuildGenerator, self).__init__()
        self.setupUi(self)
        self.setup_triggers()

        self.status_label.hide()
        # self.gif_label.hide()


    def setup_triggers(self):
        self.but_load_folders.clicked.connect(self.load_data)
        self.but_destination.clicked.connect(self.get_save_destination)
        self.but_generate_build_job.clicked.connect(self.generate_build_job)

    def load_data(self):
        # lade Ordner
        folderlist = self.get_folders()
        # teste, ob .bxy und .ini Dateien im Ordner liegen
        out = hF.test_for_matching_files(folderlist, ['.bxy', '*.ini'])

        # Filtere nur nach passenden Ordnern
        folderlist = hF.masklist(folderlist, out)

        # falls keiner der Ordner passende Dateien enthält
        if len(folderlist) == 0:
            return

        tab = self.tab_open_folders
        tab.setRowCount(len(folderlist))

        orderlist = [None] * len(folderlist)

        for i, f in enumerate(folderlist):
            para = cf.load_parameters(f)
            general_sec = 'general'
            if not para.has_section(general_sec):
                para.add_section(general_sec)
                para.set(general_sec, 'plate_size', '-')

            for fig_type in ['contours', 'hatches']:
                if not para.has_section(fig_type):
                    para.add_section(fig_type)
                    for p in ['pvz', 'IB', 'IL']:
                        para.set(fig_type, p, '-')

            tab.setItem(i, 0, QTI(str(i+1)))
            tab.setItem(i, 1, QTI(str(para['contours']['pvz'])))
            tab.setItem(i, 2, QTI(str(para['contours']['IB'])))
            tab.setItem(i, 3, QTI(str(para['contours']['IL'])))
            tab.setItem(i, 4, QTI(str(para['hatches']['pvz'])))
            tab.setItem(i, 5, QTI(str(para['hatches']['IB'])))
            tab.setItem(i, 6, QTI(str(para['hatches']['IL'])))
            tab.setItem(i, 7, QTI(str(para['general']['plate_size'])))
            tab.setItem(i, 8, QTI(f))

            orderlist[i] = str(i+1)

        order = ', '.join(orderlist)

        self.txt_user_order.setText(order)
        self.txt_destination.setText('output/job')

    def get_folders(self):
        fd = FileDialog()
        # fd.show()
        fd.exec_()
        return fd.selectedFiles()

    def get_save_destination(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not folder:
            return
        else:
            self.txt_destination.setText(folder)

    def generate_build_job(self):
        order = self.txt_user_order.text().split(', ')
        order = list(map(int, order))

        if not hF.all_unique(order):
            BOX.show_info_box('Es wurden Ordner mehrfach gewählt!')
            return

        flist = [None] * len(order)
        parameters = [None] * len(order)

        tab = self.tab_open_folders
        for i in range(len(order)):
            flist[i] = tab.item(order[i]-1, 8).text()
            parameters[i] = {
                'contours': {
                    'pvz': tab.item(order[i]-1, 1).text(),
                    'IB': tab.item(order[i]-1, 2).text(),
                    'IL': tab.item(order[i]-1, 3).text()
                },
                'hatches': {
                    'pvz': tab.item(order[i]-1, 4).text(),
                    'IB': tab.item(order[i]-1, 5).text(),
                    'IL': tab.item(order[i]-1, 6).text()
                },
                'plate_size': tab.item(order[i]-1, 7).text()
            }
        if not hF.all_equal([i['plate_size'] for i in parameters]):
            BOX.show_error_box('Es sind Figuren für unterschiedliche Bauräume geladen.')
            return

        try:
            dest = self.txt_destination.text()

            if dest == '':
                BOX.show_error_box('Kein Zielverzeichnis angegeben!')
                return

            if not os.path.isabs(dest):
                dest = os.path.abspath(dest)

            hatch_first = self.cb_hatch_first.isChecked()
            old_file_names = self.cb_oldfilename.isChecked()

            gif = QMovie("C:/Users/halbauer/Desktop/loading_2.gif")
            self.gif_label.setMovie(gif)
            # self.gif_label.show()
            # gif.start()
            accepted = BOX.show_msg_box('Der Inhalt des Ordners wird gelöscht.\nFortfahren?')
            if accepted:
                hF.delete_all_files_in_directory(dest)
            else:
                return

            success = bGe.process_folder_list(flist, parameters, b_directory=dest,
                                              hatches_first=hatch_first, old_files=old_file_names, pb=gif)

            gif.stop()

            if success:
                BOX.show_info_box('Baujob erfolgreich erstellt.')
            else:
                BOX.show_error_box('Es gab Fehler')

        except FileNotFoundError as FE:
            print(FE)
            BOX.show_error_box('Datei nicht gefunden.')


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.DirectoryOnly)

        for view in self.findChildren((QtWidgets.QListView, QtWidgets.QTreeView)):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

