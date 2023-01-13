import pandas as pd
import numpy as np
import random

#%% Question 1
def transition_matrix(states):
    k = states
    result = np.identity(k)
    result = result + np.random.uniform(size=(k, k))
    # divide by row-wise sum to normalize to 1.
    result = result / result.sum(axis=1, keepdims=1)
    return result

result = transition_matrix(5)
print(result)
# The sum of the rows should be 1 since each vector is a probability vector.
#%% Question 2
def initial_state(states):
    k = states
    result = np.identity(1)
    result = result + np.random.uniform(size=(1, k))
    result = result / result.sum(axis=1, keepdims=1)
    return result

result2 = initial_state(5)
print(result2)
#%% Question 3, 4
states = [0,1,2,3,4]
def markov_chain(transition_matrix, initial_state, chain_length):
    array = []
    val = 0
    for i in range(chain_length):
        if i == 1:
            val = np.random.choice(states, p=result2[0])
            array.append(val)
        else:
            val = np.random.choice(states, p = transition_matrix[val])
            array.append(val)
    return array

result3 = markov_chain(result, result2, 100000)
#%% Question 4: Hardcoding- will fix later
# This code only allows for a transition matrix of 5 states
# Need to change code to generalize this step
ct00 = 0
ct01 = 0
ct02 = 0
ct03 = 0
ct04 = 0
ct10 = 0
ct11 = 0
ct12 = 0
ct13 = 0
ct14 = 0
ct20 = 0
ct21 = 0
ct22 = 0
ct23 = 0
ct24 = 0
ct30 = 0
ct31 = 0
ct32 = 0
ct33 = 0
ct34 = 0
ct40 = 0
ct41 = 0
ct42 = 0
ct43 = 0
ct44 = 0
for i in range(0,len(result3)-1):
    if result3[i]==0: 
        if result3[i+1]==0:
            ct00 += 1
        if result3[i+1]==1:
            ct01 += 1   
        if result3[i+1]==2:
            ct02 += 1
        if result3[i+1]==3:
            ct03 += 1
        if result3[i+1]==4:
            ct04 += 1
    if result3[i]==1: 
        if result3[i+1]==0:
            ct10 += 1
        if result3[i+1]==1:
            ct11 += 1   
        if result3[i+1]==2:
            ct12 += 1
        if result3[i+1]==3:
            ct13 += 1
        if result3[i+1]==4:
            ct14 += 1
    if result3[i]==2: 
        if result3[i+1]==0:
            ct20 += 1
        if result3[i+1]==1:
            ct21 += 1   
        if result3[i+1]==2:
            ct22 += 1
        if result3[i+1]==3:
            ct23 += 1
        if result3[i+1]==4:
            ct24 += 1
    if result3[i]==3: 
        if result3[i+1]==0:
            ct30 += 1
        if result3[i+1]==1:
            ct31 += 1   
        if result3[i+1]==2:
            ct32 += 1
        if result3[i+1]==3:
            ct33 += 1
        if result3[i+1]==4:
            ct34 += 1
    if result3[i]==4: 
        if result3[i+1]==0:
            ct40 += 1
        if result3[i+1]==1:
            ct41 += 1   
        if result3[i+1]==2:
            ct42 += 1
        if result3[i+1]==3:
            ct43 += 1
        if result3[i+1]==4:
            ct44 += 1

ct0 = ct00 + ct01 + ct02 + ct03 + ct04
ct1 = ct10 + ct11 + ct12 + ct13 + ct14
ct2 = ct20 + ct21 + ct22 + ct23 + ct24
ct3 = ct30 + ct31 + ct32 + ct33 + ct34
ct4 = ct40 + ct41 + ct42 + ct43 + ct44

ct0ar = np.array([ct00, ct01, ct02, ct03, ct04]).reshape(1, 5)
ct1ar = np.array([ct10, ct11, ct12, ct13, ct14]).reshape(1, 5)
ct2ar = np.array([ct20, ct21, ct22, ct23, ct24]).reshape(1, 5)
ct3ar = np.array([ct30, ct31, ct32, ct33, ct34]).reshape(1, 5)
ct4ar = np.array([ct40, ct41, ct42, ct43, ct44]).reshape(1, 5)

ct0ar = ct0ar/ct0
ct1ar = ct1ar/ct1
ct2ar = ct2ar/ct2
ct3ar = ct3ar/ct3
ct4ar = ct4ar/ct4

final = np.vstack([ct0ar, ct1ar, ct2ar, ct3ar, ct4ar])
subt = final - result
# The estimate is extremely close to the original. The "subt" matrix shows that the 
# difference between the estimated transition matrix and real transition matrix
# entries are essentially zero. 
#%% Question 5
mark = pd.DataFrame(result3, columns=['chain'])
temp = mark.value_counts()
temp = temp / sum(temp)
temp = np.array(temp)
temp = temp.reshape(1,5)
calc = np.matmul(temp, result)
print(calc)

# The proportions do not change much when multiplied by the transition matrix. 
#%%