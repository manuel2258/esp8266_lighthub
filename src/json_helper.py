import json

"""
Helps with loading / editing jsons from the config file folder
"""

BASE_PATH = "/configs/"


def load_json_from_endpoint(endpoint):
    """
    Loads a json config from the given endpoint
    BASE_PATH + endpoint -> file_path
    :param endpoint: String referring to the file_name
    :return:
    """
    try:
        with open(BASE_PATH + endpoint) as file:
            data = json.load(file)
            return data, True
    except FileNotFoundError:
        print("Could not load from: ", endpoint)
        return {}, False


def update_json_value(endpoint, keys, value):
    """
    Loads and updates a value in the json at the given endpoint
    :param endpoint: String referring to the file_name
    :param keys: A list off all keys in ascending order
    :param value: The value that's supposed to be placed or updated
    :return: True if successful, otherwise False
    """
    data, success = load_json_from_endpoint(endpoint)
    if not success:
        print("Could not found / update the file")
        return False

    for key in range(len(keys) - 1):
        data = data[key]
    data[keys[-1]] = value
    return True
