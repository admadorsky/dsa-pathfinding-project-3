import bpy
import csv
import pathlib

# get csv file location
file_loc = pathlib.Path(__file__).parent.resolve()
folder = pathlib.Path(file_loc).parent.resolve()

# open nodes.csv and store it in object "nodes"
nodes = pathlib.Path(folder).joinpath('nodes.csv')
# open adj_list_with_weights.csv and store it in object "adj_list"
adj_list = pathlib.Path(folder).joinpath('adj_list.csv')

collection = bpy.data.collections['Collection']

# initialize storage
vertices = []
edges = []

# read vertex/intersection data
with open(nodes, 'r') as csvfile:
    # initialize csv reader object
    datareader = csv.reader(csvfile)
    # skip header
    next(datareader)
    # initialize vertex counter
    i = 0
    for row in datareader:
        vertices.append((float(row[1]) * 10, float(row[2]) * 10, 0))
        i = i + 1
        
with open(adj_list, 'r') as csvfile2:
    # initialize csv reader object
    datareader2 = csv.reader(csvfile2)
    # skip header
    next(datareader2)
    # initialize edge counter
    i2 = 0
    for row in datareader2:
        neighbors = row[1].split()
        neighbors[0] = neighbors[0][1:]
        
        for neighbor in neighbors:
            if len(neighbor) > 1:
                edges.append((int(row[0]), int(neighbor[:-1])))
                i2 = i2 + 1
        
new_mesh = bpy.data.meshes.new('data')
new_mesh.from_pydata(vertices, edges, [])
new_mesh.update()

print(i)

new_object = bpy.data.objects.new('data_graph', new_mesh)
collection.objects.link(new_object)