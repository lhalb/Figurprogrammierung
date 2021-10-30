import os
import fnmatch
from itertools import groupby


# Function to use boolean masks on lists
def masklist(mylist, mymask):
    return [a for a, b in zip(mylist, mymask) if b]


def test_for_matching_files(directory, ftype=None):
    ret_val = [False] * len(directory)
    for i, d in enumerate(directory):
        files = os.listdir(d)
        if not files:
            continue
        if [ft for ft in ftype if fnmatch.filter(files, f'*{ft}')]:
            ret_val[i] = True

    return ret_val


def create_directory_if_needed(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return False


def delete_all_files_in_directory(path):
    # lösche alle alten dateien
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))


def get_mode(file):
    # Beim ersten Aufruf der CNC-Datei
    if not os.path.exists(file):
        mode = 'w'
    else:
        mode = 'a'

    return mode


def all_unique(x):
    return not len(x) > len(set(x))


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def get_filename(path):
    return os.path.split(path)[1].split('.')[0]