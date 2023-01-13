import pandas as pd
import numpy as np
from numpy import linalg
from numpy.linalg import eig
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


data = pd.read_excel('SB_box_scores_2019_without_rank.xlsx')
data['Point_diff'] = data['Pts_winner']-data['Pts_loser']



team_wins = data['Winner'].value_counts().sort_index()




team_names = pd.concat([data['Winner'], data['Loser']])
team_names = team_names.sort_values()
team_names = team_names.reset_index()
team_names = team_names[0]
team_names = team_names.drop_duplicates()
team_names = team_names.reset_index(drop=True)



total_games = team_names.value_counts().sort_index()



win_pct = team_wins/total_games
win_pct = win_pct.fillna(0)
win_pct = win_pct.sort_values(ascending=False)
mat = np.zeros((len(team_names), len(team_names)))
mat = pd.DataFrame(mat, columns=team_names, index=team_names)

empt = []
for i in team_names:
    yur = data[(data['Winner'] == i) | (data['Loser'] == i)]
    empt.append(yur)




for df,name in zip(empt, team_names):
    df['multiplier'] = np.where((df['Loser'] == name), -1, 1)



for df in empt:
    df['new_score_diff'] = df['multiplier'] * df['Point_diff']


empt2 = []
for df in empt:
   df = df.loc[:,['Winner', 'Loser', 'new_score_diff']]
   empt2.append(df)

new = pd.concat(empt2)
new2  = new.pivot_table(index="Winner", columns = "Loser", values = "new_score_diff")


win_df = new[new['new_score_diff']>0]
lose_df = new[new['new_score_diff']<0]

win2 = win_df.pivot_table(index="Winner", columns = "Loser", values = "new_score_diff")
lose2 = lose_df.pivot_table(index="Loser", columns = "Winner", values = "new_score_diff")

df3 = pd.concat([win2, lose2], axis=1)
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
temp = df3.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))
temp = temp.sort_index()

temp = temp.mask(temp == '')
temp = temp.fillna(0.00000000000000000000000000000000000000000000000000000000000001)
temp = temp.astype(float)
temp = temp.div(temp.sum(axis=1), axis=0)

w,v = eig(temp)
v = abs(v)

Eigenvalues, Eigenvectors = np.linalg.eig(np.transpose(temp))
ss = np.abs(Eigenvectors[:,np.argmax(np.abs(Eigenvalues))])
ser = pd.Series(ss, name = "result")
ser2 = pd.concat([ser, team_names], axis=1)
rankings = ser2.sort_values(by = "result", ascending=False)

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=rankings.values,colLabels=rankings.columns,loc='center')
pp = PdfPages("table.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
