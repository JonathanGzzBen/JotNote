import json
import os

configuration_filename = "config.json"

def create_configuration_file_if_not_exists():
    if os.path.exists(configuration_filename):
        return

    default_configuration = {
        "limit": 10
    }
    with open(configuration_filename, "w") as config_file:
        json.dump(default_configuration, config_file)

def get_configuration():
    create_configuration_file_if_not_exists()
    with open(configuration_filename) as config_file:
        configuration = json.load(config_file)
    return configuration

def save_configuration(configuration):
    create_configuration_file_if_not_exists()
    with open(configuration_filename, "w") as config_file:
        json.dump(configuration, config_file)
