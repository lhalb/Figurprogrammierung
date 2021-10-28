import os
import fnmatch


# Function to use boolean masks on lists
def masklist(mylist, mymask):
    return [a for a, b in zip(mylist, mymask) if b]


def test_for_matching_files(directory, ftype=None):
    ret_val = [False] * len(directory)
    for i, d in enumerate(directory):
        files = os.listdir(d)
        if [ft for ft in ftype if fnmatch.filter(files, f'*{ft}')]:
            ret_val[i] = True

    return ret_val


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
