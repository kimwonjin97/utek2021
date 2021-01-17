import heapq
import json
from collections import deque

def dijkstra(graph, start, end):
    distances = {vertex: [float('inf'), start] for vertex in graph}

    distances[start] = [0, start]

    q = []
    heapq.heappush(q, [distances[start][0], start])

    while q:
        c_d, c_v = heapq.heappop(q)

        if distances[c_v][0] < c_d:
            continue

        for a, w in graph[c_v].items():
            distance = c_d + w
            
            if distance < distances[a][0]:
                distances[a] = [distance, c_v]
                heapq.heappush(q, [distance, a])

    path = end
    path_output = end + ','
    while distances[path][1] != start:
        path_output += distances[path][1] + ','
        # print(path_output)
        path = distances[path][1]
    
    path_output += start
    x = path_output.split(",")
    x.reverse()
    return x, distances

def main():
    with open('./3.json') as json_file:
        data_raw = json.load(json_file)
    input_graph = {}
    for i, data in enumerate(data_raw["Nodes"]):
    
        temp = {}
        for j in data["Neighbours"]:
            temp[j["Name"]] = j["Distance"]

        input_graph[data["Name"]] = temp

    
    route, distance = dijkstra(input_graph, 'Queens', 'Yonge and Dundas')

    res = ""
    for i in route:
        res += i + ', '
    res += str(distance['Yonge and Dundas'][0])
    print(res)
   

if __name__ == "__main__":
    main()

