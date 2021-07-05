# To avoid environment problems, we highly recoomend you to run the demo code in colab
## colab link : https://colab.research.google.com/notebooks/intro.ipynb
    Demo data format must be like "visualization_data.json"
    ex:{"current_state_1": [12, 17, 63, 81, 182, 365, 305, 390, 484, 430, 476, 517, 393, 406, 450], "current_state_2": [10, 22, 36, 49, 125, 341, 641, 905, 1255, 1632, 1980, 2358, 2745, 3035, 3319], "isolated_miss_rate": [60.0, 0.0, 0.0, 0.0, 0.0], "infected_isolated_rate": [42.42424242424242, 7.620320855614973, 3.5077951002227175, 2.3485364193328797, 1.9541427826993223], "Accumulate_infect": [22, 39, 99, 172, 349, 748, 1003, 1352, 1796, 2125, 2519, 2938, 3207, 3510, 3838], "Accumulate_cured": [0, 0, 0, 105, 105, 105, 120, 120, 120, 126, 126, 126, 132, 132, 132]}

# How to get demo video?
## 1. Please upload your visualization data to colab. 
## 2. Modify the data path in generate_graph.ipynb
## 3. Modify your output file path and run the code. If you want to show the video in jupter notebook, please modify output file path as "None".
# Customize
## You can modify the parameters in bcr.bar_chart_race function according to your need.
### Reference : https://github.com/dexplo/bar_chart_race?fbclid=IwAR1GT3bBfHpyqUKcDnMJbSbFo9KjIDbvgSlcggatCqQUzsXOlINWF2T962g
## The code is based on bar_chart_race package