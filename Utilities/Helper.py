import json

def read_json(fname):
    with open(fname, "r") as f:
        return json.loads(f.read())

def write_json(data,fname):

    with open(fname, "w") as f:
        f.write(json.dumps(data))