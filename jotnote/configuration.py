#!/usr/bin/env python3

import json
import os

directory_path = os.path.dirname(__file__)
configuration_path = os.path.join(directory_path, "config.json")


def create_configuration_file_if_not_exists():
    if os.path.exists(configuration_path):
        return

    default_configuration = {
        "limit": 10,
        "orderby": "modification"
    }
    with open(configuration_path, "w") as config_file:
        json.dump(default_configuration, config_file)


def get_configuration():
    create_configuration_file_if_not_exists()
    with open(configuration_path) as config_file:
        configuration = json.load(config_file)
    return configuration


def save_configuration(configuration):
    create_configuration_file_if_not_exists()
    with open(configuration_path, "w") as config_file:
        json.dump(configuration, config_file)
