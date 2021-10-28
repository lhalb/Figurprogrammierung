from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem as QTI
from gui import buildGUI as bG
from gui import boxes as BOX
from lib import config as cf
from lib import buildGen as bGe
from lib import helperFunctions as hF


class BuildGenerator(QtWidgets.QDialog, bG.Ui_Dialog):
    def __init__(self):
        super(BuildGenerator, self).__init__()
        self.setupUi(self)
        self.setup_triggers()

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
        tab.setRowCount(len(folderlist) + 1)

        orderlist = [None] * len(folderlist)

        for i, f in enumerate(folderlist):
            para = cf.load_parameters(f)

            tab.setItem(i+1, 0, QTI(str(i+1)))
            tab.setItem(i+1, 1, QTI(str(para['PARAMS']['pvz'])))
            tab.setItem(i + 1, 2, QTI(f))

            orderlist[i] = str(i+1)

        order = ', '.join(orderlist)

        self.txt_user_order.setText(order)

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

        flist = [None] * len(order)
        parameters = [{}] * len(order)

        tab = self.tab_open_folders
        for i in range(len(order)):
            flist[i] = tab.item(order[i], 2).text()
            parameters[i]['pvz'] = tab.item(order[i], 1).text()

        try:
            dest = self.txt_destination.text()
            hatch_first = self.cb_hatch_first.isChecked()
            success = bGe.process_folder_list(flist, parameters, b_directory=dest, hatches_first=hatch_first)
            if success:
                BOX.show_info_box('Baujob erfolgreich erstellt.')

        except FileNotFoundError:
            BOX.show_error_box('Ausgabeziel nicht definiert')




class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.DirectoryOnly)

        for view in self.findChildren((QtWidgets.QListView, QtWidgets.QTreeView)):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

