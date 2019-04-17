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
    with open(BASE_PATH + endpoint + ".json") as file:
        data = json.load(file)
    return data


def update_json_value(endpoint, keys, value):
    """
    Loads and updates a value in the json at the given endpoint
    :param endpoint: String referring to the file_name
    :param keys: A list off all keys in ascending order
    :param value: The value that's supposed to be placed or updated
    :return: True if successful, otherwise False
    """
    print("Updating {} in file {} with {}".format(keys, endpoint, value))
    data = load_json_from_endpoint(endpoint)
    dump_data = data
    for i in range(len(keys) - 1):
        key = keys[i]
        if key not in data:
            data[key] = {}
        data = data[key]
    data[keys[-1]] = value
    json.dump(dump_data, open(BASE_PATH + endpoint + ".json", 'w'))
    return True
