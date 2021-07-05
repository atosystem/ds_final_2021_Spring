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
current_4_number = 0
#current_3_number = 0
#current__number = 0
infection_state = {
                0:"Not infected",
                1:"Incubation period",
                2:"pathogenesis",
                3:"immune",
                4:"isolated"
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
#@total_ordering
class Person:
        
        def __init__(self, name):
            
            self.name = name
            self.phone_number = random_phone_num_generator()
            self.state = infection_state[0]
            self.last_place = []
            self.infect_prob = random.random()/3
            self.go_outside_prob = random.random()
            self.Incubation_length = random.random()/3  # make Incubation longer
            
        def get_info(self):
            return (self.name, self.phone_number, self.state)
        
        def infect_or_not(self, p):
            # consider person difference
            global current_1_number
            global Accumulate_infect_number
            if self.infect_prob < p  and self.state == infection_state[0]: # get infected
                self.state = infection_state[1]
                current_1_number += 1
                Accumulate_infect_number += 1
        
        def get_sick_or_not(self, p):
            global current_2_number
            global current_1_number
            if self.Incubation_length < p and self.state == infection_state[1]: 
                current_2_number += 1
                current_1_number -= 1
                self.state = infection_state[2]

        def isolated(self):
            global current_2_number
            global current_1_number
            global current_4_number
            if self.state == infection_state[1]:
                current_1_number -= 1
            elif self.state == infection_state[2]:
                current_2_number -= 1
                
           
#            this will halt miss
#            else:
#                raise "shit cure wrong !!!!!!!!!"
            current_4_number += 1
            self.state = infection_state[4]
            
        def cured(self):
            global Accumulate_cured_number, current_4_number
            Accumulate_cured_number += 1
            current_4_number -= 1
            self.state = infection_state[3]
       
                
        
import matplotlib.pyplot as plt
 
class env:
    
    def __init__(self, POPULATION, I_PROB, progress_time = 1):
        
        self.POPULATION = POPULATION # population of environment
        self.init_infect_number = 10
        self.people = {}
        
        self.I_PROB = I_PROB # Infection probability
        self.infect_number = 0
#        self.search_time = 5 #  being dependent to search time
        self.simulation_time = 2 # how many simulation between search
        self.progress_time = progress_time # how many search to conduct
        self.verbose = False
        self.infect_people = []
        self.datas = {}
        self.place = json.load(codecs.open(r"./place.json", 'r', 'utf-8'))
        self.init_address =json.load(codecs.open(r"../raw_data/all_place.json", 'r', 'utf-8'))['Place']
#        print("len of add is ", len(self.init_address))
        
        self.bed_ratio = 1
        self.hospital_size = self.POPULATION // self.bed_ratio         
#        print()
        self.hospital = queue.SimpleQueue()
        self.wait_hospital_person = queue.PriorityQueue()
        self.ALL_PLACE = {}
        # ALl data need
        self.visalization_data = {
                    'current_state_1':[],
                    'current_state_2':[],
                    'isolated_miss_rate':[],
                    'infected_isolated_rate' :[],
                    'Accumulate_infect':[],
                    'Accumulate_cured':[]
                }
        self.map = True
        self.map_data = [] # For map visualizaion
        
        self.current_1 = {'brute':[], 'trie':[]}
        self.current_2 = {'brute':[], 'trie':[]}
        self.current_3 = {'brute':[], 'trie':[]}
        self.current_0 = {'brute':[], 'trie':[]}
        self.current_4 = {'brute':[], 'trie':[]}
        self.miss_rate = {'brute':[], 'trie':[]}
        self.time = {'brute':[], 'trie':[]}
        self.accumulated_infect = {'brute':[], 'trie':[]}
        self.accumulated_infect_isolated_rate = {'brute':[], 'trie':[]}
        #        plt.text(19, 8.8, f"infection probability: {self.I_PROB}")
#                                 ]
        print("Start Init",flush=True)
        # build place
        # self.ALL_PLACE : entire_address -> [person name..]
        
    
    def draw(self):
        plt.figure(figsize=(20,10), dpi = 100)      
        plt.style.use('seaborn-whitegrid')     
        plt.text(19, 9, f"infection probability: {self.I_PROB}")
        plt.text(19, 8.9, f"Initial infectied number: {self.init_infect_number}")

#        self.current_1 = {'brute':[], 'trie':[]}
        plt.plot(self.current_1['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.current_1['trie'], color='red', label = " Trie Method")
        plt.plot([self.POPULATION for i in range(len(self.current_1['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel(f"At {infection_state[1]} people number")
        plt.title(f"{infection_state[1]} people")
        plt.legend(loc = "best")
        for i,v in enumerate(self.current_1['brute']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+100))
        for i,v in enumerate(self.current_1['trie']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+150))
        plt.savefig("state_1.jpg")
        plt.cla()
#        self.current_2 = {'brute':[], 'trie':[]}
        plt.plot(self.current_2['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.current_2['trie'], color='red', label = " Trie Method")
        plt.plot([self.POPULATION for i in range(len(self.current_2['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel(f"At {infection_state[2]} people number")
        plt.title(f"{infection_state[2]} people")
        plt.legend(loc = "best")
        for i,v in enumerate(self.current_2['brute']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+5))
        for i,v in enumerate(self.current_2['trie']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+10))
        plt.savefig("state_2.jpg")
        plt.cla()
#        self.current_3 = {'brute':[], 'trie':[]}
        plt.plot(self.current_3['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.current_3['trie'], color='red', label = " Trie Method")
        plt.plot([self.POPULATION for i in range(len(self.current_3['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel(f"At {infection_state[3]} people number")
        plt.title(f"{infection_state[3]} people")
        plt.legend(loc = "best")
        for i,v in enumerate(self.current_3['brute']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+50))
        for i,v in enumerate(self.current_3['trie']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+50))
        plt.savefig("state_3.jpg")
        plt.cla()
#        self.current_0 = {'brute':[], 'trie':[]}
        plt.plot(self.current_0['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.current_0['trie'], color='red', label = " Trie Method")
        plt.plot([self.POPULATION for i in range(len(self.current_0['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel("Not infected people number")
        plt.title("Not infected people")
        plt.legend(loc = "best")
        for i,v in enumerate(self.current_0['brute']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+5))
        for i,v in enumerate(self.current_0['trie']):
            if i % 3 == 0:
                plt.annotate(str(v), xy=(i,v+5))
        plt.savefig("state_0.jpg")
        plt.cla()
#        self.miss_rate = {'brute':[], 'trie':[]}
        plt.plot(self.miss_rate['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.miss_rate['trie'], color='red', label = " Trie Method")
#        plt.plot([self.POPULATION for i in range(len(self.miss_rate['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel("Isolated miss_rate")
        plt.title("Isolated Miss")
        for i, (v1, v2) in enumerate(zip(self.miss_rate['brute'], self.miss_rate['trie'])):
            if i % 2 == 0:
                if v1 > v2:
                    plt.annotate(str(v1) + "%", xy=(i,v1+5))
#                    plt.annotate(str(self.current_2['brute'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v1+6))
#                    plt.annotate(str(self.current_2['trie'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v1-5))
                    plt.annotate(str(v2)+ "%", xy=(i,v2-6))
                else:
                    plt.annotate(str(v1)+ "%", xy=(i,v1-6))
#                    plt.annotate(str(self.current_2['brute'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v1-5))
#                    plt.annotate(str(self.current_2['trie'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v1+6))
                    plt.annotate(str(v2)+ "%", xy=(i,v2+5))
#        for i,v in enumerate(self.miss_rate['brute']):
#            if i % 2 == 0:
#                plt.annotate(str(v*100)+ "%", xy=(i,v+0.1))
#                plt.annotate(str(self.current_2['brute'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v+5.2))
#        for i,v in enumerate(self.miss_rate['trie']):
#            if i % 2 == 0:
#                plt.annotate(str(v*100) + "%", xy=(i,v+0.1))
#                plt.annotate(str(self.current_2['trie'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v+10.2))

        plt.legend(loc = "best")
        plt.savefig("miss_rate.jpg")
        plt.cla()
#        self.time = {'brute':[], 'trie':[]}
        plt.plot(self.time['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.time['trie'], color='red', label = " Trie Method")
#        plt.plot([self.POPULATION for i in range(len(self.miss_rate['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel("Taken Search Time (sec)")
        plt.title("Search Time")
        plt.legend(loc = "best")
        for i,v in enumerate(self.time['brute']):
            if i % 2 == 0:
                plt.annotate(str(v)+"(sec)", xy=(i,v+5))
#                plt.annotate(str(self.current_2['brute'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v + 20))

        for i,v in enumerate(self.time['trie']):
            if i % 2 == 0:
                plt.annotate(str(v)+"(sec)", xy=(i,v+5))
#                plt.annotate(str(self.current_2['trie'][2*i+1]) + f"people at {infection_state[2]} ", xy=(i,v+20))
        plt.savefig("time.jpg")
        plt.cla()
#        self.accumulated_infect = {'brute':[], 'trie':[]}         
        plt.plot(self.accumulated_infect['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.accumulated_infect['trie'], color='red', label = " Trie Method")
        plt.plot([self.POPULATION for i in range(len(self.accumulated_infect['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel("Accumulated Infect number")
        plt.title("Accumulated Infect")
        plt.legend(loc = "best")
        for i, (v1, v2) in enumerate(zip(self.accumulated_infect['brute'], self.accumulated_infect['trie'])):
            if i % 2 == 0:
                if v1 > v2:
                    plt.annotate(str(v1), xy=(i,v1+100))
                    plt.annotate(str(v2), xy=(i,v2-100))
                else:
                    plt.annotate(str(v1), xy=(i,v1-100))
                    plt.annotate(str(v2), xy=(i,v2+100))
        
        plt.savefig("Accumulated_Infect.jpg")
        plt.cla()
        
        plt.plot(self.accumulated_infect_isolated_rate['brute'], color='blue', label = " Brute Force Method")
        plt.plot(self.accumulated_infect_isolated_rate['trie'], color='red', label = " Trie Method")
#        plt.plot([self.POPULATION for i in range(len(self.accumulated_infect['trie']))], color='green', label = "Total Population")
        plt.legend(loc='best')
        plt.xlabel("time")
        plt.ylabel("Accumulated Infect isolated rate")
        plt.title("Accumulated Infect isolated rate")
        plt.legend(loc = "best")
        for i,v in enumerate(self.accumulated_infect_isolated_rate['brute']):
            if i % 2 == 0:
                plt.annotate(str(v) + "%", xy=(i,v+0.1))
#                plt.annotate(str(self.accumulated_infect['trie'][2*i+1]) + f"people once infected ", xy=(i,v+10.2))
        for i,v in enumerate(self.accumulated_infect_isolated_rate['trie']):
            if i % 2 == 0:
                plt.annotate(str(v) + "%" , xy=(i,v+0.1))
#                plt.annotate(str(self.accumulated_infect['trie'][2*i+1]) + f"people once infected ", xy=(i,v+10.2))
        plt.savefig("Accumulated_Infect_isolated_rate.jpg")
        plt.cla()
    def reset(self): # called when search is over
        print("Reset",flush=True)
        for  p in self.ALL_PLACE.keys():
            self.ALL_PLACE[p].clear()
        for i in range(self.simulation_time):
            self.datas["people_list"][i] = {}
        self.datas["infected_people"] = []
    def search(self, t):
        ### To do 
        # Input: self.place
        # Output : list of people to be isolated(state 2),(optional) list of people to be self isolated(state 1) 

        from Brute_force import Brute_force
        from Trie import trie_search
        # results = Brute_force(self.datas)
        if t == 'brute':
            return Brute_force(self.datas)
        if t == 'trie':
            return trie_search(self.datas)
        
        
        
    
    
        
    def calculate_search_time(self, Time):
        # can be modified
        global current_2_number, Accumulate_cured_number, Accumulate_infect_number
        print("Time is ", Time)
        print("current_2_number is ", current_2_number)
        num = self.I_PROB * (current_2_number + current_1_number) * self.init_infect_number / (Time + 1)
#        print("percent is ", ((Time) / (current_2_number+1)))
        if self.verbose:
            print(f"Can take {num} people")
        return max(1, int(num))

    def progress(self): # start next round
        for search in ['brute']:
            global Accumulate_cured_number,  Accumulate_infect_number, Accumulate_isolated_infect_number, current_1_number, current_2_number, current_3_number, current_4_number 
            Accumulate_cured_number = 0
            Accumulate_infect_number = self.init_infect_number
            Accumulate_isolated_infect_number = 0
            current_1_number = 0
            current_4_number = 0
            current_3_number = 0
            current_2_number = self.init_infect_number
            while (not self.hospital.empty()):
                name = self.hospital.get()
            print(f"Now {self.hospital.qsize()} people in hosipital")
            for place in self.init_address:
                temp = ""
                for p in place:
                    temp += p
                self.ALL_PLACE[temp] = set()
            # build people
            
            
    #        places = iter(self.init_address)
            self.people.clear()
            self.datas.clear()
            self.datas["people_list"] = {}
            self.datas["infected_people"] = []
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
            print("***********************************************")
            print("Length of people ", len(self.people))
            print('current_state_1 initialize is ', current_1_number)
            print('current_state_2 initialize is ', current_2_number)
            print('current_state_3 initialize is ', current_3_number)
            print('current_state_4 initialize is ', current_4_number)
            print("Accumulate_cured_number is ", Accumulate_cured_number)
            print("Accumulate_infect_number is ", Accumulate_infect_number)
            print("Accumulate_isolated_infect_number ", Accumulate_isolated_infect_number)
            print("Done Init",flush=True)
            print(f"Now is {search} search")
            for k in range(self.progress_time):
                if self.verbose:
                    print("-------------------------------------------------------------")            
                for i in range(self.simulation_time):
                    self.new_simulation_2(i, search)
                    self.visalization_data['current_state_1'].append(current_1_number)
                    self.visalization_data['current_state_2'].append(current_2_number)
                    self.visalization_data['Accumulate_infect'].append(Accumulate_infect_number)
                    self.visalization_data['Accumulate_cured'].append(Accumulate_cured_number)
                    
                    
                start = time.time()
                sick_people = self.search(search)
                end = time.time()
                self.time[search].append(end-start)
                num = self.calculate_search_time(end-start)
    #            exit(0)
                goin = 0
                catch_miss = 0 # record those whom isolated but not infected
                 # lU TODO ##########################
                print(self.hospital.qsize())
                print(self.hospital_size)
                num = min(num, len(sick_people)-1)
                
                # let hosioital realease
                while (not self.hospital.empty()):
                    name = self.hospital.get()
                    self.people[name].cured()
                for person in sick_people[:num]:
                    
                    if self.hospital.qsize() < self.hospital_size:
                        if self.people[person].state == infection_state[0]:
                            catch_miss += 1
                        elif self.people[person].state == infection_state[3]:
                            num += 1
                            goin -= 1
                        else:
                            Accumulate_isolated_infect_number += 1
                            self.hospital.put(person)
                            self.people[person].isolated()
                            
    #                        del self.people[person]
                        goin += 1
                   
    #            if self.verbose:
                print("Total population", len(self.people))
                print("Total people caught: ", num)
                print("     Can go to hospital : ", goin)
                print("     Can't go to hospital : ", num - goin)
                print(f"Catch miss rate : {100*(catch_miss/(num))}% ({catch_miss}/{num})" )
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
                
                # collect data for drawing
                self.accumulated_infect[search].append(Accumulate_infect_number)
                self.miss_rate[search].append(100* catch_miss/num)
                self.current_3[search].append(Accumulate_cured_number)
                self.current_4[search].append(current_4_number)
                self.accumulated_infect_isolated_rate[search].append(100*(Accumulate_isolated_infect_number/Accumulate_infect_number))
            fp = codecs.open('visualization_data.json', 'w', 'utf-8')
            fp.write(json.dumps(self.visalization_data,ensure_ascii=False))
            fp.close()
            
            if(self.map):
                fp = codecs.open('brute_map_data.json', 'w', 'utf-8')
                fp.write(json.dumps(self.map_data,ensure_ascii=False))
                fp.close()
                
        self.draw()
            
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
                            prob.append(1-i/20)
                        else :
                            prob.append((i/20)/(len(data)-1))
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
    
    def new_simulation_2(self, time_index, search):
        global Accumulate_infect_number,  current_1_number, current_2_number 

        infected_place = set()
        map_data = {}
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
            if (self.map):
                map_data[name] = {
                            'location':person.last_place,
                            'state':person.state
                        }
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
            get_sick_prob = random.uniform(0, self.I_PROB)*5 # infection_state 1 -> 2  
            while(len(self.ALL_PLACE[p]) > 0):# traverse all the name in place infected
                name = self.ALL_PLACE[p].pop()
                person = self.people[name]
                if person.state == infection_state[0]:
                    person.infect_or_not(infect_prob)
                    if(self.map):
                        map_data[name]['state'] = person.state
                    if person.state  == infection_state[1] and self.verbose:
                        print(f'{person.name} is {person.state}')
#                Incubation end
                elif person.state == infection_state[1]:
                    person.get_sick_or_not(get_sick_prob)
                    if(self.map):
                        map_data[name]['state'] = person.state
                    if person.state == infection_state[2] and (person.name not in self.infect_people):
                        self.datas["infected_people"].append(person.name)
                        if self.verbose:
                            print(f'{person.name} is {person.state}')
#        collect drawing data
        self.current_0[search].append(self.POPULATION - Accumulate_infect_number)
        self.current_1[search].append(current_1_number)
        self.current_2[search].append(current_2_number)
        if (self.map):
            self.map_data.append(map_data)

Environment = env(
    POPULATION=100000, 
    I_PROB=0.2,  
    progress_time = 5
)
Environment.progress()   