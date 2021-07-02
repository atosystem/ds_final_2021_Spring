# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 15:55:42 2021

@author: 王式珩
"""

import numpy as np
import names
import random
import time
import math
import queue
import json
import codecs
import uuid

#from enum import Enum
Accumulate_infect_number = 0
Accumulate_isolated_infect_number = 0
#Accumulate_dead_number = 0
Accumulate_cured_number = 0
current_1_number = 0
current_2_number = 0
#current_3_number = 0
#current__number = 0
infection_state = {
                0:"Not infected",
                1:"Incubation period",
                2:"pathogenesis",
                3:"immune"
                }
def random_phone_num_generator():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '{}-{}-{}'.format(first, second, last)


from functools import total_ordering
import threading
@total_ordering
class Person:
        
        def __init__(self, name):
            
            self.name = name
            self.phone_number = random_phone_num_generator()
            self.state = infection_state[0]
            self.last_place = []
            self.infect_prob = random.random()
            self.go_outside_prob = random.random()
            self.Incubation_length = random.random() / 2 # make Incubation longer
            
        def __eq__(self, other):
            if not isinstance(other, __class__):
                return NotImplemented
            return self.dead_prob == other.dead_prob

        def __lt__(self, other):
            if not isinstance(other, __class__):
                return NotImplemented
            return self.dead_prob < other.dead_prob
        
        def get_info(self):
            return (self.name, self.phone_number, self.state)
        
        def infect_or_not(self, p):
            # consider person difference
            global current_1_number
            global Accumulate_infect_number
            if p < self.infect_prob and self.state == infection_state[0]: # get infected
                self.state = infection_state[1]
                current_1_number += 1
                Accumulate_infect_number += 1
        
        def get_sick_or_not(self, p):
            global current_2_number
            global current_1_number
            if p < self.Incubation_length and self.state == infection_state[1]: 
                current_2_number += 1
                current_1_number -= 1
                self.state = infection_state[2]

        def cured(self):
            global Accumulate_cured_number
            global current_2_number
            global current_1_number
            if self.state == infection_state[1]:
                current_1_number -= 1
            elif self.state == infection_state[2]:
                current_2_number -= 1
                
           
#            this will halt miss
#            else:
#                raise "shit cure wrong !!!!!!!!!"
            Accumulate_cured_number += 1
            self.state = infection_state[3]
                
                
       
                
        
            
class env:
    
    def __init__(self, POPULATION, I_PROB, progress_time = 1):
        
        self.POPULATION = POPULATION # population of environment
        self.init_infect_number = 10
        self.people = {}
        
        self.I_PROB = I_PROB # Infection probability
        self.infect_number = 0
#        self.search_time = 5 #  being dependent to search time
        self.simulation_time = 3 # how many simulation between search
        self.progress_time = progress_time # how many search to conduct
        self.verbose = False
        self.infect_people = []
        self.datas = {}
        self.place = json.load(codecs.open(r"./place.json", 'r', 'utf-8'))
        self.init_address =json.load(codecs.open(r"../raw_data/all_place.json", 'r', 'utf-8'))['Place']
        print("len of add is ", len(self.init_address))
        
        self.bed_ratio = 1
        self.hospital_size = self.POPULATION // self.bed_ratio         
        
        self.hospital = queue.SimpleQueue()
        self.wait_hospital_person = queue.PriorityQueue()
        self.ALL_PLACE = {}
        
        self.visalization_data = {
                    'current_state_1':[],
                    'current_state_2':[],
                    'isolated_miss_rate':[],
                    'infected_isolated_rate' :[],
                    'Accumulate_infect':[],
                    'Accumulate_cured':[]
                }
        
#        self.tranistion_matrix = [
#                                  [  0.9, 0.025, 0.025, 0.025, 0.025],
#                                  [0.025,   0.9, 0.025, 0.025, 0.025],
#                                  [0.025, 0.025,   0.9, 0.025, 0.025],
#                                  [0.025, 0.025, 0.025,   0.9, 0.025],
#                                  [0.025, 0.025, 0.025, 0.025,   0.9]
#                                 ]
        print("Start Init",flush=True)
        # build place
        # self.ALL_PLACE : entire_address -> [person name..]
        for place in self.init_address:
            temp = ""
            for p in place:
                temp += p
            self.ALL_PLACE[temp] = set()
        # build people
        self.datas["people_list"] = {}
        self.datas["infected_people"] = []
        
#        places = iter(self.init_address)
        global current_2_number
        global Accumulate_infect_number
        current_2_number += self.init_infect_number
        Accumulate_infect_number += self.init_infect_number
        for i in range(self.init_infect_number):
            name = str(uuid.uuid4())
            self.people[name] = Person(name)
            self.people[name].last_place = random.choice(self.init_address) 
            
            self.people[name].state = infection_state[2] 
            self.datas["infected_people"].append(name)
            if self.verbose:
                print(f"{name} is at {infection_state[2]}")
        
        for i in range(self.POPULATION-self.init_infect_number):
            name = str(uuid.uuid4())
            self.people[name] = Person(name)
            self.people[name].last_place = random.choice(self.init_address)
        for i in range(self.simulation_time):
             self.datas["people_list"][i] = {}
        print("Length of people ", len(self.people))
        print("Done Init",flush=True)
              
    def reset(self): # called when search is over
        print("Reset",flush=True)
        for  p in self.ALL_PLACE.keys():
            self.ALL_PLACE[p].clear()
        for i in range(self.simulation_time):
            self.datas["people_list"][i] = {}
        self.datas["infected_people"] = []
    def search(self):
        ### To do 
        # Input: self.place
        # Output : list of people to be isolated(state 2),(optional) list of people to be self isolated(state 1) 

        from Brute_force import Brute_force
#        from Trie import trie_search
        # results = Brute_force(self.datas)
        results = Brute_force(self.datas)
        
        
        return results
    
    
        
    def calculate_search_time(self, Time):
        # can be modified
        num = 10 // Time
        if self.verbose:
            print(f"Can take {int(num+1)} people")
        return int(num+1)

    def progress(self): # start next round
        global Accumulate_cured_number,  Accumulate_infect_number, Accumulate_isolated_infect_number, current_1_number, current_2_number 
        for k in range(self.progress_time):
            if self.verbose:
                print("-------------------------------------------------------------")            
            for i in range(self.simulation_time):
                self.new_simulation_2(i)
                self.visalization_data['current_state_1'].append(current_1_number)
                self.visalization_data['current_state_2'].append(current_2_number)
                self.visalization_data['Accumulate_infect'].append(Accumulate_infect_number)
                self.visalization_data['Accumulate_cured'].append(Accumulate_cured_number)
                
                
            start = time.time()
            sick_people = self.search()
            end = time.time()
            num = self.calculate_search_time(end-start)
#            exit(0)
            goin = 0
            catch_miss = 0 # record those whom isolated but not infected
             # lU TODO ##########################
            for person in sick_people[:num]:
                if self.people[person].state == infection_state[0]:
                    catch_miss += 1
                else:
                    Accumulate_isolated_infect_number += 1
                if self.hospital.qsize() < self.hospital_size:
                    self.hospital.put(person)
                    self.people[person].cured()
                    del self.people[person]
                    goin += 1
                
#            if self.verbose:
            print("Total population", len(self.people))
            print("Total people caught: ", num)
            print("     Can go to hospital : ", goin)
            print("     Can't go to hospital : ", num - goin)
            print(f"Catch miss rate : {100*(catch_miss/num)}% ({catch_miss}/{num})" )
            print(f"isolated rate of infected people {100*(Accumulate_isolated_infect_number/Accumulate_infect_number)}%")
            self.visalization_data['isolated_miss_rate'].append(100*(catch_miss/num))        
            self.visalization_data['infected_isolated_rate'].append(100*(Accumulate_isolated_infect_number/Accumulate_infect_number))        
            self.reset()
#            if self.verbose:
            print(f"Not isolated people at {infection_state[1]}:",current_1_number)
            print(f"Not isolated people at {infection_state[2]}:",current_2_number)
            print("Accumulated infected person :",Accumulate_infect_number)
            print("Accumulated cured person :",Accumulate_cured_number)
            print("-------------------------------------------------------------")
        
        fp = codecs.open('visualization_data.json', 'w', 'utf-8')
        fp.write(json.dumps(self.visalization_data,ensure_ascii=False))
        fp.close()
            
    def Move(self, last):
        data = self.place
        new_location = ['台灣']
        #print(len(data))
        if self.verbose:
            print("last location is ", last)
        move = False
        #new_place = ""
        for i in range(1,5):
        #    for key in data.keys():
            keys = []
            prob = []
            try:
                for key in data.keys():
                    if key == "All_place":
                        continue
                    keys.append(key)
                    if not (move):
                        if key == last[i]:
                            prob.append(1-i/10)
                        else :
                            prob.append((i/10)/(len(data)-1))
                    else:
                        prob.append(1/len(data))
            except:
                print("data is ", data)
                    
            new_place = random.choices(keys, weights=prob)[0]
            new_location.append(new_place)
            if not move and new_place != last[i]:
                move = True
            data = data[new_place]
        #    new_place = data
        new_location.append(data[-1])
        if self.verbose:
            print("Go to ", new_location)  
        return new_location
    
    def new_simulation_2(self, time_index):
        infected_place = set()
        
        for name in self.people.keys():
            person = self.people[name]
            if self.verbose:
                print("*******************************************")
                print("Person :", person.get_info())
#            threads = []
#            for i in range(5):
#              threads.append(threading.Thread(target = self.Move, args = (person.last_place,)))
#              threads[i].start()

            person.last_place = self.Move(person.last_place)
            temp = ""
            for p in person.last_place:
                temp += p
            # record place of infected, used for virus propagation
            if (person.state == infection_state[1] or person.state == infection_state[2]):
#                for p in person.last_place:
                infected_place.add(temp)
                if self.verbose:
                    print(f"{person.last_place} is infected !!")
            # recorder every place has who
#            for key in person.last_place:
            self.ALL_PLACE[temp].add(person.name)
            # store the data for search
            self.datas["people_list"][time_index][name] = person.last_place
              
        
        while(len(infected_place) > 0): # traverse all the place infected
            
            p = infected_place.pop() # got one infected place
            infect_prob = random.uniform(0, self.I_PROB) # infection_state 0 -> 1
            get_sick_prob = random.uniform(0, self.I_PROB) # infection_state 1 -> 2  
            while(len(self.ALL_PLACE[p]) > 0):# traverse all the name in place infected
                name = self.ALL_PLACE[p].pop()
                person = self.people[name]
                if person.state == infection_state[0]:
                    person.infect_or_not(infect_prob)
                    if person.state  == infection_state[1] and self.verbose:
                        print(f'{person.name} is {person.state}')
#                Incubation end
                elif person.state == infection_state[1]:
                    person.get_sick_or_not(get_sick_prob)
                    
                    if person.state == infection_state[2] and (person.name not in self.infect_people):
                        self.datas["infected_people"].append(person.name)
                        if self.verbose:
                            print(f'{person.name} is {person.state}')
        

Environment = env(
    POPULATION=5000, 
    I_PROB=0.1,  
    progress_time = 5
)
Environment.progress()   