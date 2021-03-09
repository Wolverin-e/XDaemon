import json


def prettify(dict):
    """
        For prettifying a Dictionary object.
    """
    return json.dumps(dict, indent=2)
