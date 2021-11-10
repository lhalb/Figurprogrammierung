import os
from shutil import copyfile
from lib import helperFunctions as hF


def process_folder_list(fl, param_data, b_directory=None, hatches_first=False, old_files=False):
    current_layer = 0
    fig_nr = 1
    no_layers_left = False
    figures_in_layer_before = 0
    section = 1

    while not no_layers_left:

        layer_figures = []

        # gehe nur durch die Ordner, die noch Daten enthalten (Ordner ohne Daten werden auf "None" gesetzt
        for fold in [f for f in fl if f]:
            # liste alle Dateien im Ordner auf
            all_files = os.listdir(fold)

            # Dateiname hat die Struktur >> CLI-Name_LAYER_contour/hatch.bxy <<
            substring = f'_{current_layer}_'
            # Finde alle Dateien, die im aktuellen Ordner liegen sollen
            matching_figures = [string for string in all_files if substring in string and '.bxy' in string]
            # Falls der Ordner keine Figuren mehr in diesem Layer enthält
            if not matching_figures:
                # index des Ordners heraussuchen
                index_of_folder = fl.index(fold)
                # den Ordner von der Liste zu durchsuchender Ordner löschen
                fl[index_of_folder] = None
                # Liste mit Parameterdateien anpassen
                param_data[index_of_folder] = None
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

        if figures_in_layer != figures_in_layer_before and figures_in_layer != 0:
            # erstelle den String für eine Neue Section
            parameters = [i for i in param_data if i]
            para_string = create_new_section(section, current_layer, figures_in_layer, parameters, layer_figures)
            # schreibe ihn in eine Datei im Build-Verzeichnis
            write_cnc_file(para_string, b_directory)
            figures_in_layer_before = figures_in_layer
            section += 1

        for i, fig in enumerate(layer_figures):
            if old_files:
                ext = '.b00'
            else:
                ext = '.bxy'
            new_name = f'{fig_nr}{ext}'
            new_dest = b_directory + '/' + new_name
            copyfile(fig, new_dest)
            fig_nr += 1

        current_layer += 1

        # Wenn es keine Ordner mehr gibt, in denen Figuren liegen
        if not any(fl):
            no_layers_left = True

    return True


def create_new_section(nr, cl, figures, params, figure_names):
    dimx = params[0]['plate_size']
    dimy = params[0]['plate_size']

    stringlist = [f'_par_field[{nr},0] = SET({cl+1}, -{dimx}, -{dimy}, {figures})']
    par = -1
    folder_before = ''
    for f in range(figures):
        curr_folder = figure_names[f].split('/')[-2]
        for s in ['contours', 'hatches']:
            if s in figure_names[f]:
                sec = s

        if curr_folder != folder_before:
            par += 1
        folder_before = curr_folder

        pvzl = params[par][sec]['pvz']
        pvzh = 0
        il = params[par][sec]['IL']
        ib = params[par][sec]['IB']
        s = f'_par_field[{nr}, {10+5*f}] = SET({il}, {ib}, {pvzl}, {pvzh})'
        stringlist.append(s)

    sec_string = '\n'.join(stringlist)

    return sec_string


def write_cnc_file(s, dest, name='0_cnc_params.txt'):
    fname = dest + '/' + name
    mode = hF.get_mode(fname)
    with open(fname, mode) as f:
        if mode == 'a':
            s = "\n\n" + s
        f.write(s)



