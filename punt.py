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

dat2 = dat[["pff_GAMEDATE","pff_DEFTEAM","pff_GAINLOSS", "pff_DOWN", "pff_DISTANCE", "pff_DRIVEENDEVENT",'pff_FIELDPOSITION', 'pff_SPECIALTEAMSTYPE', "pff_KICKYARDS"]]

fourth = dat2[(dat2['pff_DOWN'] == 4)]
punt = fourth[fourth['pff_SPECIALTEAMSTYPE'] == 'PUNT']
plt.hist(punt['pff_KICKYARDS'], bins=20)
# beta dist alpha =2 beta =8
fg = fourth[(fourth['pff_SPECIALTEAMSTYPE'] == 'FIELD GOAL')]
plt.hist(fg['pff_FIELDPOSITION'], bins=20)
# uniform distribution

goforit = fourth[(fourth['pff_SPECIALTEAMSTYPE'] != 'FIELD GOAL') & (fourth['pff_SPECIALTEAMSTYPE'] != 'PUNT')]
plt.hist(goforit['pff_FIELDPOSITION'], bins=20)


# punt distance: draw from normal distribution with mean 42 sd of 9
punt['pff_KICKYARDS'].std()
s = np.random.normal(42, 9, 1)


