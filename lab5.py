import pandas as pd
import numpy as np 

nhl = pd.read_csv("nhl_pbp20162017.csv")
nhl = nhl.loc[:,["Game_Id", "Ev_Team","Period", "Event", "Seconds_Elapsed", "Strength"]]
nhl2 = nhl[(nhl["Period"]==1)|(nhl["Period"]==2)|(nhl["Period"]==3)]
nhl2 = nhl2[(nhl["Event"]=="SHOT")|(nhl["Event"]=="GOAL")]
