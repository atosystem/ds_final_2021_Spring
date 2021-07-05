# Covid-19 疾病傳播模擬

![](https://i.imgur.com/rFQpES3.gif)

# Prerequisite
```
$ pip install -r requirements.txt
```

# Run Environment
...
# Run Animated Map
Demo : [Link]("https://youtu.be/cUGV4uGejgQ")

Go to [`./location_visualization`](./location_visualization) for more details

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
