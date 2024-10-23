from psychopy import visual, core, event
import pandas as pd
import json
import numpy as np

win = visual.Window(units='pix', fullscr=True, color='black');
ticks=[0,1,2,3]
lbl= [''] * len(ticks);
slider = visual.Slider(win, 
    ticks=ticks,  # The range is from 0 to 3
    labels=lbl,  # Empty labels for each tick
    granularity=1,  # Discrete steps
    style=['rating'],  # Style of the slider
    size=(0.6*win.size[0], 0.05*win.size[1]),  # Size of the slider
    pos=(0, 0));  # Position at the center
slider.marker.color = 'green';


### Read inputs
game_schedule = pd.read_csv("Input/Game_Schedule.csv");

with open('Input/reference.json', 'r') as file:
    json_string = file.read();
ref_table = eval(json_string);

with open('Input/reference_bis.json', 'r') as file:
    json_string = file.read();
ref_table_bis = eval(json_string);

print(ref_table_bis,ref_table);
refs = [ref_table,ref_table_bis];
print(refs[0]);
s = [0,1];
np.random.shuffle(s); #Select which one of the set will be bis
print(s,s[0],s[1]);

dictionary = {"slider":slider,"game":game_schedule,"ref":refs[s[0]],"ref_bis":refs[s[1]]};


win.close();
core.quit();