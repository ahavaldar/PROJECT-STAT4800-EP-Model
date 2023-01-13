import numpy as np
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from scipy.stats import bernoulli, chisquare, chi2

football_data = pd.read_csv('2019 PFF All Plays.csv')

football_data['O_FG'] = np.where(football_data['pff_SPECIALTEAMSTYPE'] == 'FIELD GOAL', 1, 0)
FG_attempts = football_data[football_data['O_FG'] == 1]
FG_attempts['Made'] = np.where(FG_attempts['pff_KICKRESULT'].str.contains('MADE'), 1, 0)
grouped_FG = FG_attempts.groupby('pff_FIELDPOSITION').sum()

FG_Pos = np.array(FG_attempts['pff_FIELDPOSITION'])
FG_Pos = FG_Pos.reshape(-1,1)

model = LogisticRegression()
fit = model.fit(FG_Pos, FG_attempts['Made'])
#fit.intercept_
#fit.coef_
#ans = fit.predict([[35]])
#ans
#fit.predict_proba([[35]])
#%%
dat = pd.read_csv('2019 PFF All Plays.csv')
# subset, probability of run/pass, density function conditioned on doing that

# run/pass, yardline, ytg, down

dat2 = dat[["pff_GAINLOSS", "pff_DOWN", "pff_RUNPASS", "pff_DISTANCE"]]
#%%
import random 
import numpy as np

def punt(previous_field_position):
  punt_yards = int(np.floor(np.random.normal(42, 9)))
  if previous_field_position + punt_yards > 100:
    return 80
  else:
    return previous_field_position + punt_yards

def first_down(yards_to_go):
  down1_p = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="P")]
  down1_r = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="R")]

  len(down1_p), len(down1_r)

  comb = len(down1_p) + len(down1_r)

  a = (len(down1_p)/comb)
  b = (len(down1_r)/comb)

  # 1 = pass, 0 = run
  data_bern = bernoulli.rvs(size=1,p=a)
  play_call = data_bern[0]

  if play_call == 0:
    if yards_to_go > 10:
      # 1st down run (Longer 10<x)
      down1_r_long = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]>10)]

      s = np.random.normal(down1_r_long['pff_GAINLOSS'].mean(), down1_r_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]

    else:
      # 1st down run (Normal x<=10)
      down1_r_normal = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]<=10)]

      s = np.random.normal(down1_r_normal['pff_GAINLOSS'].mean(), down1_r_normal['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
  
  else:
    if yards_to_go > 10:
      # 1st down pass (Long 10<x)
      down1_p_long = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]>10)]

      s = np.random.normal(down1_p_long['pff_GAINLOSS'].mean(), down1_p_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]

    else:
      # 1st down pass (Normal x<=10)
      down1_p_normal = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]<=10)]

      s = np.random.normal(down1_p_normal['pff_GAINLOSS'].mean(), down1_p_normal['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]

def second_down(yards_to_go):
  if yards_to_go >= 11:
    # 2nd down and long
    down2_long = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]>=11)]
    down2_long = down2_long['pff_RUNPASS'].value_counts()
    
    down2_r = down2_long[0]
    down2_p = down2_long[1]
    comb = down2_p + down2_r

    a = (down2_p/comb)
    b = (down2_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down2_r_long = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]>=11)]
      s = np.random.normal(down2_r_long['pff_GAINLOSS'].mean(), down2_r_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down2_p_long = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]>=11)]
      s = np.random.normal(down2_p_long['pff_GAINLOSS'].mean(), down2_p_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]
      
  if yards_to_go >= 5:
    # 2nd down and medium
    down2_medium = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
    down2_medium = down2_medium['pff_RUNPASS'].value_counts()

    down2_r = down2_medium[0]
    down2_p = down2_medium[1]
    comb = down2_p + down2_r

    a = (down2_p/comb)
    b = (down2_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down2_r_medium = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
      s = np.random.normal(down2_r_medium['pff_GAINLOSS'].mean(), down2_r_medium['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down2_p_medium = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
      s = np.random.normal(down2_p_medium['pff_GAINLOSS'].mean(), down2_p_medium['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]

  else:
    # 2nd down and short
    down2_short = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]<=4)]
    down2_short = down2_short['pff_RUNPASS'].value_counts()

    down2_r = down2_short[0]
    down2_p = down2_short[1]
    comb = down2_p + down2_r

    a = (down2_p/comb)
    b = (down2_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down2_r_short = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]<=4)]
      s = np.random.normal(down2_r_short['pff_GAINLOSS'].mean(), down2_r_short['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down2_p_short = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]<=4)]
      s = np.random.normal(down2_p_short['pff_GAINLOSS'].mean(), down2_p_short['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]

def third_down(yards_to_go):
  if yards_to_go >= 11:
    # 3rd down and long
    down3_long = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]>=11)]
    down3_long = down3_long['pff_RUNPASS'].value_counts()
    
    down3_r = down3_long[0]
    down3_p = down3_long[1]
    comb = down3_p + down3_r

    a = (down3_p/comb)
    b = (down3_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down3_r_long = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]>=11)]
      s = np.random.normal(down3_r_long['pff_GAINLOSS'].mean(), down3_r_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down3_p_long = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]>=11)]
      s = np.random.normal(down3_p_long['pff_GAINLOSS'].mean(), down3_p_long['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]
      
  if yards_to_go >= 5:
    # 3rd down and medium
    down3_medium = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
    down3_medium = down3_medium['pff_RUNPASS'].value_counts()

    down3_r = down3_medium[0]
    down3_p = down3_medium[1]
    comb = down3_p + down3_r

    a = (down3_p/comb)
    b = (down3_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down3_r_medium = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
      s = np.random.normal(down3_r_medium['pff_GAINLOSS'].mean(), down3_r_medium['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down3_p_medium = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]>=5) & (dat2['pff_DISTANCE']<=10)]
      s = np.random.normal(down3_p_medium['pff_GAINLOSS'].mean(), down3_p_medium['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]

  else:
    # 3rd down and short
    down3_short = dat2[(dat2["pff_DOWN"]==2) & (dat2["pff_DISTANCE"]<=4)]
    down3_short = down3_short['pff_RUNPASS'].value_counts()

    down3_r = down3_short[0]
    down3_p = down3_short[1]
    comb = down3_p + down3_r

    a = (down3_p/comb)
    b = (down3_r/comb)

    # 1 = pass, 0 = run
    data_bern = bernoulli.rvs(size=1,p=a)
    play_call = data_bern[0]

    if play_call == 0:
      down3_r_short = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="R") & (dat2["pff_DISTANCE"]<=4)]
      s = np.random.normal(down3_r_short['pff_GAINLOSS'].mean(), down3_r_short['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Run"]
    
    else:
      down3_p_short = dat2[(dat2["pff_DOWN"]==2)&(dat2['pff_RUNPASS']=="P") & (dat2["pff_DISTANCE"]<=4)]
      s = np.random.normal(down3_p_short['pff_GAINLOSS'].mean(), down3_p_short['pff_GAINLOSS'].std(), 2)
      return [int(np.floor(s.mean())), "Pass"]
#%%
def simulation(down, yards_to_go, field_position, team, t):
  if field_position >= 90:
    to_go = "Goal"
  else:
    to_go = yards_to_go
  #The Play
  #print("Team "+str(team)+": "+str(down)+" down and "+str(to_go)+" on the "+str(field_position))
  if down == 4 and field_position >= 60:
    #print("FG Attempted")
    probs = fit.predict_proba([[abs(100-field_position)]])
    make = np.random.binomial(1, probs[0][1])
    if make == 1:
      #print("FG Made!")
      if team == t:
        return 3
      else:
        return -3
    else:
      #print("FG Missed!")
      team = 2 if team == 1 else 1
      return simulation(1, 10, 100-field_position, team, t)
  else:
    #Yards Gained
    #yards_gained = min(random.randint(-5, 100-field_position), random.randint(-5, 100-field_position))
    if down == 1:
      result = first_down(yards_to_go)
    elif down == 2:
      result = second_down(yards_to_go)
    elif down == 3:
      result = third_down(yards_to_go)
    elif down == 4:
      # 4th Down Decision
      if field_position >= 50 and yards_to_go <= 2:
        result = third_down(yards_to_go)
      else:
        #print("Punt")
        team = 2 if team == 1 else 1
        return simulation(1, 10, 100-punt(field_position), team, t)

    yards_gained = result[0]
    play_call = result[1]

    #print("Play Call: "+play_call)

    #Field Position
    previous_field_position = field_position
    field_position = field_position + yards_gained

    #yards_gained
    if field_position <= 0:
      yards_gained = -previous_field_position

    if field_position >= 100:
      yards_gained = 100-previous_field_position

    #New Down
    down = down + 1
    #Yards To Go
    yards_to_go = yards_to_go - yards_gained

    #print("Yards Gained: "+str(yards_gained))

    #Interception
    if play_call == "Pass":
      if random.randint(1, 70) == 2:
        #print("Interception!")
        team = 2 if team == 1 else 1
        if field_position >= 100:
          field_position = 20
        else:
          field_position = 100 - field_position
        down = 1
        yards_to_go = 10
    
    #Fumble
    if random.randint(1, 100) == 2:
      if field_position < 100:
        #print("Fumble!")
        team = 2 if team == 1 else 1
        field_position = 100 - field_position
        down = 1
        yards_to_go = 10

    #Safety
    if field_position <= 0:
      #print("Safety!")
      if team == t:
        return -2
      else:
        return 2
      '''
      team = 2 if team == 1 else 1
      field_position = 35 #change this
      down = 1
      yards_to_go = 10
      '''

    #Touch Down
    if field_position >= 100:
      #print("Team: "+str(team)+" "+"Touchdown!")
      if team == t:
        return 7
      else:
        return -7
    #First Down
    if yards_to_go <= 0:
      down = 1
      yards_to_go = 10
    #Turnover
    if down > 4:
      #print("Turnover!")
      team = 2 if team == 1 else 1
      field_position = 100 - field_position
      down = 1
      yards_to_go = 10
    
    return simulation(down, yards_to_go, field_position, team, t)

#down, distance, field_position, team, team_under_analysis

print(simulation(1, 10, 20, 1, 1))
#%%
#down, distance, field_position, team, team_under_analysis
import time
t1 = time.time()
monte = 5
sims = 30
punted = []
didnt_get_it = []
got_it = []

field_position = 60
distance = 5

p2 = []
d2 = []
g2 = []

for i in range(monte):
    for i in range(sims):
      #print(i+1)
      punted.append(simulation(1, 10, 100-punt(field_position), 2, 1))
      didnt_get_it.append(simulation(1, 10, field_position, 2, 1))
      got_it.append(simulation(1, 10, field_position+distance, 1, 1))
    p1 = sum(punted)/len(punted)
    d1 = sum(didnt_get_it)/len(didnt_get_it)
    g1 = sum(got_it)/len(got_it)
    p2.append(p1)
    d2.append(d1)
    g2.append(g1)
t2 = time.time()
print(t2-t1)

     

#print(punted)
print(sum(punted)/len(punted))
p1 = sum(punted)/len(punted)

#print(didnt_get_it)
print(sum(didnt_get_it)/len(didnt_get_it))
d1 = sum(didnt_get_it)/len(didnt_get_it)

#print(got_it)
print(sum(got_it)/len(got_it))
g1 = sum(got_it)/len(got_it)

p3 = np.random.normal(np.mean(p2), np.std(p2), 1000)
d3 = np.random.normal(np.mean(d2), np.std(d2), 1000)
g3 = np.random.normal(np.mean(g2), np.std(g2), 1000)

plt.hist(p3)
plt.hist(d3)
plt.hist(g3)
