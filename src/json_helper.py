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
    print("Loading file:", BASE_PATH + endpoint + ".json")
    with open(BASE_PATH + endpoint + ".json") as file:
        try:
            return json.load(file), True
        except ValueError:
            return {}, False


def update_json_value(endpoint, keys, value):
    """
    Loads and updates a value in the json at the given endpoint
    :param endpoint: String referring to the file_name
    :param keys: A list off all keys in ascending order
    :param value: The value that's supposed to be placed or updated
    :return: True if successful, otherwise False
    """
    data, _ = load_json_from_endpoint(endpoint)
    dump_data = data
    for i in range(len(keys) - 1):
        key = keys[i]
        if key not in data:
            data[key] = {}
        data = data[key]
    data[keys[-1]] = value
    with open(BASE_PATH + endpoint + ".json", 'w') as file:
        json.dump(dump_data, file)
    print("Updated file {} with {}".format(endpoint, dump_data))
    return True
