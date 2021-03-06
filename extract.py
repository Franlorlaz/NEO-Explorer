"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import pathlib

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path=pathlib.Path('./data/neos.csv')):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A list of `NearEarthObject`s.
    """
    neos = []  # A better option: neos = {} (read EXTENSIONS.md)
    with open(neo_csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            # neos={} ==> neos[line['pdes']] = NearEarthObject(**line)
            neos.append(NearEarthObject(**line))
    return neos


def load_approaches(cad_json_path=pathlib.Path('./data/cad.json')):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A list of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as file:
        read = json.load(file)
    appr = [CloseApproach(**dict(zip(read['fields'], data))) for data in read['data']]
    return appr
