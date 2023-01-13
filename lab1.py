# LAB 1

import numpy as np
import pandas as pd
from statistics import variance


# read in df
df = pd.read_csv("2019 PFF All Plays.csv")

# %% Question 1
# Dividing the field into obvious 10 yard increments, create a csv file with four columns.
# In the first column place the bin ids (e.g. (0-10], (10-20], etc), in the second column place
# the proportion of times teams punted on 4th down, in the 3rd column place the proportion of
# times teams kicked a field goal on 4th down, and in the 4th column the proportion of times
# teams attempted to convert to a new set of downs.

# going to have to group by bins to find proportions

# ================ Dividing into bins======================
pos = df['pff_FIELDPOSITION']
# from -49 to -40 is own 1-10; from -39 to -30 is own 11-20; from -29 to -20 is own 21-30
# from -19 to -10 is own 31- 40; from -9 to -1 is own 41-40; 50 is midfield
# 49-40; 39-30; 29-20; 19-10, 9-0 0 is TD

df['bins'] = np.where(((pos >= -10) & (pos <= -1)), '(0,10]',
                        np.where(((pos >= -20) & (pos <= -11)), '(10,20]',
                                 np.where(((pos >= -30) & (pos <= -21)), '(20,30]',
                                          np.where(((pos >= -40) & (pos <= -31)), '(30,40]',
                                                   np.where(((pos > -50) & (pos <= -41)), '(40,50]',
                                                            np.where(pos == 50, '(40,50]',
                                                                     np.where(((pos < 50) & (pos >= 40)), '(50,60]',
                                                                              np.where(((pos < 40) & (pos >= 30)), '(60,70]',
                                                                                       np.where(((pos < 30) & (pos >= 20)), '(70,80]',
                                                                                                np.where(((pos < 20) & (pos >= 10)), '(80,90]',
                                                                                              np.where(((pos < 10) & (pos >= 0)), '(90,100]', float("nan"))))))))))))
# ========================================================================
sub = df[['pff_GAMEID', 'pff_DOWN', 'pff_PENALTYYARDS',
            'pff_FIELDPOSITION', 'bins', 'pff_DRIVEENDEVENT',
            'pff_KICKYARDS', 'pff_BALLCARRIER', 'pff_SPECIALTEAMSTYPE',
            'pff_RUNPASS']]

fourth = sub[(sub['pff_DOWN'] == 4)]

fourth_punt = fourth[fourth['pff_SPECIALTEAMSTYPE'] == 'PUNT']
fourth_fg = fourth[fourth['pff_SPECIALTEAMSTYPE'] == 'FIELD GOAL']
fourth_went = fourth[(fourth['pff_RUNPASS'] == 'R') |
                     (fourth['pff_RUNPASS'] == 'P')]
fourth_X = fourth[fourth['pff_RUNPASS'] == 'X']
fourth_NA = fourth[(fourth['pff_SPECIALTEAMSTYPE'].isnull())
                   & (fourth['pff_RUNPASS'].isnull())]


# for the props, are we calculating them as a proportion of all fourth down plays ran?
# Including plays with penalties?
# Are props supposed to add to 1, condition on bins

prop_punt = fourth_punt['bins'].value_counts().to_frame()
prop_punt['prop_punt'] = prop_punt['bins'] / len(fourth_punt)

prop_fg = fourth_fg['bins'].value_counts().to_frame()
prop_fg['prop_fg'] = prop_fg['bins'] / len(fourth_fg)

prop_went = fourth_went['bins'].value_counts().to_frame()
prop_went['prop_went'] = prop_went['bins'] / len(fourth_went)

prop_punt = prop_punt.drop(columns = ['bins']).sort_index(ascending=True).T
prop_fg = prop_fg.drop(columns = ['bins']).sort_index(ascending=True).T
prop_went = prop_went.drop(columns = ['bins']).sort_index(ascending=True).T
temp3 = prop_punt.merge(prop_fg, how = 'outer')
temp3 = temp3.merge(prop_went, how = 'outer')

props_total = temp3.rename(index={0: 'Punt', 1: 'FG', 2:'Went for it'})
#props_total.to_csv('props_total.csv', header=True)
# %% Question 2
# first find number of plays per drive for each drive
# then calculate average by dividing total number of plays in a game by number of drives
# have to sort by game ID  0.84

uva = df[df['pff_OFFTEAM'] == 'VAUN']
uva2 = uva[['pff_GAMEID', 'pff_DRIVE', 'pff_DOWN',
            'pff_DRIVEPLAY', 'pff_PENALTYYARDS', 'pff_SPECIALTEAMSTYPE',
            'pff_RUNPASS', 'pff_DRIVEENDPLAYNUMBER']]
# takes out kickoffs and plays with penalties that didnt result in a play
uva2 = uva2[uva2['pff_DOWN'] != 0]
uva2 = uva2[(uva2['pff_SPECIALTEAMSTYPE'].notnull())
            | (uva2['pff_RUNPASS'].notnull())]

# if there is an NA after a drive, the driveplay should be the previous row +1 and drivenumber should be the same

uva2['pff_DRIVE'].fillna(method='pad', inplace=True)
uva2['pff_DRIVEPLAY'].fillna(method='pad', inplace=True)

uva2['pff_DRIVEPLAY'] = np.where(uva2['pff_DOWN']==4, uva2['pff_DRIVEPLAY']+1,uva2['pff_DRIVEPLAY'] )
uva3 = uva2[['pff_GAMEID', 'pff_DRIVE', 'pff_DRIVEPLAY']]
temp6 = uva3['pff_DRIVE'].groupby(uva3['pff_GAMEID'])
temp7 = temp6.max() # number of drives per game
temp8 = temp6.count() # number of plays per game
avg_perdrive = temp8 / temp7

variance(avg_perdrive)
# %% Question 3
# Write a function that returns all play IDs that correspond to safeties.
# Upload a CSV file (not an excel) with only a single column that has all play IDs that
# correspond to safeties. This may be more challenging than it seems at first.
# Don't trust that the obvious solution is the right solution.
# You should verify that all other 2 point scores in the dfset are indeed not safeties.
# This will involve some exploratory analysis of the presumably "non-safety" 2 point gains.

# 2 safeties were never recorded in the same game in 2019
temp4 = df[df['pff_DRIVEENDEVENT'] == 'SAFETY']
temp4 = temp4[['pff_PLAYID', 'pff_GAMEID', 'pff_GAMEDATE', 'pff_DRIVE', 'pff_DOWN',
               'pff_DRIVEPLAY']]

temp5 = temp4.groupby(['pff_GAMEID'])['pff_PLAYID'].max().to_frame()
playid = temp5[['pff_PLAYID']].reset_index().drop('pff_GAMEID', axis=1)
#playid.to_csv('playid.csv', header= True)
