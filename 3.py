import json
from heapq import *
import sys

'''
Here is the pseudo code for dijkstra: a common shortest path algorithm
'''


class Node:
    def __init__(self, name, accessible, coordinates, neighbours, prev, dist, num_ia=0, num_a=0):
        self.name = name
        self.accessible = accessible
        self.coordinates = coordinates
        self.neighbours = neighbours

        self.prev = prev
        self.dist = dist
        
        self.num_ia = num_ia
        self.num_a = num_a
        
    def __lt__(self, other):
        return self.dist < other.dist

def calc_total_E(G):
    total_num_edges = 0
    for key in G:
        total_num_edges += len(G[key].neighbours)
    return total_num_edges

def calc_total_V(G):
    return len(G)

def calc_p_ia(G):
    total_num_ia = 0
    for key in G:
        if not G[key].accessible:
            total_num_ia += 1
    return total_num_ia/calc_total_V(G)

def calc_p_a(G):
    total_num_a = 0
    for key in G:
        if G[key].accessible:
            total_num_a += 1
    return total_num_a/calc_total_V(G)

def calc_avg_d_ia(G):
    total_d_ia = 0
    for node in G:
        for neighbour in G[node].neighbours:
            if not G[neighbour["Name"]].accessible:
                total_d_ia += neighbour["Distance"]
    return total_d_ia/calc_total_E(G)

def calc_avg_d_a(G):
    total_d_a = 0
    for node in G:
        for neighbour in G[node].neighbours:
            if G[neighbour["Name"]].accessible:
                total_d_a += neighbour["Distance"]
    return total_d_a/calc_total_E(G)

def calc_avg_path_length(total_E, total_V):
    return total_E/(total_V*(total_V-1))

def calc_expected_nodes_left(num_ia, num_a, total_E, total_V):
    avg_path_length = calc_avg_path_length(total_E, total_V)
    return max((avg_path_length - (num_ia + num_a) -1), 1)

def calc_p_over(num_ia, num_a, p_ia, p_a, current_accessible, total_E, total_V):
    expected_nodes_left = calc_expected_nodes_left(num_ia, num_a, total_E, total_V)
    expected_ia_nodes = num_ia + expected_nodes_left*p_ia
    expected_a_nodes = num_a + expected_nodes_left*p_a
    if current_accessible:
        expected_a_nodes += 1
    else:
        expected_ia_nodes += 1
    return expected_ia_nodes/expected_a_nodes

def calc_expected_d_left(num_ia, num_a, total_E, total_V, p_ia, p_a, avg_d_ia, avg_d_a):
    expected_nodes_left = calc_expected_nodes_left(num_ia, num_a, total_E, total_V)
    return (p_ia*avg_d_ia + p_a*avg_d_a) * expected_nodes_left

def heuristic_func(d_current, d_next, num_ia, num_a, total_E, total_V, p_ia, p_a, avg_d_ia, avg_d_a, current_accessible):
    expected_nodes_left = calc_expected_nodes_left(num_ia, num_a, total_E, total_V)
    expected_ia_nodes = num_ia + expected_nodes_left*p_ia
    expected_a_nodes = num_a + expected_nodes_left*p_a
    expected_d_left = calc_expected_d_left(num_ia, num_a, total_E, total_V, p_ia, p_a, avg_d_ia, avg_d_a)
    
    plus_5_score = d_current + d_next + expected_d_left + 5*expected_ia_nodes
    double_score = 2*(d_current + d_next + expected_d_left)
    
    p_over = calc_p_over(num_ia, num_a, p_ia, p_a, current_accessible, total_E, total_V)
    if p_over <= 1:
        return plus_5_score
    else:
        return max(plus_5_score, double_score)

def dijkstra(G, source, dest):
    #initialize
    for key in G:
        G[key].dist = int(sys.maxsize)
        G[key].prev = None

    G[source].dist = 0

    Q = construct_q(G)

    non_accessible_count = 0
    total_node_count = 0
    while len(Q) > 0:	# main loop
        current_node = heappop(Q)
        total_node_count += 1

        if not current_node.accessible:
            non_accessible_count += 1
            current_node.num_ia += 1
        else:
            current_node.num_a += 1

        if current_node.name == dest:
            path = []
            path.append(current_node.name)

            prev = current_node.prev
            while prev != source:
                path.append(prev)
                prev = G[prev].prev
            path.append(source)
            return path[::-1]

        for neighbour in current_node.neighbours:
            if G[neighbour["Name"]].accessible:
                current_dist = current_node.dist + neighbour["Distance"]
            else:
                # current_dist = current_node.dist + max(neighbour["Distance"]+5, 2*neighbour["Distance"])
                # current_dist = current_node.dist + neighbour["Distance"]+5
                if float(non_accessible_count/total_node_count) > 0.5:
                    current_dist = current_node.dist + max(neighbour["Distance"]+5, 2*neighbour["Distance"])
                else:
                    current_dist = current_node.dist + neighbour["Distance"]+5
                # total_E = calc_total_E(G)
                # total_V = calc_total_V(G)
                # avg_d_ia = calc_avg_d_ia(G)
                # avg_d_a = calc_avg_d_a(G)
                # p_ia = calc_p_ia(G)
                # p_a = calc_p_a(G)
                # current_dist = heuristic_func(current_node.dist, neighbour["Distance"], current_node.num_ia, current_node.num_a, total_E, total_V, p_ia, p_a, avg_d_ia, avg_d_a, current_node.accessible)

            if current_dist < G[neighbour["Name"]].dist:	# Relax
                G[neighbour["Name"]].dist = current_dist
                G[neighbour["Name"]].prev = current_node.name
                G[neighbour["Name"]].num_a = current_node.num_a
                G[neighbour["Name"]].num_ia = current_node.num_ia
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
                               int(sys.maxsize),
                               0,
                               0)
    return G

def construct_q(street_graph):
    Q = []
    for street_name in street_graph:
        heappush(Q, street_graph[street_name])
    
    return Q


def open_input_file(input_file_path):
    with open(input_file_path, "r") as input_file:
        input_content = input_file.read()
        input_content = input_content.split("\n")[:-1] # discard the last line as it is empty
        
        for i, line in enumerate(input_content):
            source_and_destination = line.split(',')
            input_content_dict = {"source": source_and_destination[0],
                                  "dest": source_and_destination[1]}
            input_content[i] = input_content_dict

        return input_content

def main():
    street_data = load_street_file("./3.json")
    street_graph = construct_graph(street_data)
    
    input_content = open_input_file("3.in")
    
    for input_line in input_content:
        path = dijkstra(street_graph, input_line["source"], input_line["dest"])
        print(", ".join(path), end=", ")
        print(get_final_distance(street_graph, path, True))

if __name__ == "__main__":
    main()
