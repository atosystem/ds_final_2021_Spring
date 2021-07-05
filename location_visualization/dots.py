import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import random
import json


N = 5000
BOUND = 4000

STOP_TIME = 10
MOVE_TIME = 40

isolation_pos_x = 500
isolation_pos_y = 500
NOISE = 600

ISOLATION_STATE_NUM = 4

# color_for_state = {
#     0 : "blue",   # "Not infected"
#     1 : "orange", # "Incubation period"
#     2 : "red",    # "pathogenesis"
#     3 : "gray",   # "immune",
#     4 : "gray"    #isolated
# }


color_for_state = {
    0 : [0/255,134/255,236/255,0.2],   # "Not infected"
    1 : [252/255,164/255,56/255,0.8], # "Incubation period"
    2 : [255/255,0,0,0.9],    # "pathogenesis"
    3 : [90/255,90/255,90/255,1],    # "immune"
    4 : [90/255,90/255,90/255,1]    # "isolated"
}

size_for_state = {
    0 : 1,   # "Not infected"
    1 : 10, # "Incubation period"
    2 : 10,    # "pathogenesis"
    3 : 10,    # "immune"
    4 : 10    # "isolated"
}




with open('./map_data_converted.json', newline='') as f:
    movingdata = json.load(f)

# Creating dot class
class dot(object):
    def __init__(self,person_name):
        # self.x = BOUND * np.random.random_sample()
        # self.y = BOUND * np.random.random_sample()
        self.x = (movingdata[0][person_name][0])
        self.y = (movingdata[0][person_name][1])
        self.velx = self.generate_new_vel()
        self.vely = self.generate_new_vel()
        self.trace = [] # [(x1,y1),(x2,y2)..]
        self.name = person_name
        self.state = movingdata[0][person_name][2]

    def generate_new_vel(self):
        return (np.random.random_sample() - 0.5)  * 5

    def move(self,animate_i):
        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def inside(x1, y1):
            if distance(x1, y1, 5, 5) <= 1:
                return True
            else:
                return False

        def calc_dist(d):
            ret = 0
            for x in dots:
                if inside(x.x, x.y) and x != d:                            
                    ret = ret + distance(x.x, x.y, d.x, d.y)
            return ret

        position_i = int(animate_i / (STOP_TIME+MOVE_TIME))
        if position_i >= len(movingdata) - 1:
            return
        position_inner_i = animate_i % (STOP_TIME+MOVE_TIME)
        if position_inner_i < STOP_TIME:
            # not transiting

            self.state = movingdata[position_i][self.name][2]
        else:
            # transiting
            # ratio = (position_inner_i - STOP_TIME) / MOVE_TIME
            ratio = 1 / MOVE_TIME
            target_x = movingdata[position_i+1][self.name][0]
            target_y = movingdata[position_i+1][self.name][1]
            start_x = movingdata[position_i][self.name][0]
            start_y = movingdata[position_i][self.name][1]

            if movingdata[position_i+1][self.name][2] == ISOLATION_STATE_NUM:
                target_x = isolation_pos_x + (np.random.random_sample()-0.5)*NOISE
                target_y = isolation_pos_y + (np.random.random_sample()-0.5)*NOISE
            if movingdata[position_i][self.name][2] == ISOLATION_STATE_NUM:
                start_x = isolation_pos_x + (np.random.random_sample()-0.5)*NOISE
                start_y = isolation_pos_y + (np.random.random_sample()-0.5)*NOISE


            # self.x = (target_x - start_x) * ratio * (position_inner_i-STOP_TIME) + start_x
            # self.y = (target_y - start_y) * ratio * (position_inner_i-STOP_TIME) + start_y
            self.x += (target_x - start_x) * ratio
            self.y += (target_y - start_y) * ratio


# Initializing dots
d_l = list(movingdata[0].keys())
# random.shuffle(d_l)
dots = [dot(p) for p in d_l[:N]]
print("Total #{} dots".format(len(dots)))



fig = plt.figure()
ax = plt.axes(xlim=(0, BOUND), ylim=(0, BOUND))

d = ax.scatter([dot.x for dot in dots],
             [dot.y for dot in dots],s = [ size_for_state[dot.state] for dot in dots],color=[ color_for_state[dot.state] for dot in dots])

# isolation zone
circle = plt.Circle((isolation_pos_x, isolation_pos_y), 250, color='b', fill=False)
ax.add_artist(circle)


# animation function
def animate(i):
    # print(i)
    for dot in dots:
        dot.move(i)
    d.set_offsets([[dot.x,dot.y] for dot in dots])
    d.set_color([color_for_state[dot.state] for dot in dots])
    d._sizes = ([ size_for_state[dot.state] for dot in dots])
    return d,

anim = animation.FuncAnimation(fig, animate, frames=2000, interval=200,repeat=False)

plt.show()
