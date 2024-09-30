import numpy as np
import pandas as pd
from psychopy import visual, event, core
from  function_Task1 import *



win = visual.Window(units='pix', fullscr=True, color='black');


global_obj = init(win);

table = global_obj["game"];
ref_table = global_obj["ref"];

print(table[:]);
print(table.iloc[1,:]);


sampling_players(win,table,ref_table,0,maxSample=3,conf_label=["High","Low","Low","High"])


win.close();
core.quit();