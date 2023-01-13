import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# TD is worth 7 or 6
# dividing field 5 yard increments, divide yards to go into increments
# filter by 1st and 3rd quarter
# avg of the interval, will this drive end in points
data = pd.read_csv("2019 PFF All Plays.csv")
df = data.loc[(data['pff_QUARTER']==1) | (data['pff_QUARTER']==3)]

# 2nd and 7 on own 32; run plays then punt
# want to know expected points for our current situation
# now other team has the ball and is going the other way
# they get a conversion in 2 plays, have a few more, and get a touchdown
# so for the 2nd and 7 on 32, what is the point value of the next score? = -7 in this case
# think about it offense vs defense, look at where the offense is
# each field position is a different calculation
# for every single line, what was the next score? and was it the current offense (+7) that scored
# or the current defense (-7)
# divide by yards to go and by down 

df = df[['pff_PLAYID', 'pff_GAMEID','pff_QUARTER', 'pff_DOWN', 'pff_CLOCK',
         'pff_DRIVE', 'pff_DRIVEPLAY','pff_DRIVEENDPLAYNUMBER','pff_DISTANCE','pff_DRIVEENDEVENT',
         'pff_DEFTEAM','pff_FIELDPOSITION', 'pff_DRIVEENDFIELDPOSITION', 'pff_SCORE']]
pos = df['pff_FIELDPOSITION']
df['yardline'] = np.where(((pos >= -10) & (pos <= -1)), '(0,10]',
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
# BINS: use same field position bins as lab1
# bin 1: 1st down
# bin 1a: between 1-10 yards
# bin 1b: between 11-15 yards
# bin 1c: greater than 16 yards
# bin 2: 2nd down
# bin 2a: between 1-3 yards
# bin 2b: between 4-7 yards
# bin 2c: between 8-15 yards
# bin 2d: greater than 16 yards
# same bins for 3 and 4 as bin 2
# home.away compare by to last line
down = df['pff_DOWN']
dist = df['pff_DISTANCE']

# figure this out
df['bin'] = np.where(((down==1) & (1 <= dist) & (dist <= 10)), "1[1-10]",
                     np.where(((down==1) & (11 <= dist) & (dist <= 15)), "1[11-15]",
                              np.where(((down==1) & (16 <= dist)), "1[16+]",
                                        np.where(((down==2) & (1 <= dist) &(dist <= 3)), "2[1-3]",
                                                 np.where(((down==2) & (4 <= dist) &(dist <= 7)), "2[4-7]",
                                                          np.where(((down==2) & (8 <= dist) &(dist <= 15)), "2[8-15]", 
                                                                   np.where(((down==2) & (16 <= dist)), "2[16+]",
                                                                            np.where(((down==3) & (1 <= dist) &(dist <= 3)), "3[1-3]",
                                                                                     np.where(((down==3) & (4 <= dist) &(dist <= 7)), "3[4-7]",
                                                                                              np.where(((down==3) & (8 <= dist) &(dist <= 15)), "3[8-15]",
                                                                                                       np.where(((down==3) & (16 <= dist)), "3[16+]",
                                                                                                                np.where(((down==4) & (1 <= dist) &(dist <= 3)), "4[1-3]",
                                                                                                                         np.where(((down==4) & (4 <= dist) &(dist <= 7)), "4[4-7]",
                                                                                                                                  np.where(((down==4) & (8 <= dist) &(dist <= 15)), "4[8-15]",
                                                                                                                                           np.where(((down==4) & (16 <= dist)), "4[16+]", 'na')))))))))))))))
df['new_bin'] = df['bin'] + '' + df['yardline']        

df['points'] = np.where(df['pff_DRIVEENDEVENT']=='TOUCHDOWN', 6, 
                         np.where(df['pff_DRIVEENDEVENT']=='FIELD GOAL',3,
                                  np.where(df['pff_DRIVEENDEVENT']=='SAFETY',-2,
                                           np.where(df['pff_DRIVEENDEVENT'] == 'FUMBLE-TD', -6,
                                                    np.where(df['pff_DRIVEENDEVENT']=='INTERCEPTION-TD', -6,float('nan'))))))
# Now have to figure out how to get the point value of each drive

# loop through each row, store them in a new df, and when the loop reaches a point where
# there is a score value, assign all the rows in the new df that value
# but what about +/-? : + for the rows where the defteam is not the same as the row where
# the loop stopped
df2 = df.reset_index()
df2 = df2.iloc[0:102,]        

# need to remove drives that carry over into 2nd and 4th quarter

# drive play does not equal drive end play
# if the last entry in temp6 field position does not equal drive end field position
# then dont append those rows to the df
# tstart = time.time()

# temp5 = pd.DataFrame()
# temp6 = pd.DataFrame()
# temp7 = pd.DataFrame()
# for i,r in df2.iterrows():
#     temp5 = temp5.append(r)
#     temp6 = temp6.append(r)
#     if pd.isna(r['pff_DRIVE']):
#         temp2['points'] = r['points']
#         new = temp2.iloc[-1]['pff_DEFTEAM']
#         #print(new)
#         temp2['points'] = np.where(temp2['pff_DEFTEAM']==new, temp2['points']*1, temp2['points']*-1)
#         #new2 = temp6.iloc[-1]['pff_DRIVEPLAY']
#         #new3 = temp6.iloc[-1]['pff_DRIVEENDPLAYNUMBER']
#         #print(str(new2) + ' ' + str(new3))
#         #if new2 != new3:
#             temp7 = temp7.append(temp6)
#         temp5 = pd.DataFrame()
#         temp6 = pd.DataFrame()



# tend = time.time()
# print(tend-tstart)


tstart = time.time()
temp = pd.DataFrame(columns = ['points'])
temp2 = pd.DataFrame(columns = ['points'])
temp3 = pd.DataFrame(columns=['points'])

for i,r in df.iterrows():
    temp = temp.append(r)
    temp2 = temp2.append(r)
    #print(temp['pff_DEFTEAM'])
    if pd.notnull(r['points']):
        temp2['points'] = r['points']
        new = temp2.iloc[-1]['pff_DEFTEAM']
        #print(new)
        temp2['points'] = np.where(temp2['pff_DEFTEAM']==new, temp2['points']*1, temp2['points']*-1)
        temp3 = temp3.append(temp2)
        temp = pd.DataFrame(columns = ['points'])
        temp2 = pd.DataFrame(columns = ['points'])

tend = time.time()
print(tend-tstart) # 1047 seconds

temp4 = df.loc[df['points'].notnull()]
temp3['new_bin'] = '' + temp3['bin'] + '' + temp3['yardline']        

# from this stage, if we have a scenario, the expected points would be whats in this table?
gb = temp3['points'].groupby(temp3['new_bin']).mean()
gb = gb.iloc[0:-7]

# visualize
gb = gb.reset_index()
plt.bar(gb['new_bin'], gb['points'])
plt.xticks(rotation=45, fontsize=9)
plt.show()
gb.to_csv('exp_value.csv', header=True)

