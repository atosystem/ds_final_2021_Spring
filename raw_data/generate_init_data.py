import json
import random
import codecs

with open('./all_place.json', newline='') as f:
    place = json.load(f)
with open('./all_people.json', newline='') as f:
    people = json.load(f)

data = dict()
for i in people["People"] :
    data[i] = random.choice(place["Place"])

fp = codecs.open('init_data.json', 'a+', 'utf-8')
fp.write(json.dumps(data,ensure_ascii=False))
fp.close()