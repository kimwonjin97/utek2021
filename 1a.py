import json

def load_file(file_path):
    street_data = {}
    f = open(file_path,)

    data = json.load(f)
    for i in data["Nodes"]:
        print(i["Name"])
        street_data[i["Name"]] = [i["Accessible"], i["Neighbours"]]
        debug = 1

load_file('1a.json')
