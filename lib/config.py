import json
import os
import configparser


def load_config(fname):
    with open(fname) as json_data_file:
        data = json.load(json_data_file)

    return data


def save_config(fname, data):
    with open(fname, "w") as outfile:
        json.dump(data, outfile)


def load_parameters(dest, filename='para.ini'):
    config = configparser.ConfigParser()
    fname = dest + '/' + filename
    config.read(fname)
    return config


def save_parameters(p, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    config = configparser.ConfigParser()
    config['PARAMS'] = p

    fname = dest + '/para.ini'

    with open(fname, 'w') as cf:
        config.write(cf)
