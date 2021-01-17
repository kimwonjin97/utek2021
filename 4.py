import json
from heapq import *
import sys
import itertools

class Node:
    def __init__(self, name, accessible, coordinates, neighbours, prev, dist):
        self.name = name
        self.accessible = accessible
        self.coordinates = coordinates
        self.neighbours = neighbours

        self.prev = prev
        self.dist = dist
        
    def __lt__(self, other):
        return self.dist < other.dist


def dijkstra(G, source, dest):
    #initialize
    for key in G:
        G[key].dist = int(sys.maxsize)
        G[key].prev = None

    G[source].dist = 0

    Q = construct_q(G)

    while len(Q) > 0:	# main loop
        current_node = heappop(Q)

        if current_node.name == dest:
            path = []
            path.append(current_node.name)

            prev = current_node.prev
            while prev != source:
                path.append(prev)
                if prev is None:
                    break
                prev = G[prev].prev
            path.append(source)
            return path[::-1]

        for neighbour in current_node.neighbours:
            current_dist = current_node.dist + neighbour["Distance"]
            if current_dist < G[neighbour["Name"]].dist:	# Relax 
                G[neighbour["Name"]].dist = current_dist
                G[neighbour["Name"]].prev = current_node.name
                heapify(Q)
    return []

def get_final_distance(G, path, accessibility):
    total_nodes = len(path)
    non_accessible_count = 0
    true_dist = 0
    penalized_dist = 0
    for i in range(len(path)-1):
        for neighbour in G[path[i]].neighbours:
            if neighbour["Name"] == path[i+1]:
                current_dist = neighbour["Distance"]
                true_dist += current_dist
                if not G[neighbour["Name"]].accessible:
                    current_dist += 5
                penalized_dist += current_dist

        if not G[path[i]].accessible:
            non_accessible_count += 1
    if not G[path[-1]].accessible:
        non_accessible_count += 1
    
    if accessibility:
        if float(non_accessible_count/total_nodes) > 0.5:
            return max(true_dist*2, penalized_dist)
        else:
            return penalized_dist
    else:
        return true_dist


def load_street_file(file_path):
    street_data = {}
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    
    return data["Nodes"]

def construct_graph(street_data):
    G = {}
    for node in street_data:
        G[node["Name"]] = Node(node["Name"], 
                               node["Accessible"], 
                               node["Coordinates"], 
                               node["Neighbours"], 
                               None, 
                               int(sys.maxsize))
    return G

def construct_q(street_graph):
    Q = []
    for street_name in street_graph:
        heappush(Q, street_graph[street_name])
    
    return Q


def open_input_file(input_file_path):
    with open(input_file_path, "r") as input_file:
        input_content = input_file.read()
        input_content = input_content.split("\n")
        
        for i, line in enumerate(input_content):
            destinations = line.split(',')
            input_content[i] = destinations

        return input_content

     
        
def main():
    street_data = load_street_file("./4.json")
    street_graph = construct_graph(street_data)
    
    input_content = open_input_file("4.in")

    for input_line in input_content:
        final_path = []
        final_dist = int(sys.maxsize)
        perms = itertools.permutations(input_line)
        for perm in iter(perms):
            total_path = []
            for i in range(len(perm)-1):
                sub_path = dijkstra(street_graph, perm[i], perm[i+1])
                if i > 0:
                    total_path.extend(sub_path[1:])
                else:
                    total_path.extend(sub_path)
            sub_path = dijkstra(street_graph, perm[-1], perm[0])
            total_path.extend(sub_path[1:])
            curr_dist = get_final_distance(street_graph, total_path, False)
            if curr_dist < final_dist:
                final_dist = curr_dist
                final_path = total_path
        print(", ".join(final_path), end=", ")
        print(final_dist)


if __name__ == "__main__":
    main()
