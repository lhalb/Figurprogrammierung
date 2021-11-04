import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from lib import helperFunctions as hF
import os
matplotlib.use('Qt5agg')


def load_data(file):
    with open(file) as f:
        lines = f.readlines()

    layers = [int(i.split('/')[1]) for i in lines if 'LAYERS' in i][0]

    hatchlines = [i.strip().split(',')[2:] for i in lines if 'HATCHES' in i]
    polylines = [i.strip().split(',')[3:] for i in lines if 'POLYLINE' in i]
    # hatch_anz = [int(i.split(',')[1]) for i in lines if 'HATCHES' in i]

    return layers, hatchlines, polylines


def convert_hatches(layers, hatchlines):
    hatchlist, arrowlist = [None] * layers, [None] * layers

    for i in range(layers):
        data = np.asarray(hatchlines[i]).astype(float).reshape((-1, 4))
        start = data[:, :2]
        end = data[:, 2:]

        arr = np.hstack((start, end-start))

        hatchlist[i] = data
        arrowlist[i] = arr



    return hatchlist, arrowlist


def convert_polylines(layers, list_of_polylines):
    # initialisiere die Daten, da mehrere Polylines in einer Schicht sein können
    polylist, arrowlist = [None] * layers, [None] * layers

    # loope über eingescannte Daten, da Polylines unterschiedliche Länge haben können
    for i in range(layers):
        data = np.asarray(list_of_polylines[i]).astype('float')

        start = data[:-2]
        end = data[2:]
        dist = end - start

        points = int((len(data)/2)-1)

        new_start = start.reshape(points, 2)
        new_end = end.reshape(points, 2)
        new_dist = dist.reshape(points, 2)

        polylist[i] = np.hstack((new_start, new_end))
        arrowlist[i] = np.hstack((new_start, new_dist))

    return polylist, arrowlist


def convert_to_volt_rel(data, factor=1):
    return data/factor


def convert_to_volt_abs(data, factor=1):
    shifted_data = data - factor
    return shifted_data/factor


def make_rest_positions(d, v=100, time=2, rp_min=0.3, rp_max=0.7, exact=4, verbose=False):
    '''
    :param d: Abmessungen der Bearbeitungskontur [x_min, x_max, y_min, y_max]
    :param v: gewünschte Strahlgeschwindigkeit [mm/s]
    :param time: gewünschte Verweilzeit des Strahls [s]
                 (v*t ergibt die Strecke, die durch Rastpositionen zurückgelegt werden muss)
    :param rp_min: Anteil des inneren Feldes, der nicht beschrieben wird
    :param rp_max: Anteil des Feldes, in dem noch geschrieben wird
    :param exact: Genauigkeit der Strecke der Rastpositionen in Stellen
    :param verbose: Gebe den Fortschritt der Wegberechnung an
    :return: Vektoren des Musters [x, y, dx1=x, 0, d0, dy1=y, dx2=-x, 0, 0, dy2=-y]
    '''

    def get_random_positions(n, d_i, d_o):
        numbers = np.random.rand(n)
        return numbers * d_o + (1 - numbers) * d_i

    dx = d[1] - d[0]
    dy = d[3] - d[2]
    d_min = min(dx, dy)

    center = [(d[0] + dx * 0.5), d[2] + dy*0.5]

    dia_inner = rp_min * d_min
    dia_outer = rp_max * d_min

    soll_weg = v*time

    # print(f'Es müssten {soll_weg} mm zurückgelegt werden.')

    anz = 1
    pos = get_random_positions(anz, dia_inner, dia_outer)
    weg = round(np.sum(pos)*4, exact)
    while weg != soll_weg:
        if weg < soll_weg:
            anz += 1
        elif weg > soll_weg:
            anz -= 1
        pos = get_random_positions(anz, dia_inner, dia_outer)
        weg = round(np.sum(pos)*4, exact)
        if verbose:
            print(f'SOLL: {soll_weg}, IST: {weg}, Bahnen: {anz}')

    points = np.zeros((len(pos), 4, 4))

    for i, el in enumerate(pos):
        shift = pos[i]
        pos_x = center[0] + shift * 0.5
        pos_y = center[1] + shift * 0.5

        points[i][0, 0] = pos_x
        points[i][0, 1] = pos_y
        points[i][1, 0] = pos_x - shift
        points[i][1, 1] = pos_y
        points[i][2, 0] = pos_x - shift
        points[i][2, 1] = pos_y - shift
        points[i][3, 0] = pos_x
        points[i][3, 1] = pos_y - shift
        index_dir = [[0, 2], [1, 3], [2, 2], [3, 3]]
        i_dir_trans = np.array(index_dir).T.tolist()
        points[i][tuple(i_dir_trans)] = shift

        i_negative = [[0, 2], [1, 3]]
        i_neg_trans = np.array(i_negative).T.tolist()
        points[i][tuple(i_neg_trans)] *= -1

    dirs = points[:, :, 2:].reshape(len(points), 8)
    starts = points[:, 0, 0:2]

    rp_points = np.hstack((starts, dirs))

    return rp_points, points.reshape(-1, 4)


def init_plot(size=4, unit='mm', layer=0):
    plt.figure(figsize=(size, size))
    plt.xlabel(f'X in [{unit}]')
    plt.ylabel(f'Y in [{unit}]')
    plt.title(f'Strahllaufwege Schicht {layer}')


def show_plot(save=False, sdir=None, s_name=None, s_only=False):
    if save:
        save_dir = os.path.abspath(sdir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        dest = os.path.join(save_dir, s_name + '.png')

        plt.savefig(dest, dpi=300)
    if not s_only:
        plt.show()


def plot_arrows(data, color='k', a=1.0):
    x = data[:, 0]
    y = data[:, 1]
    u = data[:, 2]
    v = data[:, 3]

    plt.quiver(x, y, u, v,
               color=color,
               angles='xy',
               scale_units='xy',
               scale=1,
               width=0.005,
               headwidth=5,
               alpha=a
               )


def get_points_for_velocity(x, y, v, pvz):
    return int((np.sqrt(x ** 2 + y ** 2) / v) / (pvz * 1e-9) - 1)


def generate_contour_data(data, v=None, pvz=None):
    s = [f'ABS {data[0, 0]} {data[0, 1]}']
    for d in data:
        if v is None and pvz is None:
            anz = ''
        else:
            anz = get_points_for_velocity(d[2], d[3], v, pvz)

        s.append(f'REL {d[2]} {d[3]} {anz}')

    return '\n'.join(s)


def generate_hatch_data(data, rest=False, v=None, pvz=None):
    slist = []
    for d in data:
        s = []
        if v is None and pvz is None:
            anz = ''
        else:
            anz = get_points_for_velocity(d[2], d[3], v, pvz)
        s.append(f'ABS {d[0]} {d[1]}')
        s.append(f'REL {d[2]} {d[3]} {anz}')
        if rest:
            s.append(f'REL {d[4]} {d[5]} {anz}')
            s.append(f'REL {d[6]} {d[7]} {anz}')
            s.append(f'REL {d[8]} {d[9]} {anz}')

        s = '\n'.join(s)
        slist.append(s)

    string = '\n'.join(slist)

    return string


def combine_arrays(arrays):
    return np.vstack(arrays)


def write_data(fname, sdir, data):
    # falls das Verezichnis noch nicht existiert
    hF.create_directory_if_needed(sdir)

    dest = os.path.join(sdir, fname)

    with open(dest, "w") as f:
        f.write(data)


def generate_output(strings, comment='default'):
    comment_string = []
    if comment == 'default':
        pass
    else:
        comment_string.append(comment)

    comment_string.append('# VECTOR\nDATA')

    comment_string = '\n'.join(comment_string)

    figure_data = '\n'.join(strings)

    output = '\n'.join([comment_string, figure_data, 'END\nEOF'])

    return output


def get_outbox(layerdata):
    x_vals = np.hstack((layerdata[:, 0], layerdata[:, 2]))
    y_vals = np.hstack((layerdata[:, 1], layerdata[:, 3]))
    x_min = np.min(x_vals)
    x_max = np.max(x_vals)
    y_min = np.min(y_vals)
    y_max = np.max(y_vals)

    return x_min, x_max, y_min, y_max


if __name__ == '__main__':
    file = 'data/testfig.cli'

    hatchlist, arrows = convert_hatches(*load_data(file))

