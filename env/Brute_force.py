# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 23:13:22 2021

@author: 王式珩
"""

class Person_info :
    def __init__(self,sim_data,name):
        self.name = name
        self.location = sim_data["people_list"][0][name]
        self.score = 0
        if name in sim_data["infected_people"] :
            self.is_infected = True
        else:
            self.is_infected = False
    def calculate_score(self,danger_path):
        #danger_path:list of infected_people list
        if self.is_infected :
            self.score = 100000000 #the highest danger
        else :
            #same store : get 3000 points
            #same road : get 200 points
            #same community : get 50 points
            #same city : get 5 points
            #same region : get 1 points
            #otherwise : get 0 points
            l = [0,1,5,50,200,3000]
            for danger in danger_path:
                in_same_store = True
                for i in range(1,6) :
                    #check overlap path
#                    print("self.location ", self.location)
#                    print("*******************************")
#                    print("danger ", danger)
                    if self.location[i] != danger[i] :
                        self.score += l[i-1]
                        in_same_store = False
                        break
                if in_same_store :
                    self.score += l[5]
    def __lt__(self,other):
        return self.score<other.score
    def __eq__(self,other):
        return self.score == other.score
    def __str__(self) :
        return self.name
    def get_score(self):
        return self.score 
    def get_name(self):
        return self.name
class Brute_Force :
    def __init__(self,sim_data) :
         self.sim = sim_data
         self.PeopleList = [] #list of Person_info object
         self.infected_path = []
         for i in sim_data["infected_people"]:
             self.infected_path.append(self.sim["people_list"][0][i])  
    def create_all(self) :
        for i in self.sim["people_list"][0] :
            self.PeopleList.append(Person_info(self.sim,i))
    def solve(self) :
        for i in self.PeopleList :
            i.calculate_score(self.infected_path)
        self.PeopleList.sort(reverse=True)
    def get_output(self):
        self.create_all()
        self.solve()
        output_name_list = []
        for i in self.PeopleList :
            output_name_list.append(i.get_name())
        return output_name_list
#if __name__=="__main__":
def Brute_force(sim_data):
#    import json
#    import numpy as np
#    import codecs
#    with open("../env/data.json","r") as f:
#    sim_data = json.load(codecs.open(r"C:\\Users\\王式珩\\Desktop\\資料結構\\final\\ds_final_2021_Spring\\env\\data.json", 'r', 'utf-8'))

#    sim_data = json.load(f)
    #tem path
    
    #print(sim_data)
    
    
    brute_method = Brute_Force(sim_data)
    results = brute_method.get_output()
#    print(results)
    return results