#!/usr/bin/env python3

import json
import os

application_data_dir = os.path.join(os.getenv("HOME"), ".jotnote")
configuration_path = os.path.join(application_data_dir, "config.json")


def create_configuration_file_if_not_exists(function_using_configuration_file):
    def decorator(*args, **kwargs):
        if os.path.exists(configuration_path):
            return function_using_configuration_file(*args, **kwargs)

        os.makedirs(application_data_dir, exist_ok=True)
        default_configuration = {
            "limit": 10,
            "orderby": "modification"
        }

        with open(configuration_path, "w") as config_file:
            json.dump(default_configuration, config_file)

        return function_using_configuration_file(*args, **kwargs)

    return decorator


@create_configuration_file_if_not_exists
def get_configuration():
    with open(configuration_path) as config_file:
        configuration = json.load(config_file)
    return configuration


@create_configuration_file_if_not_exists
def save_configuration(configuration):
    with open(configuration_path, "w") as config_file:
        json.dump(configuration, config_file)
