import os
import fnmatch
from shutil import copyfile
from gui import boxes as BOX
from lib import helperFunctions as hF

def process_folder_list(fl, param_data, b_directory=None, hatches_first=False):

    accepted = BOX.show_msg_box('Der Inhalt des Ordners wird gelöscht.\nFortfahren?')
    if not accepted:
        return False

    hF.delete_all_files_in_directory(b_directory)

    current_layer = 0
    fig_nr = 1
    no_layers_left = False
    figures_in_layer_before = 0
    section = 1

    while not no_layers_left:
        layer_figures = []

        for fold in fl:
            # liste alle Dateien im Ordner auf
            all_files = os.listdir(fold)

            # Dateiname hat die Struktur >> CLI-Name_LAYER_contour/hatch.bxy <<
            substring = f'_{current_layer}_'
            # Finde alle Dateien, die im aktuellen Ordner liegen sollen
            matching_figures = [string for string in all_files if substring in string and '.bxy' in string]
            # Falls der Ordner keine Figuren mehr in diesem Layer enthält
            if not matching_figures:
                fl.remove(fold)
                continue
            else:
                # Wenn Hatches zuerst geschrieben werden sollen
                if hatches_first and len(matching_figures) > 1:
                    matching_figures.reverse()

                matching_figures = [fold + '/' + s for s in matching_figures]
                layer_figures.append(matching_figures)

        layer_figures = [i for sublist in layer_figures for i in sublist]
        # Teste, ob sich die Figurenanzahl im Layer geändert hat
        figures_in_layer = len(layer_figures)

        if figures_in_layer != figures_in_layer_before or figures_in_layer != 0:
            print(param_data)
            # erstelle den String für eine Neue Section
            para_string = create_new_section(section, current_layer, figures_in_layer, param_data)
            # schreibe ihn in eine Datei im Build-Verzeichnis
            write_cnc_file(para_string, b_directory)
            figures_in_layer_before = figures_in_layer
            section += 1

        for i, fig in enumerate(layer_figures):
            new_name = f'{fig_nr}.bxy'
            new_dest = b_directory + '/' + new_name
            copyfile(fig, new_dest)
            fig_nr += 1

        current_layer += 1

        # Wenn es keine Ordner mehr gibt, in denen Figuren liegen
        if not fl:
            no_layers_left = True

    return True


def create_new_section(nr, cl, figures, params):
    dimx = 150
    dimy = 150
    stringlist = [f'_par_field[{nr},0] = SET({cl+1}, {dimx}, {dimy}, {figures})']
    for f in range(figures):
        pvzl = params[int(f/2)]['pvz']
        pvzh = 0
        il = 2000
        ib = 5
        s = f'_par_field[{nr}, {10+5*f}] = SET({il}, {ib}, {pvzl}, {pvzh})'
        stringlist.append(s)

    sec_string = '\n'.join(stringlist)

    return sec_string


def write_cnc_file(s, dest, name='0_cnc_params.txt'):
    fname = dest + '/' + name
    mode = hF.get_mode(fname)
    with open(fname, mode) as f:
        f.write(s)

def test_for_matching_files(directory, ftype=['.bxy', '*.ini']):
    ret_val = [False] * len(directory)
    for i, d in enumerate(directory):
        files = os.listdir(d)
        if [ft for ft in ftype if fnmatch.filter(files, f'*{ft}')]:
            ret_val[i] = True

    return ret_val


