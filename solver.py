from class_definition import *
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.pyplot as mplt

# All temps in °C
# All masses in kg
# All powers in MWth
# All volumes in m3

eta = 0.33 # Turbine efficiency
dt = 60 # Time step in seconds
grad = 5/6000 # Reactor power gradient in %/s
storage_level = 0.1 # Level of thermal storage system at the start of the simulation

reac = Reactor(345/eta, 345/eta, grad*dt, 550, 400) # Reactor initialization
sodium = Fluid(927, 1230, 84) # Secondary fluid initialization

nitrate_salt = Fluid(1772, 1500, 0.443) # Storage fluid initialization
hot_tank = Tank(15700, storage_level*15700, nitrate_salt, 500) # Hot tank initialization
cold_tank = Tank(hot_tank.V_max, hot_tank.V_max - hot_tank.V, nitrate_salt, 290) # Cold tank initialization
storage_load_hx = Heat_exchanger(345/eta, reac.T_out, reac.T_in, cold_tank.T_tank, hot_tank.T_tank) # Secondary-to-storage heat exchanger initialization
max_stored_energy = hot_tank.V_max * nitrate_salt.rho * hot_tank.fluid.cp * (hot_tank.T_tank - cold_tank.T_tank) # Computing the maximum storable energy in the storage system
P_unload_max = 155/eta # Parameter setting the maximum discharge rate of the storage system

a = (np.zeros(200) + 200)/eta
b = np.array([200,195,190,185,180,175,170,165,160,155,150,145,140,135,130,125,120,115,110])/eta
c = (np.zeros(890) + 100)/eta
d = np.array([110,120,130,140,150,160,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,380,390,400])/eta
# d = np.array([110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,270,280,290,300,310,320,330,340,345])/eta
e  = (np.zeros(800) + 420)/eta
# e = (np.zeros(550) + 345)/eta
P_grid = np.concatenate((a,b,c,d,e)) # Test grid load

Time = np.zeros(len(P_grid))

P_core = np.zeros(len(P_grid))
P_core[0] = reac.P
P_load = np.zeros(len(P_grid))
P_unload = np.zeros(len(P_grid))

V_hot_tank = np.zeros(len(P_grid))
V_hot_tank[0] = hot_tank.V
V_cold_tank = np.zeros(len(P_grid))
V_cold_tank[0] = cold_tank.V

stored_energy = np.zeros(len(P_grid))
stored_energy[0] = hot_tank.fluid_mass()*hot_tank.fluid.cp*(storage_load_hx.T_cold_out - storage_load_hx.T_cold_in) # Amount of energy at the start in the thermal storage system

mfr_secondary_tot = np.zeros(len(P_grid))
mfr_storage = np.zeros(len(P_grid))

def load_following(P_grid):

    for t in range(len(P_grid)-1): # Iteration over the time range given by the grid input
        
        Time[t] = t     
        # We first study the case were the reactor output is above the demand by the electrical grid
        if P_grid[t] <= reac.P:
            #We compute the time for the reactor to match the grid power level (could be <0):
            t_reac_grid = (reac.P-P_grid[t])/(reac.P_grad*reac.P_max) 

            # We then compute the amount of energy that would still be irremediably stored by the reactor if it were to start matching the grid demand
            # We can now check if the storage system would be saturated by this energy if we did not reduce the output of the reactor power now:
            if stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt*t_reac_grid/2 < max_stored_energy - (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt:
                P_load[t] = reac.P - P_grid[t]
                # In that case we can store the difference of the reactor output and the grid demand over this step in the storage system
                stored_energy[t+1] = stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt
                # If the reactor can be throttled up, in that case we increase the power level by the allowable power gradient 
                if reac.P < reac.P_max:
                    if reac.P_max - reac.P < reac.P_grad*reac.P_max:
                        reac.P = reac.P_max
                        P_core[t+1] = reac.P
                    else:
                        reac.P += reac.P_grad*reac.P_max
                        P_core[t+1] = reac.P
                else:
                    P_core[t+1] = reac.P                

            # If the previous condition lead to the saturation of the thermal storage, we start throttling back the reactor to the grid power requirement now:
            else:
                if reac.P-reac.P_grad*reac.P_max <= P_grid[t]:
                    reac.P = P_grid[t]
                    P_core[t+1] = reac.P
                else:
                    reac.P -= reac.P_grad*reac.P_max
                    P_core[t+1] = reac.P
                P_load[t] = reac.P - P_grid[t]
                # We add the energy produced at this time step by the reduced power output to the energy level of the next step:
                stored_energy[t+1] = stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt
            
        # Now we assume the grid demands a higher power than what the reactor is outputting
        else:
            if P_grid[t] <= reac.P_max:
                # If the grid level is above what the reactor is outputting and the reactor is below is rated power, we throttle up the reactor    
                if reac.P < reac.P_max:
                    # If throttling up the reactor causes it to go beyond the grid requirements, we match the grid
                    if  reac.P+reac.P_grad*reac.P_max >= P_grid[t]:
                        reac.P = P_grid[t]
                        stored_energy[t+1] = stored_energy[t]
                        P_core[t] = reac.P
                        P_core[t+1] = reac.P
                    # If the reactor is near P_max, we match P_max
                    elif reac.P_max - reac.P < reac.P_grad*reac.P_max:
                        reac.P = reac.P_max
                        stored_energy[t+1] = stored_energy[t]
                        P_core[t] = reac.P
                        P_core[t+1] = reac.P
                    # Else that means throttling up the reactor does not allow to follow the load. In that case we still throttle it up and we use the
                    # storage system as a gap filler to match the load:
                    else :
                        if stored_energy[t] == 0:
                            P_unload[t] = 0
                        else:
                                P_unload[t] = min(P_grid[t] - reac.P, P_unload_max) # Storage system serving as stopgap for rapid load following
                        stored_energy[t+1] = max(0,stored_energy[t] - MW_to_W(P_unload[t])*dt)
                        reac.P += reac.P_grad*reac.P_max
                        P_core[t] = reac.P
                        P_core[t+1] = reac.P
                
            # If the load goes beyond the rated power of the reactor, we start unloading the storage system:
            else:
                if stored_energy[t] == 0:
                    P_unload[t] = 0
                else:
                    P_unload[t] = min(P_grid[t] - reac.P_max, P_unload_max)
                stored_energy[t+1] = max(0,stored_energy[t] - MW_to_W(P_unload[t])*dt)
                reac.P = reac.P_max
                P_core[t] = reac.P_max
                P_core[t+1] = reac.P_max
                    
def print_graph(x1,x2):
    
    range = (x1,x2)

    plt.plot(Time[range[0]:range[1]], Joules_to_MWh(stored_energy[range[0]:range[1]]))
    plt.xlabel("Time (min)")
    plt.ylabel("Stored energy (MWh)")
    plt.gca().set_ylim(-10,2500) 
    plt.grid()
    plt.show()

    plt.plot(Time[range[0]:range[1]], P_core[range[0]:range[1]]*eta, label = "Reactor power level")
    plt.plot(Time[range[0]:range[1]], P_grid[range[0]:range[1]]*eta, label = "Grid electrical load")
    plt.xlabel("Time (min)")
    plt.ylabel("Core output power and load from the grid (MW)")
    plt.legend(loc='best')
    plt.gca().set_ylim(-10,520)
    plt.grid()
    plt.show()

    plt.plot(Time[range[0]:range[1]], (P_load[range[0]:range[1]] - P_unload[range[0]:range[1]])*eta)
    plt.xlabel("Time (min)")
    plt.ylabel("Storage input power (MW)")
    plt.gca().set_ylim(-160,350)
    plt.grid()
    plt.show()


load_following(P_grid)
print_graph(0, 1900)