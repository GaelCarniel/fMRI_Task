from psychopy import visual, core, event, data, gui
import numpy as np

def f(delta):
    return ((5/2)*delta+50)/100



n_trials = 50;
quest = data.QuestHandler(startVal=15, startValSd=5, pThreshold=.75, gamma=0.5, nTrials=n_trials, minVal=0, maxVal=20);


for trial in quest:
    delta = quest.next();
    delta = max(min(delta, 20), 0);
    
    prob = f(delta);
    
    r = np.random.uniform();
    if r<prob:
        correct= 1;
    else:
        correct = 0;

    quest.addResponse(correct);
    print(f"Trial: delta was {delta} the subject answer correctly: {correct}");
print(f"treshold = {quest.mean()}");
print(f"F({quest.mean()}) = {f(quest.mean())}");

