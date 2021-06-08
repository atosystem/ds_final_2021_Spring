
import os
import json
import random
import numpy as np
import time



HUMAN_COUNT = 10
PLACES_COUNT = 10
HOURS_COUNT = 12

OUTPUT_FILE = "random_data.json"

print("[parameters]")
print("HUMAN_COUNT : {}".format(HUMAN_COUNT))
print("PLACES_COUNT : {}".format(PLACES_COUNT))
print("HOURS_COUNT : {}".format(HOURS_COUNT))

with open("names_data/first-names.json","r") as f:
    first_name_list = json.load(f)
with open("names_data/middle-names.json","r") as f:
    middle_name_list = json.load(f)
with open("names_data/names.json","r") as f:
    last_name_list = json.load(f)

random.seed(int(time.time()))
people_list=set([])

while(not len(people_list) == HUMAN_COUNT):
    random.shuffle(first_name_list)
    random.shuffle(middle_name_list)
    random.shuffle(last_name_list)
    # print(len(first_name_list))
    # print(len(middle_name_list))
    # print(len(last_name_list))
    for i,m_name in enumerate(middle_name_list[:HUMAN_COUNT-len(people_list)]):
        people_list.add("{}_{}_{}".format(first_name_list[i],m_name,last_name_list[i]))

result=[]
for t in range(HOURS_COUNT):
    print("Generating hour #{}/{}".format(t,HOURS_COUNT))
    hour_data = {}
    for place in range(PLACES_COUNT):
        hour_data["place_{}".format(place)] = []
    for p in people_list:
        hour_data["place_{}".format(random.randint(0,PLACES_COUNT-1))].append(p)

    result.append(hour_data)

with open(OUTPUT_FILE,"w") as f:
    json.dump({
        "names" : list(people_list),
        "places" : ["place_{}".format(x) for x in range(PLACES_COUNT)],
        "data" : result
    },f)
print("random data saved to {}".format(OUTPUT_FILE))
        

