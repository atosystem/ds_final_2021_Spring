# Covid-19 疾病傳播模擬

> Animated Map

<img src="https://i.imgur.com/QvwzACg.gif" alt="drawing" width="480"/>

> Dynamic Results Demo

<img src="https://i.imgur.com/OIf1CTz.gif" alt="drawing" width="480"/>

# Prerequisite
```
$ pip install -r requirements.txt
```

# Run Environment
...
# Run Animated Map
Demo : [Link](https://youtu.be/cUGV4uGejgQ)

Go to [`./location_visualization`](./location_visualization) for more details

# Run dynamic results demo
Go to [`./demo`](./demo) for more details

Code based on repo : [bar_chart_race](https://github.com/dexplo/bar_chart_race)

# Functionalities
1. Environment for people movements and epidemic simulation
2. Using `Trie` and `Brute Force` to isolate people
3. Animated Map for visualization



# Input/Output for our Search Algorithm

Search Algorithm Input: 
```
{
    "people_list":
    {
        "王大華" : ["台灣","北區","台北市","大安區","羅斯福路","7-11"],
        "王小華" : ["台灣","北區","台北市","大安區","復興南路","全家"],
        ...
    },
    "infected_people":["王小華"...]
}
```
> `people_list` indicates the places where all people are

search algorithm output: (include all people names who needs to be isolated)
```
["王小華", "王大華"...]
```
> Note that in our implementation, we use uuid or ID instead of Chinese Name.

> For generating random data go to [`./raw_data`](./raw_data).
