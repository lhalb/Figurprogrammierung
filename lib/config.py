import json
import os
import configparser
from lib import helperFunctions as hF


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


def save_parameters(p, dest, section):
    if not os.path.exists(dest):
        os.makedirs(dest)
    config = configparser.ConfigParser()
    config[section] = p

    fname = dest + '/para.ini'

    mode = hF.get_mode(fname)
    with open(fname, mode) as cf:
        config.write(cf)
