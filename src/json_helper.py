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
    :return: (to return json, successful)
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
    :return:
    """
    dump_data, _ = load_json_from_endpoint(endpoint)
    data = _get_data_at_key_end(dump_data, keys)
    data[keys[-1]] = value
    with open(BASE_PATH + endpoint + ".json", 'w') as file:
        json.dump(dump_data, file)


def remove_item_from_json(endpoint, keys):
    """
    Loads the json from the endpoint and removes the given key from the last point
    :param endpoint: The to load from endpoint
    :param keys: A List of keys to nest to
    :return:
    """
    dump_data, _ = load_json_from_endpoint(endpoint)
    data = _get_data_at_key_end(dump_data, keys)
    del data[keys[-1]]
    with open(BASE_PATH + endpoint + ".json", 'w') as file:
        json.dump(dump_data, file)


def _get_data_at_key_end(data, keys):
    for i in range(len(keys) - 1):
        key = keys[i]
        if key not in data:
            data[key] = {}
        data = data[key]
    return data
