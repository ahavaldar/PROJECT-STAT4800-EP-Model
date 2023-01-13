import numpy as np
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


football_data = pd.read_csv('2019 PFF All Plays.csv')
football_data['O_FG'] = np.where(football_data['pff_SPECIALTEAMSTYPE'] == 'FIELD GOAL', 1, 0)
FG_attempts = football_data[football_data['O_FG'] == 1]
FG_attempts['Made'] = np.where(FG_attempts['pff_KICKRESULT'].str.contains('MADE'), 1, 0)
grouped_FG = FG_attempts.groupby('pff_FIELDPOSITION').sum()



FG_Pos = np.array(FG_attempts['pff_FIELDPOSITION'])
FG_Pos = FG_Pos.reshape(-1,1)



model = LogisticRegression()
fit = model.fit(FG_Pos, FG_attempts['Made'])
fit.intercept_
fit.coef_
ans = fit.predict([[31]])
ans
ans = fit.predict_proba([[31]])
ans[0][1]


#Miss Make

np.random.binomial(1, [0.47389604])

for i in range(40):
    print(fit.predict_proba([[i]]))


# def simulation(down, yards_to_go, field_position, team):
#   #The Play
#   print("Team "+str(team)+": "+str(down)+" down and "+str(yards_to_go)+" on the "+str(field_position))
#   #Yards Gained
#   #yards_gained = min(random.randint(-5, 100-field_position), random.randint(-5, 100-field_position))
#   yards_gained = round(np.floor(np.random.normal(3.5, 2, size=(1)))[0])
#   print("Yards Gained: "+str(yards_gained))
#   #Field Position
#   field_position = field_position + yards_gained
#   #New Down
#   down = down + 1
#   #Yards To Go
#   yards_to_go = yards_to_go - yards_gained

#   #Touch Down
#   if field_position >= 100:
#     print("Team: "+str(team)+" "+"Touchdown!")
#     return
#   #First Down
#   if yards_to_go <= 0:
#     down = 1
#     yards_to_go = 10
#   # Field Goal
#   if field_position >= 60 and down == 4:
#     print("Field Goal Attempt")
      
#   #Turnover
#   if down > 4:
#     print("Turnover!")
#     team = 2 if team == 1 else 1
#     field_position = 100 - field_position
#     down = 1
#     yards_to_go = 10
#   simulation(down, yards_to_go, field_position, team)


# simulation(1, 10, 25, 1)



df = pd.read_csv("2019 PFF All Plays.csv")
df2 = df.loc[:,["pff_FIELDPOSITION", "pff_KICKDEPTH", "pff_KICKRESULT"]]



def simulation(down, yards_to_go, field_position, team):
  #The Play
  print("Team "+str(team)+": "+str(down)+" down and "+str(yards_to_go)+" on the "+str(field_position))
  if down == 4 and field_position > 60:
    print("FG Attempted")
    probs = fit.predict_proba([[abs(100-field_position)]])
    #print(probs[0][1])
    make = np.random.binomial(1, probs[0][1])
    if make == 1:
      print("FG Made!")
      return
    else:
      print("FG Missed!")
      team = 2 if team == 1 else 1
      simulation(1, 10, 100-field_position, team)
    else:
    #Yards Gained
    #yards_gained = min(random.randint(-5, 100-field_position), random.randint(-5, 100-field_position))
        yards_gained = round(np.floor(np.random.normal(3.5, 2, size=(1)))[0])
        print("Yards Gained: "+str(yards_gained))
    #Field Position
        field_position = field_position + yards_gained
    #New Down
        down = down + 1
    #Yards To Go
        yards_to_go = yards_to_go - yards_gained
    #Touch Down
        if field_position >= 100:
        print("Team: "+str(team)+" "+"Touchdown!")
          return
    #First Down
    if yards_to_go <= 0:
      down = 1
      yards_to_go = 10
    #Turnover
    if down > 4:
      print("Turnover!")
      team = 2 if team == 1 else 1
      field_position = 100 - field_position
      down = 1
      yards_to_go = 10
    simulation(down, yards_to_go, field_position, team)

simulation(1, 10, 25, 1)

