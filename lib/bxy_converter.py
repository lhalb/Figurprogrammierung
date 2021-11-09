import numpy as np


def convert_bxy(file):
    with open(file) as f:
        lines = f.readlines()

    relevant_lines = [line for line in lines if 'ABS' in line or 'REL' in line]

    rel_lines = [list(map(float, line.strip().split(' ')[1:3])) for line in lines if 'REL' in line]

    data = np.zeros((len(relevant_lines), 4))
    data[:] = np.nan

    i = 0
    j = 0
    for rl in relevant_lines:
        if 'ABS' in rl:
            j = 0
            data[i, :2] = list(map(float, rl.strip().split(' ')[1:]))
        elif 'REL' in rl:
            # Wenn es nicht der erste Punkt ist
            if j != 0:
                data[i, 0] = data[i-1, 0] + rel_lines[i-1][0]
                data[i, 1] = data[i-1, 1] + rel_lines[i-1][1]
            else:
                i -= 1
            data[i, 2:] = rel_lines[i]
            j += 1

        i += 1

    return data
