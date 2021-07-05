# ds_final_2021_Spring

![](https://i.imgur.com/rFQpES3.gif)

# Prerequisite
```
$ pip install -r requirements.txt
```

# Run environment
...
# Run animated map
Demo : [Link]("https://youtu.be/cUGV4uGejgQ")

Go to `./location_visualization` for more details


# i : ith place
search algorithm input: {"number of place": k, i": [["name1, name2"], ["name1, name2""name1, name2"] ......], "i+1": [["name1, name2"], ["name3", "name4"] ......], "i+2": [["name1, name2"], ["name3", "name4"] ......] ..... , "names": ["name1, name2", "name3, name4", .....nameT], "infected_names":["namek", "namet".....]}

search algorithm output: ["namek", "namez".....] # include all people names who had ever been in contact with infected people
