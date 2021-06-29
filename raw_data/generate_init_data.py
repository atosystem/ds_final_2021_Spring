import json
import random
import codecs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--infected_people_num', default=1000)
args = parser.parse_args()
#print(args.infected_people_num)
with open('./all_place.json', newline='') as f:
    place = json.load(f)
with open('./all_people.json', newline='') as f:
    people = json.load(f)

path = dict()
for i in people["People"] :
    path[i] = random.choice(place["Place"])
data = dict()
data["people_list"] = path
data["infected_people"] = []
for i in range(int(args.infected_people_num)) :
    data["infected_people"].append(random.choice(people["People"]))
fp = codecs.open('init_data.json', 'a+', 'utf-8')
fp.write(json.dumps(data,ensure_ascii=False))
fp.close()