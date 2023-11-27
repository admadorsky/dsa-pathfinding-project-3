import bpy
import csv
import pathlib
from importlib.machinery import SourceFileLoader

dijkstra = SourceFileLoader("Dijkstra", r"C:\Users\admadorsky\Desktop\DSA\Project 3\Dijkstra.py").load_module()

# get csv file location
file_loc = pathlib.Path(__file__).parent.resolve()
folder = pathlib.Path(file_loc).parent.resolve()

# open nodes.csv and store it in object "nodes"
nodes = pathlib.Path(folder).joinpath('nodes.csv')
# open adj_list.csv and store it in object "adj_list"
adj_list_p = pathlib.Path(folder).joinpath('adj_list.csv')
#open adj_list_with_weights.csv and store it in object "adj_list_with_weights"
adj_list_with_weights = pathlib.Path(folder).joinpath("adj_list_with_weights.csv")

gpencil_data = bpy.data.grease_pencils.new("GPencil")
gpencil = bpy.data.objects.new(gpencil_data.name, gpencil_data)
bpy.context.collection.objects.link(gpencil)

gp_layer = gpencil_data.layers.new("base")
gp_frame = gp_layer.frames.new(bpy.context.scene.frame_current)

vertices = []
edges = []
adj_dict = dict()

# collect necessary data from nodes.csv
with open(nodes, 'r') as csvfile:
    # initialize csv reader object
    datareader = csv.reader(csvfile)
    # skip header
    next(datareader)
    # initialize vertex counter
    num_nodes = 0
    for row in datareader:
        vertices.append((float(row[1]) * 10, float(row[2]) * 10, 0))
        num_nodes = num_nodes + 1

# collect necessary data from adj_list.csv
with open(adj_list_p, 'r') as csvfile:
    # initialize csv reader object
    datareader2 = csv.reader(csvfile)
    # skip header
    next(datareader2)
    # initialize edge counter
    num_edges = 0
    # count number of edges in map & populate edges[] with info from adj_list
    for row in datareader2:
        neighbors = row[1].split()
        neighbors[0] = neighbors[0][1:]
        for neighbor in neighbors:
            if len(neighbor) > 1:
                edges.append((int(row[0]), int(neighbor[:-1])))
                num_edges = num_edges + 1
                
# collect necessary data from adj_list_with_weights.csv
with open(adj_list_with_weights, 'r') as csvfile:
    # initialize csv reader object
    datareader3 = csv.reader(csvfile)
    # skip header
    next(datareader3)
    for row in datareader3:
        neighbors_str_dirty = row[1].split()
        neighbors_str_clean = []
        i = 0
        for neighbor_data in neighbors_str_dirty:
            neighbors_str_clean.append(neighbors_str_dirty[i].translate({ord(x): None for x in '"(),[] '}))
            i = i + 1
            
        neighbors_dict = dict()
        j = 0
        for neighbor_data in neighbors_str_clean:
            if j < (len(neighbors_str_clean) - 1):
                neighbors_dict[int(neighbors_str_clean[j])] = float(neighbors_str_clean[j + 1])
                j = j + 2
            
        adj_dict[int(row[0])] = neighbors_dict
               
base_mat = bpy.data.materials.new(name='Black')
bpy.data.materials.create_gpencil_data(base_mat)
gpencil.data.materials.append(base_mat)

for edge in edges: 
    # create a new stroke object
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.line_width = 6
    gp_stroke.start_cap_mode = 'ROUND'
    gp_stroke.end_cap_mode = 'ROUND'
    # add start and end points
    gp_stroke.points.add(count = 2)
    gp_stroke.points[0].co = (vertices[edge[0]][0] - 5.0, 0.0, vertices[edge[0]][1] - 5.0)
    gp_stroke.points[0].vertex_color = (0.2745, 0.4666, 0.4823, 0.2)
    gp_stroke.points[1].co = (vertices[edge[1]][0] - 5.0, 0.0, vertices[edge[1]][1] - 5.0)
    gp_stroke.points[1].vertex_color = (0.2745, 0.4666, 0.4823, 0.2)
    
# create a new stroke object
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.line_width = 6
    gp_stroke.start_cap_mode = 'ROUND'
    gp_stroke.end_cap_mode = 'ROUND'
    # add start and end points
    gp_stroke.points.add(count = 2)
    
result = dijkstra.Dijkstra(adj_dict, 100, 26734, 1000)

for node in result:
    for edge in adj_dict[node].keys():
        # create a new stroke object
        gp_stroke2 = gp_frame.strokes.new()
        gp_stroke2.line_width = 8
        gp_stroke2.start_cap_mode = 'ROUND'
        gp_stroke2.end_cap_mode = 'ROUND'
        # add start and end points
        gp_stroke2.points.add(count = 2)
        gp_stroke2.points[0].co = (vertices[node][0] - 5.0, 0.0, vertices[node][1] - 5.0)
        gp_stroke2.points[0].vertex_color = (0.1137, 0.7373, 0.8588, 1.0)
        gp_stroke2.points[1].co = (vertices[edge][0] - 5.0, 0.0, vertices[edge][1] - 5.0)
        gp_stroke2.points[1].vertex_color = (0.1137, 0.7373, 0.8588, 1.0)