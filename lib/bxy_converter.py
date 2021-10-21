import numpy as np

def convert_bxy(file):
    with open(file) as f:
        lines = f.readlines()

    relevant_lines = [line for line in lines if 'ABS' in line or 'REL' in line]

    rel_lines = [list(map(float, line.strip().split(' ')[1:3])) for line in lines if 'REL' in line]

    data = np.zeros((len(rel_lines), 4))
    data[:] = np.nan

    i = 0
    for rl in relevant_lines:
        if 'ABS' in rl:
            # TODO: aendern!!!!
            if j[0] == 0:
                j = [0, 0]
            data[i, :2] = list(map(float, rl.strip().split(' ')[1:]))
        if 'REL' in rl:
            j[0] += 1
            if j[1] != 1:
                j[1] = 1
            # setze Richtungsanweisung
            data[i, 2:] = rel_lines[i]

            # Wenn keine Startkoordinaten existieren (weil REL auf REl folgt)
            if np.isnan(data[i, 1]):
                # Setze X- und Y-Wert durch Addition der beiden vorherigen Wertepaare
                data[i, 0] = data[i-1, 0] + data[i-1, 2]
                data[i, 1] = data[i - 1, 1] + data[i - 1, 3]

            i += 1

    return data