# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 20:46:33 2020

@author: maric
"""
#This code adapts .dat files to version 07.02.2021 of Digital Semiology
import pickle
ictal_episode_code=input('Please, write the code of this ictal episode and then press Enter\n')
DS_version=input('Please, write the version of Digital Semiology and then press Enter\n')
filename='ictal_episode_' + ictal_episode_code +'.dat'
f=open(filename, 'rb') 
ds_starter = pickle.load(f)
ictus=pickle.load(f)
report=pickle.load(f)
software_user_dialogue=pickle.load(f)
f.close()
name_changer=0
for i in range (0,len(ictus)):
    for j in range (4,len(ictus[i])):
        if ictus[i][0]==0: #Simple motor
            if len(ictus[i][j])<52:
                ictus[i][j]=ictus[i][j]+['']*(52-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==1: #Automatisms
            if len(ictus[i][j])<12:
                ictus[i][j]=ictus[i][j]+['']*(12-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==2: #Autonomic
            if len(ictus[i][j])<4:
                ictus[i][j]=ictus[i][j]+['']*(4-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==3: #Eye movements
            if len(ictus[i][j])<23:
                ictus[i][j]=ictus[i][j]+['']*(23-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==4: #Hyperkinetic
            if len(ictus[i][j])<12:
                ictus[i][j]=ictus[i][j]+['']*(12-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==5: #Voice
            if len(ictus[i][j])<3:
                ictus[i][j]=ictus[i][j]+['']*(3-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==6: #Dialeptic
            if len(ictus[i][j])<13:
                ictus[i][j]=ictus[i][j]+['']*(13-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==7: #GTCS
            if len(ictus[i][j])<3:
                ictus[i][j]=ictus[i][j]+['']*(3-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==8: #Aura reporting
            if len(ictus[i][j])<133:
                ictus[i][j]=ictus[i][j]+['']*(133-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==9: #"Other"
            if len(ictus[i][j])<28:
                ictus[i][j]=ictus[i][j]+['']*(28-len(ictus[i][j]))
                name_changer=1
        if ictus[i][0]==10: #Trigger
            if len(ictus[i][j])<9:
                ictus[i][j]=ictus[i][j]+['']*(9-len(ictus[i][j]))
                name_changer=1

if name_changer==1:
    print ('ictus has been adapted to the new vesion of Digital Semiology')
    filename='ictal_episode_' + ds_starter[18] + '_vers' + DS_version +'.dat'
    output=open(filename, 'wb')  # Overwrites any existing file with the same name.
    pickle.dump(ds_starter, output)
    pickle.dump(ictus, output)
    pickle.dump(report, output)
    pickle.dump(software_user_dialogue, output)
    output.close()
else:
    print(filename+''' doesn't require adaptation to the current Digital Semiology version''')
       