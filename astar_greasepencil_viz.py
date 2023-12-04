import bpy
import csv
import pathlib
import math
from importlib.machinery import SourceFileLoader

a_star = SourceFileLoader("a_star", r"C:\Users\admadorsky\Desktop\DSA\Project 3\a_star.py").load_module()

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

glow_fx1 = gpencil.shader_effects.new('glow', 'FX_GLOW')
glow_fx1.samples = 32
glow_fx1.size.x = 150.0
glow_fx1.size.y = 150.0
glow_fx1.opacity = 0.6

gp_layer = gpencil_data.layers.new("base")
gp_frame = gp_layer.frames.new(1)

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
    
source = 50000
destination = 55084
    
# 280 for Dijkstra
# ??? for Astar
iterations_to_find = 200

for iteration in range(iterations_to_find): 
    
    # create new grease pencil object
    gpencil_data2 = bpy.data.grease_pencils.new("GPencil")
    gpencil2 = bpy.data.objects.new(gpencil_data2.name, gpencil_data2)
    bpy.context.collection.objects.link(gpencil2)
    gp_layer2 = gpencil_data2.layers.new("viz")
    gp_frame_progress = gp_layer2.frames.new(iteration + 1)
    
    glow_fx = gpencil2.shader_effects.new('glow', 'FX_GLOW')
    glow_fx.samples = 32
    glow_fx.size.x = 150.0
    glow_fx.size.y = 150.0
    glow_fx.opacity = 0.6
    
    progress_mat = bpy.data.materials.new(name='Black')
    bpy.data.materials.create_gpencil_data(progress_mat)
    gpencil2.data.materials.append(progress_mat)
    
    result_distances = {}   
    result = a_star.astar(adj_dict, source, destination, iteration + 1)

    max_dist = 0.00001

    for node in result:
        x_dist = vertices[source][0] - vertices[node][0]
        y_dist = vertices[source][1] - vertices[node][1]
        result_distances[node] = math.sqrt((x_dist ** 2) + (y_dist ** 2))
        if result_distances[node] > max_dist:
            max_dist = result_distances[node]

    for node in result:
        for edge in adj_dict[node].keys():
            # create a new stroke object
            gp_stroke_progress = gp_frame_progress.strokes.new()
            gp_stroke_progress.line_width = 8
            gp_stroke_progress.start_cap_mode = 'ROUND'
            gp_stroke_progress.end_cap_mode = 'ROUND'
            # calculate colors based on distance from source
            gp_stroke_progress.points.add(count = 2)
            fac = math.sqrt(result_distances[node] / max_dist)
            red = 0.2745 - ((0.2745 - 0.1137) * fac)
            green = 0.4666 + ((0.8588 - 0.4666) * fac)
            blue = 0.4823 + ((0.4862 - 0.4823) * fac)
            # add start and end points
            gp_stroke_progress.points[0].co = (vertices[node][0] - 5.0, 0.0, vertices[node][1] - 5.0)
            gp_stroke_progress.points[0].vertex_color = (red, green, blue, 0.2 + ((1.0 - 0.2) * fac))
            gp_stroke_progress.points[1].co = (vertices[edge][0] - 5.0, 0.0, vertices[edge][1] - 5.0)
            gp_stroke_progress.points[1].vertex_color = (red, green, blue, 0.2 + ((1.0 - 0.2) * fac))
        
    # draw source node
    gp_stroke_source = gp_frame_progress.strokes.new()
    gp_stroke_source.line_width = 35
    gp_stroke_source.start_cap_mode = 'ROUND'
    gp_stroke_source.end_cap_mode = 'ROUND'
    gp_stroke_source.points.add(count = 1)
    gp_stroke_source.points[0].co = (vertices[source][0] - 5.0, 0.0, vertices[source][1] - 5.0)
    gp_stroke_source.points[0].vertex_color = (0.1137, 0.8588, 0.4862, 1.0)
    
    gp_frame_finished = gp_layer2.frames.new(iteration + 2)
