import json

def load_street_file(file_path):
    street_data = {}
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    for i in data["Nodes"]:
        street_data[i["Name"]] = [i["Accessible"], i["Neighbours"]]
    
    return street_data

def print_accessible_stations(street_data):    
    accessible_stations = []
    
    for key in street_data:
        if(street_data[key][0]):
            accessible_stations.append(key)
    
    print(', '.join(accessible_stations))

def main():
    street_data = load_street_file("1a.json")
    print_accessible_stations(street_data)
    

if __name__ == "__main__":
    main()
    