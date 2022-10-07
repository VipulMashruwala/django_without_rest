import json

def is_json(data):
    try: 
        py_dict = json.loads(data)
        valid = True
    except ValueError:
        valid = False
    return valid
