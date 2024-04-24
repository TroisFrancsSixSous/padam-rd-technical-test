import random as rand
from input import parse_file
from matplotlib import pyplot as plt
import numpy as np
import math
from tqdm import tqdm

#Choose the instance:

hard_to_choose = True
islands = False
paris_map = False

#Choose the algorithm:

NN_algo = True
switch_algo = True

#Code

V,E = parse_file("instances/islands.txt")
#print(V, len(V)) #V is a list of tuples containing the coordinates x,y in a 2-D plan
#print(E) #E is  a list of tuples containing the two indexes of the vertices building the edge, the weigh of the edge and the coordinates of both vertices

#Display function for the solution

def display_solution(file, algo):
    vertices, edges = parse_file(file)
    tour, tour_dist = algo(file)
    x = [vertices[index][0] for index in tour]
    y = [vertices[index][1] for index in tour]
    plt.scatter(x,y, c='red')
    for i in range(len(tour) - 1):
        plt.plot([x[tour[i]], x[tour[i + 1]]], [y[tour[i]], y[tour[i + 1]]], color='blue')
    plt.plot([x[tour[-1]], x[tour[0]]], [y[tour[-1]], y[tour[0]]], color='blue')
    plt.show()
    print(tour_dist)
    pass

# 1- Greedy approach of nearest neighbors (NN_algo)

# def list_neighbors(edges, vertex): #intermediate function to calculate distances to neighbors of a vertex
#     """Parameters: a list of edges and the vertex
#     Result: a list of tuples of the neighbors of the vertex and the weights of the paths that leads to them"""
#     result = []
#     for edge in edges:
#         if edge[0]==vertex:
#             weighted_dist = edge[2]*math.dist(edge[3], edge[4])
#             result.append((edge[1], weighted_dist))
#         elif edge[1]==vertex:
#             weighted_dist = edge[2]*math.dist(edge[3], edge[4])
#             result.append((edge[0], weighted_dist))
#     return result
    

def dist_neighbors(V1, V2, edges): #intermediate function to calculate distances to neighbors of a vertex
    """Parameters: a list of edges and the two vertices
    Result: a float that is the weighted distance between V1 and V2"""
    #connected = False
    for edge in edges:
        if (edge[0]==V1 and edge[1]==V2) or (edge[0]==V2 and edge[1]==V1):
            #connected = True
            return edge[2]*math.dist(edge[3], edge[4]) #, connected # formula of weighted distance and bool that says wether the two vertices are connected
    return 10000 #, connected


def nearest_neighbor_solution(file):
    """
    Parameters: string containing the file name of a graph from the instances folder
    Result: a list of vertces in order of travel, ordered thanks to the nearest neighbor greedy procedure
    """
    vertices, edges = parse_file(file)
    num_vertices = len(vertices)
    starting_point = rand.randint(0,num_vertices-1) # begin the tour with a random starting point
    tour = [starting_point]
    tour_dist = 0
    pbar = tqdm(total=num_vertices)  # create a tqdm progression bar with total number of vertices 
    while len(tour)<num_vertices:
        last_visited = tour[-1] 
        min_dist = 100000
        nearest_neighbor = 0
        for explored in range(num_vertices): #TODO: can be optimized with a list of unvisited adresses
            if (explored not in tour):
                dist_to_explored = dist_neighbors(last_visited, explored, edges) #Paying atttention to calling this function once and only if the first condition is respected
                if(dist_to_explored<min_dist):
                    min_dist = dist_to_explored
                    nearest_neighbor = explored
        tour.append(nearest_neighbor)
        tour_dist += min_dist
        pbar.update(1)
    tour_dist += dist_neighbors(starting_point, tour[-1], edges)
    pbar.close()  # close tqdm progress bar
    return tour , tour_dist
    #TODO try to go through already visited path since it is pseudo-eulerian

if NN_algo:
    if hard_to_choose:  
        print(nearest_neighbor_solution("instances/hard_to_choose.txt")[0])
        display_solution("instances/hard_to_choose.txt", nearest_neighbor_solution)
    elif islands:
        print(nearest_neighbor_solution("instances/islands.txt")[0])
        display_solution("instances/islands.txt", nearest_neighbor_solution)
    elif paris_map:
        print(nearest_neighbor_solution("instances/paris_map.txt")[1])

# 2- Local research: switch vertices

def try_switching(tour, i,j, edges): # side effect function
    num_vertices = len(tour)
    current_dist = dist_neighbors(tour[i] , tour[(i+1)%num_vertices], edges) + dist_neighbors(tour[j], tour[(j+1)%num_vertices], edges)
    switched_dist = dist_neighbors(tour[i] , tour[j], edges) + dist_neighbors(tour[(i+1)%num_vertices], tour[(j+1)%num_vertices], edges)
    if current_dist > switched_dist:
        tour[(i+1)%num_vertices], tour[j] = tour[j], tour[(i+1)%num_vertices] # switch indexes if it makes the tour quicker
        return True
    return False
        
def switch_vertices_solution(file):
    vertices, edges = parse_file(file)
    tour = [_ for _ in range(len(vertices))]
    improvement_possible = True # tells if at least one switching was possible
    num_iter = 5000
    k = num_iter
    pbar = tqdm(total=num_iter) 
    while improvement_possible == True and k > 0:
        improvement_possible = False
        for i in range(len(tour)): 
            for j in range(i+2,len(tour)):
                if try_switching(tour, tour[i], tour[j], edges):
                    improvement_possible = True
                    break
            if improvement_possible == True:
                break
        k -= 1
        pbar.update(1)
    pbar.close()
    tour_dist = np.sum([dist_neighbors(tour[i], tour[(i+1)%len(tour)], edges) for i in range(len(tour))])
    return tour, tour_dist

if switch_algo:
    if hard_to_choose:  
        print(switch_vertices_solution("instances/hard_to_choose.txt")[0])
        display_solution("instances/hard_to_choose.txt", switch_vertices_solution)
    elif islands:
        print(switch_vertices_solution("instances/islands.txt")[0])
        display_solution("instances/islands.txt", switch_vertices_solution)
    elif paris_map:
        print(switch_vertices_solution("instances/paris_map.txt")[1])

#TODO implement k-means clustering methods for islands case before doing nearest neighbors
#TODO think about methods to go back on already visited vertices
#TODO debug the switching algorithm