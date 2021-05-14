#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 19:29:59 2021

@author: blanc
"""

import numpy as np
import pandas as pd

from collections import defaultdict

import random


# reward function
def get_reward(df, gamma = 0.65):
    df['reward'] = 100 - (df.index.values ** (gamma))
    df = df[df.reward > 40]
    return df


#%%
df_actions = pd.read_csv('./simulation/ch2_actions.csv')
df_actions.columns = ['action']
df_actions = df_actions[::-1].reset_index(drop=True)


#%%

df_states = pd.read_csv('./simulation/ch2.csv', sep='#' )
df_states.columns = ['state']
df_states = df_states[::-1].reset_index(drop=True)


#%%

df_actions = get_reward(df_actions)

df_actions['state'] = df_states['state']


#%%

dchaser = defaultdict()

#%%


for row in df_actions.iterrows():
    action = row[1][0]
    reward = row[1][1]
    state = row[1][2]

    if(state not in dchaser.keys()):
        dchaser[state] = defaultdict(list)
    dchaser[state][action].append(reward)
#%%

for state in range(10):
    for x in range(50):
        rnd_act = random.randint(0, 4)
        rnd_score = random.randint(20, 100)
        if(state not in dchaser.keys()):
            dchaser[state] = defaultdict(list)

        dchaser[state][rnd_act].append(rnd_score)


#%%

for keys in dchaser[1]:
    print(sum(dchaser[1][a]) / len(dchaser[1][a]))
