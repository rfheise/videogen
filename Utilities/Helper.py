import json

def read_json(fname):
    with open(fname, "r") as f:
        return json.loads(f.read())