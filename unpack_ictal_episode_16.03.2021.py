import pickle
import numpy as np
# Reading the .dat file (binary) 
ictal_episode_code=input('Please, write the code of this ictal episode and then press Enter\n')
filename='ictal_episode_' + ictal_episode_code +'.dat'
f=open(filename, 'rb') 
ds_starter = pickle.load(f)
ictus=pickle.load(f)
report=pickle.load(f)
software_user_dialogue=pickle.load(f)
f.close()

print (report)

print ('\n\t\tICTUS: encoded data regarding this ictal episode\n\n',ictus)
event_matrix=np.zeros((5,len(ictus)))
#event_matrix is 5Xn array, where n is number of events, so that every column 
#of event_matrix corresponds to individual event.
#the first row of event_matrix correspond to codes of events
#the second and third rows correspond to timing in hhmmss of
#event start (second row) and event end (third row)
#the fourth and fith rows correspond to timing in seconds of
#event start (second row) and event end (third row)

for i in range (0,len(ictus)):
    event_matrix[0,i]=ictus[i][0] 
for i in range (0,len(ictus)):
    event_matrix[1,i]=ictus[i][2]
for i in range (0,len(ictus)):
    event_matrix[2,i]=ictus[i][3] 
for i in range (0,len(ictus)):
    event_matrix[3,i]=int(ictus[i][2][0:2])*60**2+int(ictus[i][2][2:4])*60+int(ictus[i][2][4:])
for i in range (0,len(ictus)):
    event_matrix[4,i]=int(ictus[i][3][0:2])*60**2+int(ictus[i][3][2:4])*60+int(ictus[i][3][4:])
    
# Constructing plot of ictal episode
import matplotlib.pyplot as plt
episode_duration = np.arange(int(np.amax(event_matrix[3:]))-int(np.amin(event_matrix[3:]))+1)
timings = int(np.amin(event_matrix[3:])) + episode_duration
events_binary = np.zeros((event_matrix.shape[1],len(episode_duration)))
for i in range (0, event_matrix.shape[1]):
    for j in range(0,len(episode_duration)):
        if int(event_matrix[3,i])<=timings[j] and int(event_matrix[4,i])>=timings[j]:
            events_binary[i,j]=1
fig, ax = plt.subplots(figsize=(10,5))
labels=['']*event_matrix.shape[1]
for i in range (0,event_matrix.shape[1]):
    labels[i]='Event '+str(i+1)
#ax.stackplot(timings,  events_binary , labels=labels): for abolute time in seconds
#ax.set_xlim(left=timings[0], right=timings[-1]) for absolute time in seconds
ax.stackplot(episode_duration,  events_binary , labels=labels)# for time from ictal episode start
ax.set_xlim(0, episode_duration[-1])# for time from ictal episode start
ax.legend(loc='')
ax.set_title('Ictal Episode')
ax.set_ylabel('number of events in the given second')
ax.set_xlabel('time in seconds from ictal episode start')
fig.tight_layout()

# Generating the .txt file
text_file=open("ictal_episode"+ictal_episode_code+".txt", "w", encoding='utf-8')
text_file.write(report)
text_file.close()   
input ("\nPress Enter to exit")   