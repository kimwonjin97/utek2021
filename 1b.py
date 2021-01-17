import json

def load_file(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    
    path_data = {}
    for i, data in enumerate(data["Paths"]):
        accessible_count = 0
        for node in data["Nodes"]:
            if node["Accessible"] is True:
                accessible_count += 1
        path_data[i+1] = accessible_count

    return path_data


def print_and_write_paths(path_data):

    path_ordered = sorted(path_data.items(), key=lambda x: x[1], reverse=True)

    accessible_stations = []
    for item in path_ordered:
        accessible_stations.append(item[0])

    list_string = map(str, accessible_stations)
    result = 'Path ' + ', Path '.join(list_string)
    
    with open("1b.out", "w") as save_f:
        save_f.write(result)

    print(result)


def main():
    path_data = load_file("./1b.json")
    print_and_write_paths(path_data)
    

if __name__ == "__main__":
    main()