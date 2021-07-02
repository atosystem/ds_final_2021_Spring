# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 11:41:11 2021

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
Accumulate_dead_number = 0
Accumulate_cured_number = 0
infection_state = {
                0:"Not infected",
                1:"Incubation period",
                2:"pathogenesis",
                3:"curing",
                4:"immune",
                5:"dead"
                }
def random_phone_num_generator():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '{}-{}-{}'.format(first, second, last)


from functools import total_ordering

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
            self.dead_prob = 0 # should be zero at the beginning
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
            if p < self.infect_prob and self.state == infection_state[0]: # get infected
                self.state = infection_state[1]
        
        def get_sick_or_not(self, p):
            global Accumulate_infect_number
            if p < self.Incubation_length and self.state == infection_state[1]: 
                Accumulate_infect_number += 1
                self.state = infection_state[2]
                self.dead_prob = random.random()/3
                
        def curing(self):
            
            if self.state == infection_state[2]:
                self.state = infection_state[3]
                self.dead_prob = 0
        def cured(self):
            global Accumulate_cured_number
            if self.state == infection_state[3]:
                self.state = infection_state[4]
                self.dead_prob = 0
                Accumulate_cured_number += 1
                
        def die_or_not(self, p):
            global Accumulate_dead_number
            if p < self.dead_prob and self.state == infection_state[2]:
                self.state = infection_state[5]
                Accumulate_dead_number += 1
                
        
            
class env:
    
    def __init__(self, POPULATION, NUM_P, I_PROB, O_PROB, progress_time = 1):
        
        self.POPULATION = POPULATION # population of environment
        self.init_infect_number = 10
        self.people = {}
        
        self.I_PROB = I_PROB # Infection probability
        self.O_PROB = O_PROB # Go outside probability 
        self.infect_number = 0
#        self.search_time = 5 #  being dependent to search time
        self.simulation_time = 3 # how many simulation between search
        self.progress_time = progress_time # how many search to conduct
        self.verbose = False
        self.infect_people = []
        self.datas = {}
        self.NUM_P = NUM_P # number of place
        self.place = json.load(codecs.open(r"./place.json", 'r', 'utf-8'))
        self.init_address =json.load(codecs.open(r"../raw_data/all_place.json", 'r', 'utf-8'))['Place']
        print("len of add is ", len(self.init_address))
        
        self.bed_ratio = 1
        self.hospital_size = self.POPULATION // self.bed_ratio         
        
        self.hospital = queue.SimpleQueue()
        self.wait_hospital_person = queue.PriorityQueue()
        self.hospital_power = self.POPULATION // 5000
        self.ALL_PLACE = {}
        
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
        
        # places = iter(self.init_address)
        temp_i = 0
        for i in range(self.init_infect_number):
            name = str(uuid.uuid4())
            # name = names.get_full_name()
            # count = 0
            # while name in self.people.keys():
            #     name = names.get_full_name()
            #     count += 1
            #     if count > 10:
            #         print("Too many duplicate name !!!")
            #         raise "Shit, too many duplicate name !!!"
            self.people[name] = Person(name)
            # self.people[name].last_place = next(places) 
            self.people[name].last_place = self.init_address[temp_i %len(self.init_address)]
            temp_i +=1 
            
            self.people[name].state = infection_state[2] 
#            self.datas["names"].append(name)
            self.datas["infected_people"].append(name)
            if self.verbose:
                print(f"{name} is at {infection_state[2]}")
        
        for i in range(self.POPULATION-self.init_infect_number):
            name = str(uuid.uuid4())
            # name = names.get_full_name()
            # count = 0
            # while name in self.people.keys():
            #     name = names.get_full_name()
            #     count += 1
            #     if count > 10:
            #         print("Too many duplicate name !!!")
            #         raise "Shit, too many duplicate name !!!"
            self.people[name] = Person(name)
            # self.people[name].last_place = next(places)
            self.people[name].last_place = self.init_address[temp_i %len(self.init_address)]
            temp_i +=1 
#            self.datas["names"].append(name)
        for i in range(self.simulation_time):
             self.datas["people_list"][i] = {}

        print("Done Init",flush=True)
              
    def reset(self): # called when search is over
#        for i in range(self.NUM_P):
#            self.datas[i] = [[] for k in range(self.simulation_time)]
        for  p in self.ALL_PLACE.keys():
            self.ALL_PLACE[p].clear()
        self.Medical_treatment()
    def search(self):
        ### To do 
        # Input: self.place
        # Output : list of people to be isolated(state 2),(optional) list of people to be self isolated(state 1) 

        from Brute_force import Brute_force
        from Trie import trie_search


        # results = Brute_force(self.datas)
        results = trie_search(self.datas)
        
        
        return results
    
    def calculate_search_time(self, Time):
        # can be modified
        num = 10 // Time
        if self.verbose:
            print(f"Can take {int(num+1)} people")
        return int(num+1)
    # lU TODO ##########################
    def Medical_treatment(self):
        global Accumulate_cured_number
        old_cur = Accumulate_cured_number
        if self.hospital_power > self.hospital.qsize():
            
            size = self.hospital.qsize()
            for i in range(size):
                person = self.hospital.get()
                self.people[person].cured()
            
            # The hospital become empty, so it can put as many person as it could
            if self.hospital_size > self.wait_hospital_person.qsize():
                
                size = self.wait_hospital_person.qsize()
                for i in range(size):                 
                    person = self.wait_hospital_person.get()
                    self.people[person].curing()
                    self.hospital.put(person)
            
            else:
                
                for i in range(self.hospital_size):
                    person = self.wait_hospital_person.get()
                    self.people[person].curing()
                    self.hospital.put(person)
            
        else:
            for i in range(self.hospital_power):
                person = self.hospital.get()
                self.people[person].cured()
                
            # The hospital is not empty, so it can put as many person until it is full
            remain_size = self.hospital_size - self.hospital.qsize()
            if remain_size > self.wait_hospital_person.qsize():
                
                size = self.wait_hospital_person.qsize()
                for i in range(size):
                    person = self.wait_hospital_person.get()
                    self.people[person].curing()
                    self.hospital.put(person)
            
            else:
                
                for i in range(remain_size):
                    person = self.wait_hospital_person.get()
                    self.people[person].curing()
                    self.hospital.put(person)
        
        if self.wait_hospital_person.qsize() > 0:
            people_may_die = []
            size = self.wait_hospital_person.qsize()
            for i in range(size):
                people_may_die.append(self.wait_hospital_person.get())
                
            die_prob = random.random()
            for person in people_may_die:
                self.people[person].die_or_not(die_prob)
                if self.people[person].state != infection_state[5]:
                    self.wait_hospital_person.put(person)
        
        if self.verbose:
            print(f"Newly cured {Accumulate_cured_number - old_cur} people")
            
        
    def progress(self): # start next round
        
        for k in range(self.progress_time):
            if self.verbose:
                print("-------------------------------------------------------------")            
            for i in range(self.simulation_time):
                self.new_simulation_2(i)
            
            print("Start search")
            start = time.time()
            sick_people = self.search()
            end = time.time()
            print("End search")
            num = self.calculate_search_time(end-start)
#            exit(0)
            goin = 0
            not_goin = 0
             # lU TODO ##########################
            for person in sick_people[:num]:
                if self.hospital.qsize() < self.hospital_size:
                    self.people[person].curing()
                    self.hospital.put(person)
                    goin += 1
                else:
                    self.wait_hospital_person.put(person)
                    not_goin += 1
#            if self.verbose:
            print("Total people caught: ", goin+not_goin)
            print("     Can go to hospital : ", goin)
            print("     Can't go to hospital : ", not_goin)

                    
            self.reset()
#            if self.verbose:
            print("Accumulated infected person :",Accumulate_infect_number)
            print("Accumulated dead person :",Accumulate_dead_number)
            print("-------------------------------------------------------------")

            
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
        infect_prob = random.uniform(0, 0.1) # infection_state 0 -> 1
        get_sick_prob = random.uniform(0, 0.1) # infection_state 1 -> 2        
        
        while(len(infected_place) > 0): # traverse all the place infected
            
            p = infected_place.pop() # got one infected place
            
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
                        self.infect_people.append(person.name)
                        if self.verbose:
                            print(f'{person.name} is {person.state}')
        
    def new_simulation(self, time_index):
        infected_place = set()
        for name in self.people.keys():
            person = self.people[name]
            if self.verbose:
                print("*******************************************")
                print("Person :", person.get_info())
            
            person.last_place = self.Move(person.last_place)
            # record place of infected, used for virus propagation
            if (person.state == infection_state[1] or person.state == infection_state[2]):
                for p in person.last_place:
                    infected_place.add(p)
                    if self.verbose:
                        print(f"{p} is infected !!")
            # recorder every place has who
            for key in person.last_place:
                self.ALL_PLACE[key].add(person.name)
            # store the data for search
            self.datas["people_list"][time_index][name] = person.last_place
        # It' not reason to involve in taiwan
        infected_place.remove('台灣')           
        
        infect_prob = random.uniform(0, 0.1) # infection_state 0 -> 1
        get_sick_prob = random.uniform(0, 0.1) # infection_state 1 -> 2        
        
        while(len(infected_place) > 0): # traverse all the place infected
            
            p = infected_place.pop() # got one infected place
            
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
                        self.infect_people.append(person.name)
                        if self.verbose:
                            print(f'{person.name} is {person.state}')
        
Environment = env(
    POPULATION=100000, 
    NUM_P=5, # unused
    I_PROB=0.1, 
    O_PROB=0.5, 
    progress_time = 5
)
Environment.progress()               
    
        