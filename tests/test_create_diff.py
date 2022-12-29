import os
import json
import pytest

import yaml 
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from gendiff.create_diff import generate_diff


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


# source data
plain_json1 = json.load(open(get_fixture_path('file1.json')))
plain_json2 = json.load(open(get_fixture_path('file2.json')))
plain_yaml1 = yaml.load(open(get_fixture_path('plain_yaml1.yaml')), Loader=Loader)
plain_yaml2 = yaml.load(open(get_fixture_path('plain_yaml2.yaml')), Loader=Loader)

# expected result
plain_expected = read(get_fixture_path('plain.txt')) 


def test_plain_json():
    assert generate_diff(plain_json1, plain_json2) == plain_expected

def test_plain_yaml():
    assert generate_diff(plain_yaml1, plain_yaml2) == plain_expected