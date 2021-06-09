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
            self.last_place = -1
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
    
    def __init__(self, POPULATION, NUM_P, I_PROB, O_PROB, progress_time = 10):
        
        self.POPULATION = POPULATION # population of environment
        self.people = {}
        
        self.I_PROB = I_PROB # Infection probability
        self.O_PROB = O_PROB # Go outside probability 
        self.infect_number = 0
        self.search_time = 5 #  being dependent to search time
        self.progress_time = progress_time # how many search to conduct
        self.verbose = False
        self.infect_people = []
        self.places = {}
        self.NUM_P = NUM_P # number of place

        self.bed_ratio = 1000
        self.hospital_size = self.POPULATION // self.bed_ratio         
        self.hospital = queue.SimpleQueue()
        self.wait_hospital_person = queue.PriorityQueue()
        self.hospital_power = self.POPULATION // 5000
        for i in range(self.NUM_P):
            self.places[i] = [[] for k in range(self.search_time)]
        self.places["names"] = []
        self.places["infected_names"] = []
        self.places["number of place"] = self.NUM_P
        
        for i in range(self.POPULATION):
            name = names.get_full_name()
            count = 0
            while name in self.people.keys():
                name = names.get_full_name()
                count += 1
                if count > 10:
                    print("Too many duplicate name !!!")
                    raise "Shit, too many duplicate name !!!"
            self.people[name] = Person(name)
            self.places["names"].append(name)
            
                
    def reset(self): # called when search is over
        for i in range(self.NUM_P):
            self.places[i] = [[] for k in range(self.search_time)]
        self.Medical_treatment()
    def search(self):
        ### To do 
        # Input: self.place
        # Output : list of people to be isolated(state 2),(optional) list of people to be self isolated(state 1) 
#        time.sleep(1)
#        num = 1
#        print(self.people)
        import json

        with open('data.json', 'w') as fp:
            json.dump(self.places, fp)
#        with open('infect_name_list.json', 'w') as fp:
#            json.dump(self.infect_people, fp)
#        np.save("name_list.npy", self.infect_people)
        
        
        return [name for name in self.infect_people]
    
    def calculate_search_time(self, Time):
        # can be modified
        self.search_time = math.ceil(Time/5)
        if self.verbose:
            print("search_time is ", self.search_time)
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
        for key in self.people.keys():
            self.people[key].state = infection_state[1]
            print(f"{self.people[key].get_info()} is at {infection_state[1]}")
            break
        for k in range(self.progress_time):
            if self.verbose:
                print("-------------------------------------------------------------")            
            for i in range(self.search_time):
                self.simulation(i)
            
            start = time.time()
            sick_people = self.search()
            end = time.time()
            self.calculate_search_time(end-start)
            
            goin = 0
            not_goin = 0
            for person in sick_people:
                if self.hospital.qsize() < self.hospital_size:
                    self.people[person].curing()
                    self.hospital.put(person)
                    goin += 1
                else:
                    self.wait_hospital_person.put(person)
                    not_goin += 1
            if self.verbose:
                print("Total sick people : ", goin+not_goin)
                print("Can go to hospital : ", goin)
                print("Can't go to hospital : ", not_goin)

                    
            self.reset()
            if self.verbose:
                print("Accumulated infected person :",Accumulate_infect_number)
                print("Accumulated dead person :",Accumulate_dead_number)
                print("-------------------------------------------------------------")

            
            
    def simulation(self, time_index):
        infected_place = {} # to record which place has infected people
        for name in self.people.keys():
            
            person = self.people[name]
            if self.verbose:
                print("*******************************************")
                print("Person :", person.get_info())
#            means to go outside, which may get infected
            if (random.random() * 3 + (1-person.go_outside_prob)) / 4 < self.O_PROB:
                if self.verbose:
                    print("Go outside !!")
                place = random.randint(0, self.NUM_P-1)
                if self.verbose:
                    print("Go to place ", place)
                while place == person.last_place:
                    place = random.randint(self.NUM_P)
                    if self.verbose:
                        print("Go to the same place, redone ")
                if not (person.state == infection_state[3] or person.state == infection_state[5]):
                    if (person.state == infection_state[1] or person.state == infection_state[2]):
                        infected_place[place] = 1
                        if self.verbose:
                            print(f"Place {place} infected")
                    self.places[place][time_index].append(name)
            if self.verbose:
                print("*******************************************")
        
        for place in infected_place.keys():
            infect_prob = random.random()
            get_sick_prob = random.random()
            for name in self.places[place][time_index]:
#                get infected
                person = self.people[name]
#                print(person.get_info()[0])
                if person.state == infection_state[0]:
                    person.infect_or_not(infect_prob)
#                Incubation end
                elif person.state == infection_state[1]:
                    person.get_sick_or_not(get_sick_prob)
                    
                    if person.state == infection_state[2] and (person.get_info()[0] not in self.infect_people):
                        self.places["infected_names"].append(person.get_info()[0])
            
  
Environment = env(10, 3, 0.1, 0.5)
Environment.progress()               
    
        