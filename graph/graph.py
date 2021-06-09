import json
import numpy as np
class Vertex() :
    #only with key
    def __init__(self, key, index):
        self.key = key #names
        self.index = index 

    def __str__(self):
        return self.key

class graph() : 
    # using an adjacency matrix method because of large number of edges
    
    def __init__(self, max_vertexes=100):
        #max_vertexes : the total number of people
        self.matrix = [[0] * max_vertexes for _ in range(max_vertexes)]  # 2d array 
        self.num_vertexes = 0  # current number of vertexes
        self.vertexes = {}  # vertex dict
        self.i_to_key = []  # list of keys to look up from index

    def add_vertex(self, key):
        """ add vertex named key if it is not already in graph"""
        if self.num_vertexes == self.max_vertexes :
            print("max vertexes reached, cannot add more!") # It may create the two vertex to represent the same person.
            raise 
        if key not in self.vertexes:
            self.i_to_key.append(key)
            i = self.num_vertexes
            self.vertexes[key] = Vertex(key, i)
            self.num_vertexes = i + 1

    def add_edge(self, from_key, to_key, weight=1):
        """ create vertexes if needed and then set weight to 1"""
        # we could do the operation of add_edge(self,self) -> set weight to 1
        #self.add_vertex(from_key)
        #self.add_vertex(to_key)
        self.matrix[self.vertexes[from_key].index][self.vertexes[to_key].index] = weight
        self.matrix[self.vertexes[to_key].index][self.vertexes[from_key].index] = weight

    def get_vertex(self, key):
        return self.vertexes[key]

    def get_vertices(self):
        """returns the list of all vertices in the graph."""
        return self.vertexes.values()

    def __contains__(self, key):
        return key in self.vertexes

    def edges(self, from_key):
        """ return list of all edges from vertex_key """
        to_dim = self.matrix[self.vertexes[from_key].index]
        return to_dim
        
if __name__=="__main__":
    mygraph = graph()
    
    with open("data.json","r") as f:
        raw_data = json.load(f)
#print(raw_data)