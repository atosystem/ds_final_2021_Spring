
import json
import random
import numpy as np
with open('../env/brute_map_data.json', newline='') as f:
    map_data = json.load(f)

with open('./geoloaction_clean.json', newline='') as f:
    place_location = json.load(f)

infection_state = {
                "Not infected" : 0,
                "Incubation period" : 1,
                "pathogenesis" : 2,
                "immune" : 3,
                "isolated" : 4
}

MIDDLE_POINT = [120.97388,23.97565]
X_SCALE = 1000
Y_SCALE = 1000

NOISE = 0.05

import numpy as np

x_arr = []
y_arr = []
for t in map_data:
    for p in t:
        addr = "".join(t[p]["location"][2:4])
        x_pos = ((float(place_location[addr]["x"]) - MIDDLE_POINT[0]) + 3 + (np.random.random_sample()-0.5)*NOISE) * X_SCALE
        y_pos = ((float(place_location[addr]["y"]) - MIDDLE_POINT[1]) + 2 + (np.random.random_sample()-0.5)*NOISE) * Y_SCALE
        x_arr.append(x_pos)
        y_arr.append(y_pos)
        t[p] = [x_pos,y_pos,infection_state[t[p]["state"]]]
        # t[p]["location"] = [float(place_location[addr]["x"]),float(place_location[addr]["y"])]
        # print(t[p])
        # exit()

x_arr = np.array(x_arr)
y_arr = np.array(y_arr)

print("x")
print("max",np.max(x_arr))
print("min",np.min(x_arr))
print("std",np.std(x_arr))
print("avg",np.average(x_arr))

print("y")
print("max",np.max(y_arr))
print("min",np.min(y_arr))
print("avg",np.average(y_arr))
print("std",np.std(y_arr))

for t in map_data:
    print(len(t))

with open('./map_data_converted.json',"w") as f:
    json.dump(map_data,f)