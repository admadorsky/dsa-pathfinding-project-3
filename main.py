import osmnx as ox
import networkx as nx
import matplotlib
import csv
import math
from Dijkstra import Dijkstra


def main():
    G = ox.graph_from_place("Rome, Italy", network_type="drive")
    M = ox.utils_graph.get_undirected(G)

    # Extract nodes from the graph
    nodes = G.nodes()

    # initialize storage variables
    x_min = 999.000
    y_min = 999.000
    x_max = 0.00000
    y_max = 0.00000

    # find (absolute value) min and max values for x and y coords
    for node, data in nodes(data=True):
        # calculate minimums
        if data['x'] + 90 < x_min:
            x_min = data['x'] + 90
        if data['y'] + 90 < y_min:
            y_min = data['y'] + 90
        # calculate maximums
        if data['x'] + 90 > x_max:
            x_max = data['x'] + 90
        if data['y'] + 90 > y_max:
            y_max = data['y'] + 90

    viz_scale = y_max - y_min

    # Normalize x and y + Write nodes to a CSV file
    with open('nodes.csv', 'w', newline='') as csvfile:
        fieldnames = ['node_id', 'x', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        index = 0

        # Write node data
        for node, data in nodes(data=True):
            # calculate scale factors for mercator projection
            c = 0.0001120378
            angle_rad = abs(data['y']) * 0.0175
            x_scale_factor = math.sqrt(1 - (abs(data['y']) / 90) ** 2)
            y_scale_factor = (1 + c * (math.cos(2 * angle_rad) - 1)) / math.cos(angle_rad)
            print("x: ", x_scale_factor)
            print("y: ", y_scale_factor)
            # normalize x and y
            new_x = (((data['x'] + 90) - x_min) * x_scale_factor) / viz_scale
            new_y = ((((data['y'] + 90) - y_min) * y_scale_factor) / viz_scale) * (1 - (data['y'] / 900))
            # write data
            writer.writerow({'node_id': index, 'x': new_x, 'y': new_y})

            index = index + 1

    # Initialize an empty dictionary to store the adjacency lists
    adj_list_with_weights = {}
    adj_list = {}
    adj_list_i = {}
    indeces = {}
    # Initialize index counter
    n = 0

    # Iterate over nodes in the graph
    for node in G.nodes():
        indeces[node] = n
        n = n + 1

    for node in G.nodes():
        # Get the neighbors and edge attributes for each node
        neighbors_and_weights = []
        neighbors = []
        for neighbor, data in G[node].items():
            # Extract 'length' from the AtlasView
            length = data.get(0, {}).get('length', None)
            if length is not None:
                neighbors_and_weights.append((indeces[neighbor], length))
            neighbors.append((neighbor))

        # Add the node and its list of neighbors with weights to each dictionary
        adj_list_with_weights[node] = neighbors_and_weights
        adj_list[node] = neighbors

    for node2 in adj_list:
        indexed_neighbors = []
        for neighbor2 in adj_list[node2]:
            indexed_neighbors.append(indeces[neighbor2])
        key = indeces[node2]
        adj_list_i[key] = indexed_neighbors

    # Write indexed adjacency list without weights to a CSV file
    with open('adj_list.csv', 'w', newline='') as csvfile:
        fieldnames = ['node_index', 'neighbors\' indeces']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write adjacency list
        for node3, neighbors in adj_list_i.items():
            writer.writerow({'node_index': node3, 'neighbors\' indeces': neighbors})

    # Write adjacency list with weights to a CSV file
    with open('adj_list_with_weights.csv', 'w', newline='') as csvfile2:
        fieldnames2 = ['node_id', 'neighbors_with_weights']
        writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames2)

        # Write the header
        writer2.writeheader()

        # Write adjacency list with weights data
        for node4, neighbors_and_weights in adj_list_with_weights.items():
            writer2.writerow({'node_id': indeces[node4], 'neighbors_with_weights': neighbors_and_weights})

    # result_to_visualize = Dijkstra(adj_list_with_weights, 84714023, 2654104462, 9999999999999999)

if __name__ == '__main__':
    main()