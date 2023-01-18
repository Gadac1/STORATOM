import numpy as np
from solver import *

a = (np.zeros(200) + 200)/eta
b = np.array([200,195,190,185,180,175,170,165,160,155,150,145,140,135,130,125,120,115,110,105])/eta
c = (np.zeros(890) + 100)/eta
d = np.array([110,120,130,140,150,160,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,380])/eta
e  = (np.zeros(800) + 390)/eta
f= np.concatenate((a,b,c,d,e)) # Test grid load
P_grid_test = np.concatenate((f,f[::-1]*0.9))
