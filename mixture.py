import numpy as np
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from scipy.stats import bernoulli

dat = pd.read_csv('2019 PFF All Plays.csv')
# subset, probability of run/pass, density function conditioned on doing that

# run/pass, yardline, ytg, down

dat2 = dat[["pff_GAINLOSS", "pff_DOWN", "pff_DISTANCE", "pff_DRIVEENDEVENT",]]
dat["pff_GAINLOSS"]
dat["pff_DOWN"]

#%%
down1_p = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="P")]
plt.hist(down1_p['pff_GAINLOSS'], bins=10)
down1_r = dat2[(dat2["pff_DOWN"]==1)&(dat2['pff_RUNPASS']=="R")]

down1_prob_p = len(down1_p)/(len(down1_p)+len(down1_r))
down1_prob_r = len(down1_r)/(len(down1_p)+len(down1_r))
# STEP 1: SAMPLE RUN OR PASS BASED ON PROBABILITIES
down1_res = bernoulli.rvs(down1_prob_p, size=1)
down1_res

# STEP 2: SAMPLE FROM THE DISTRIBUTIONS BASED ON RUN/PASS
### 1st down run
down1_r_normal = down1_r[(down1_r["pff_DISTANCE"]<=10)]
plt.hist(down1_r_normal['pff_GAINLOSS'], bins=100)

down1_r_long = down1_r[(down1_r["pff_DISTANCE"]>10)]
plt.hist(down1_r_long['pff_GAINLOSS'], bins=100)

### 1st down pass
down1_p_normal = down1_p[(down1_p["pff_DISTANCE"]<=10)]
plt.hist(down1_p_normal['pff_GAINLOSS'], bins=100)

down1_p_long = down1_p[(down1_p["pff_DISTANCE"]>10)]
plt.hist(down1_p_long['pff_GAINLOSS'], bins=100)


#%%
### Second down short
down2_short = dat2[(dat2["pff_DOWN"]==2)& (dat2["pff_DISTANCE"]<=4)]
down2_short_r = down2_short[(down2_short['pff_RUNPASS']=="R")]
down2_short_p = down2_short[(down2_short['pff_RUNPASS']=="P")]
len(down2_short_r)
len(down2_short_p)
plt.hist(down2_short_r['pff_GAINLOSS'], bins=100)


### Second down medium
down2_med = dat2[(dat2["pff_DOWN"]==2)& (dat2["pff_DISTANCE"]>=5)& (dat2["pff_DISTANCE"]<=10)]
down2_med_r = down2_med[(down2_med['pff_RUNPASS']=="R")]
down2_med_p = down2_med[(down2_med['pff_RUNPASS']=="P")]
len(down2_med_r)
len(down2_med_p)
### Second down long
down2_long = dat2[(dat2["pff_DOWN"]==2)& (dat2["pff_DISTANCE"]>=11)]
down2_long_r = down2_long[(down2_long['pff_RUNPASS']=="R")]
down2_long_p = down2_long[(down2_long['pff_RUNPASS']=="P")]
len(down2_long_r)
len(down2_long_p)

### Third down short
down3_short = dat2[(dat2["pff_DOWN"]==3)& (dat2["pff_DISTANCE"]<=4)]
down3_short_r = down3_short[(down3_short['pff_RUNPASS']=="R")]
down3_short_p = down3_short[(down3_short['pff_RUNPASS']=="P")]
plt.hist(down3_short_r['pff_GAINLOSS'], bins=20)
plt.hist(down3_short_p['pff_GAINLOSS'], bins=20)

len(down3_short_r)
len(down3_short_p)
### Third down medium
down3_med = dat2[(dat2["pff_DOWN"]==3)& (dat2["pff_DISTANCE"]>=5)& (dat2["pff_DISTANCE"]<=10)]
down3_med_r = down3_med[(down3_med['pff_RUNPASS']=="R")]
down3_med_p = down3_med[(down3_med['pff_RUNPASS']=="P")]
len(down3_med_r)
len(down3_med_p)
### Third down long
down3_long = dat2[(dat2["pff_DOWN"]==3)& (dat2["pff_DISTANCE"]>=11)]
down3_long_r = down3_long[(down3_long['pff_RUNPASS']=="R")]
down3_long_p = down3_long[(down3_long['pff_RUNPASS']=="P")]
len(down3_long_r)
len(down3_long_p)
