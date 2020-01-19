# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:29:55 2019

This is the first version of the Ex 1- Same structure as in the Matlab exercise.
@author: mendez
"""

import numpy as np
import matplotlib.pyplot as plt

Anim=False
## Set Up and Create Data Matrix D

# 1 . Data Preparation
dt =0.5; t =np.arange(0,620+dt,dt); n_t=len(t); #Time Discretization
dy =0.01; y=np.arange(-1,1+dy,dy); n_y=len(y); #Space Discretization

# Set the parameters of the two pressure pulsation
W_1=4      # Womersley 1
Pa_1=20    # P Amplitude 1
W_2=1      # Womersley 2
Pa_2=2     # P Amplitude 2
u_A_r_1=np.zeros((n_y,n_t)) # Solution W_1
u_A_r_2=np.zeros((n_y,n_t)) # Solution W_2

# Add a step-like growth of the large scale mode 
# and a gaussian window to the fast scale
T_A_F=max(t)/2 # Location of the window center
STEP_S=np.ones(np.shape(t)) # Initialize the step
STEP_S[0:int(np.floor(n_t/10)):1]=0
STEP_S[int(len(STEP_S)-np.floor(n_t/10)):len(STEP_S):1]=0 # Step Definition
#Smooth the step like kernel
N_M=50;  
h=np.ones((N_M))/N_M # Create impulse response moving average

# We construct a smoothed step repeading 5 times a median filter
for i in range(0,4):
  STEP_S=np.convolve(STEP_S,h,'same')
  
# Create also the second kind of smoothed STEP
STEP_F=np.exp(-(t-T_A_F)**2/5000);  
# Check them
#plt.plot(t,STEP_S) 
#plt.plot(t,STEP_F)


  
  
 # 2. Initialize Matrices:
n = np.arange(0,20,1) 
N=len(n) #Modes to include in summation :
Y_n1=np.zeros((n_y,N)) #Initialize Spatial Basis
A_n1=np.zeros((N,N)) #Initialize Amplitude Matrix
T_n1=np.zeros((n_t,N)) #Initialize Temporal Basis
U_A1=np.zeros((n_t,n_y)) #Initialize PDE solution
 
Y_n2=np.zeros((n_y,N)) #Initialize Spatial Basis
A_n2=np.zeros((N,N)) #Initialize Amplitude Matrix
T_n2=np.zeros((n_t,N)) #Initialize Temporal Basis
U_A2=np.zeros((n_t,n_y)) #Initialize PDE solution
    
# 3. Construct Spatial Eigenfunction basis (Fast Scale)
ns=np.zeros(n.shape)
for i in range(0,20):     
  N=2*i+1; # odd number in the series
  ns[i]=N
  # Pulsation Mode 1
  Y_n1[:,i]=np.cos(N*np.pi*y/2) # Spatial Eigenfunction basis
  A_n1[i,i] =(16*Pa_1)/(N*np.pi*np.sqrt((2*W_1)**4+N**4*np.pi**4)); # Amplitudes 
  T_n1[:,i]=(-1)**(i+1)*np.sin(t)*STEP_F# # Temporal coefficients
  # Pulsation Mode 2
  Y_n2[:,i]=np.cos(N*np.pi*y/2); # Spatial Eigenfunction basis
  A_n2[i,i]=(16*Pa_2)/(N*np.pi*np.sqrt((2*W_2)**4+N**4*np.pi**4)); # Amplitudes 
  T_n2[:,i]=(-1)**(i+1)*np.sin((W_2/W_1)**2*t)*STEP_S; # Temporal coefficients
     

 # Assembly the response to each pulsation 
u_A_r_1=np.linalg.multi_dot([Y_n1,A_n1,np.transpose(T_n1)])
u_A_r_2=np.linalg.multi_dot([Y_n2,A_n2,np.transpose(T_n2)])
  
# Observe the time evolution in the centerline for each
fig, ax = plt.subplots(figsize=(8,5))
plt.rc('text', usetex=True)      # This is Miguel's customization
plt.rc('font', family='serif')
plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
plt.plot(t,u_A_r_2[int(np.floor(n_y/2)),:],'r-')
plt.plot(t,u_A_r_1[int(np.floor(n_y/2)),:],'k-')
plt.xlabel('$\hat{t}$',fontsize=22)
plt.ylabel('$\hat{u}(\hat{y}=0,t)$',fontsize=22)
plt.title('Centerline Vel Evolution',fontsize=20)
plt.tight_layout(pad=0.6, w_pad=0.3, h_pad=0.8)
pos1 = ax.get_position() # get the original position 
pos2 = [pos1.x0 + 0.01, pos1.y0 + 0.01,  pos1.width *0.95, pos1.height *0.95] 
ax.set_position(pos2) # set a new position
plt.savefig('Centerline_Evolution.png', dpi=300)     
plt.close(fig)
 
#Assembly the Data Matrix for the test Case
u_Mb=0.5*(1-y**2) #Compute the mean Flow
u_M=np.transpose(np.tile(u_Mb,(n_t,1))) #Repeat mean to obtain a matrix
D=u_A_r_1+u_A_r_2+u_M #Complete analytical Solution (also adding back the mean)

 
# Obs: In constructing D, it is better to avoid windowing problems.
# In this case, noise could be generated by the large scale at the right
# border. To reduce this problem, it is better to limit it so as to have a
# smoother transition. This is equivalent to Hann windowing a signal before
# computing the spectra. The windows used in the scale can be useful to
# this end.

# Save as numpy array all the data
np.savez('Data',D=D,t=t,dt=dt,n_t=n_t,y=y,dy=dy,n_y=n_y)
 
from Others import Animation

if Anim:
## Visualize entire evolution (Optional)
 Animate=Animation('Data.npz','Exercise_1.gif')
else:
 print('No animation requested')    
    
    
    