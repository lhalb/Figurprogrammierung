import json


def load_config(fname):
    with open(fname) as json_data_file:
        data = json.load(json_data_file)

    return data


def save_config(fname, data):
    with open(fname, "w") as outfile:
        json.dump(data, outfile)
