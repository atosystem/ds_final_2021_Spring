import json
import numpy as np
class Vertex() :
    #only with key
    def __init__(self, path, index):
        self.key = path #path
        self.value = set() #name
        #elf.index = index 

    def __str__(self):
        return self.key

class graph() : 
    # using an adjacency matrix method because of large number of edges
    
    def __init__(self, max_vertexes=50000):
        #max_vertexes : the total number of people
        #self.matrix = [[0] * max_vertexes for _ in range(max_vertexes)]  # 2d array 
        self.num_vertexes = 0  # current number of vertexes
        self.vertexes = {}  # vertex dict , path: Vertex object
        #self.i_to_key = []  # list of path_string to look up from index

    def add_vertex(self, path,name):
        """ add vertex named key if it is not already in graph"""
        """
        if self.num_vertexes == self.max_vertexes :
            print("max vertexes reached, cannot add more!") # It may create the two vertex to represent the same person.
            return 
        print(self.num_vertexes)
        """
        if path not in self.vertexes:
            #self.i_to_key.append(path)
            i = self.num_vertexes
            self.vertexes[path] = Vertex(path, i)
            self.vertexes[path].value.add(name)
            #self.num_vertexes = i + 1
        else:
            self.vertexes[path].value.add(name)
            
    #below is not helpful in this case
    def add_edge(self,danger_community,weight=1):
        #general graph method , but in this case, we will not use so much graph property
        """ create vertexes if needed and then set weight to 1"""
        # we could do the operation of add_edge(self,self) -> set weight to 1
        #self.add_vertex(from_key)
        #self.add_vertex(to_key)
        self.matrix[self.vertexes[from_key].index][self.vertexes[to_key].index] = weight
        self.matrix[self.vertexes[to_key].index][self.vertexes[from_key].index] = weight

    def get_vertex(self, path):
        return self.vertexes[path]

    def get_vertices(self):
        """returns the list of all vertices in the graph."""
        return self.vertexes.values()

    def __contains__(self, key):
        return key in self.vertexes

   
class graph_method :
    #This is a isolated vertice graph
    def __init__(self,sim_data):
        self.sim = sim_data
        #self.PeopleList = [] #list of Person_info object
        self.graph = graph()
        self.infected_path = []
        for i in sim_data["infected_people"]:
            #print(i)
            s = ""
            for j in range(6) :
                s += ((self.sim["people_list"])[i])[j]
            self.infected_path.append(s)  
        #print(self.infected_path)
    def create_all(self) :
        for i in self.sim["people_list"] :
            #print(self.graph.num_vertexes)
            s = ""
            for j in range(6) :
                s += ((self.sim["people_list"])[i])[j]
            self.graph.add_vertex(s,i)
            
    def solve(self) :
        target_set = set()
        for j in self.infected_path :
            #print(j)
            target_set = target_set.union((self.graph.vertexes[j]).value)
   
        return target_set
    def get_output(self):
        self.create_all()
        #print("test")
        ts = self.solve()
        #print(ts)
        output_name_list = []
        
        
        for i in ts :
            
            output_name_list.append(i)
        
        for j in self.sim["people_list"] :
            if j not in ts :
                output_name_list.append(j)
        
        return output_name_list
if __name__=="__main__":
    import json
    import numpy as np
    with open("../raw_data/init_data.json","r") as f:
        sim_data = json.load(f)
   
    
    
    Graph_Method = graph_method(sim_data)
    results = Graph_Method.get_output()
    #print(results)
  
 