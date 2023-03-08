from class_definition import *
from load_interpolation import * 
from interface import *

import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# All temps in °C
# All masses in kg
# All powers in MWth for calculations (eta for conversions)
# All volumes in m3

######################################################
##########  Important simulation parameters ##########
######################################################

dt = 60 # Time step in seconds
grad = 5/6000 # Reactor power gradient in %/s

# eta = 0.44 # Turbine efficiency
# system_max_power = 500 #MWe
# reac_T_out = 550 # Reactor secondary outlet temp (°C)
# reac_T_in = 400 # Reactor secondary inlet temp (°C)
# T_stock_hot = 500 # Reactor secondary outlet temp (°C)
# T_stock_cold = 290 # Reactor secondary inlet temp (°C)
# storage_init_level = 1 # Level of thermal storage system at the start of the simulation

######################################################
##########  Initializing working fluids ##############
######################################################

sodium = Fluid(rho = lambda T : 1014 - 0.235*(273+T), cp = lambda T : -3.001e6*(273+T)**(-2) + 1658 - 0.8479*(273+T) + 4.454e-4*(273+T)**2, k = lambda T : 104-0.047*(T+273), mu = lambda T : m.exp(556.835/(273+T) - 0.3958*m.log(273+T) - 6.4406)) # Secondary fluid initialization
nitrate_salt = Fluid(rho = lambda T : 2090 - 0.636*T, cp = lambda T : 1443 + 0.172*T, k = lambda T :  0.443 - 1.9e-4 * T, mu = lambda T : (22.714 - 0.120 * T + 2.281e-4 * T**2 - 1.474e-7 * T**3)*1e-3) # Storage fluid initialization

def system_initialize(reactor_max_power, t_unload_max):

    max_stored_energy = MW_to_W(system_max_power - reactor_max_power)*t_unload_max*3600/eta
    m_salt = max_stored_energy/(nitrate_salt.cp(T_stock_hot)*T_stock_hot-nitrate_salt.cp(T_stock_cold)*T_stock_cold)
    V_salt = m_salt/nitrate_salt.rho(T_stock_hot)
    reac = Reactor(reactor_max_power/eta, grad*dt, reac_T_out, reac_T_in) # Reactor initialization
    hot_tank = Tank(V_salt, nitrate_salt, T_stock_hot) # Hot tank initialization
    cold_tank = Tank(hot_tank.V_max, nitrate_salt, T_stock_cold) # Cold tank initialization
    P_unload_max = (system_max_power - reactor_max_power)/eta # Parameter setting the maximum discharge rate of the storage system

    return (reac, hot_tank, cold_tank, max_stored_energy, P_unload_max)

def load_following(P_grid, reac, max_stored_energy, P_unload_max):

    Time = np.zeros(len(P_grid))
    P_core = np.zeros(len(P_grid))
    reac.P = min(reac.P_max, P_grid[0])
    P_core[0] = min(reac.P_max, P_grid[0])
    P_load = np.zeros(len(P_grid))
    P_unload = np.zeros(len(P_grid))
    stored_energy = np.zeros(len(P_grid))
    stored_energy[0] =  storage_init_level*max_stored_energy# Amount of energy at the start in the thermal storage system

    for t in range(len(P_grid)-1): # Iteration over the time range given by the grid input
        Time[t] = t     
        # We first study the case were the reactor output is above the demand by the electrical grid
        if P_grid[t] <= P_core[t]:
            #We compute the time for the reactor to match the grid power level (could be <0):
            t_reac_grid = (P_core[t]-P_grid[t])/(reac.P_grad*reac.P_max) 
            # We then compute the amount of energy that would still be irremediably stored by the reactor if it were to start matching the grid demand
            # We can now check if the storage system would be saturated by this energy if we did not reduce the output of the reactor power now:
            
            if stored_energy[t] + (MW_to_W(P_core[t]) - MW_to_W(P_grid[t]))*dt*t_reac_grid/2 < max_stored_energy - 1*(MW_to_W(P_core[t]) - MW_to_W(P_grid[t]))*dt:
                # In that case we can store the difference of the reactor output and the grid demand over this step in the storage system
                P_load[t] = reac.P - P_grid[t]
                stored_energy[t+1] = min(stored_energy[t] + (MW_to_W(P_core[t]) - MW_to_W(P_grid[t]))*dt, max_stored_energy)
                # If the reactor can be throttled up, in that case we increase the power level by the allowable power gradient
                if P_core[t] < reac.P_max:
                    if reac.P_max - P_core[t] < reac.P_grad*reac.P_max and stored_energy[t+1] + (MW_to_W(reac.P_max) - MW_to_W(P_grid[t]))*dt*(1/reac.P_grad)/2 < max_stored_energy - 1*(MW_to_W(reac.P_max) - MW_to_W(P_grid[t]))*dt:
                        P_core[t+1] = reac.P_max
                    #Using the same criteria as before we check if increasing the reactor load is possible and will not saturate the storage
                    elif stored_energy[t+1] + (MW_to_W(reac.P+reac.P_grad*reac.P_max) - MW_to_W(P_grid[t]))*dt*(t_reac_grid + 1)/2 < max_stored_energy - 1*(MW_to_W(reac.P+reac.P_grad*reac.P_max) - MW_to_W(P_grid[t]))*dt:
                        reac.P += grad*reac.P_max
                        P_core[t+1] = P_core[t] + reac.P_grad*reac.P_max
                    else:
                        P_core[t+1] = P_core[t]
                else:
                    P_core[t+1] = P_core[t]               

            # If the previous condition lead to the saturation of the thermal storage, we start throttling back the reactor to the grid power requirement now:
            else:
                # We add the energy produced at this time step by the power output of the reactor to the energy level of the next step:
                P_load[t] = P_core[t] - P_grid[t]
                stored_energy[t+1] = min(stored_energy[t] + (MW_to_W(P_core[t]) - MW_to_W(P_grid[t]))*dt, max_stored_energy)
                # We then start reducing our power level
                if P_core[t]-reac.P_grad*reac.P_max <= P_grid[t]:
                    P_core[t+1] = P_grid[t]
                else:
                    P_core[t+1] = P_core[t] - reac.P_grad*reac.P_max
                 
        # Now we assume the grid demands a higher power than what the reactor is outputting
        else:
            if P_grid[t] <= reac.P_max:
                # If the grid level is above what the reactor is outputting and the reactor is below is rated power, we throttle up the reactor    
                if P_core[t] < reac.P_max:
                    # If throttling up the reactor causes it to go beyond the grid requirements, we match the grid
                    if  P_core[t]+reac.P_grad*reac.P_max >= P_grid[t]:
                        P_core[t] = P_grid[t]
                        P_core[t+1] = P_core[t]
                        stored_energy[t+1] = stored_energy[t]
                        
                    # If the reactor is near P_max, we match P_max
                    elif reac.P_max - P_core[t] < reac.P_grad*reac.P_max:
                        P_core[t] = reac.P_max
                        P_core[t+1] = P_core[t]
                        stored_energy[t+1] = stored_energy[t]
                        
                    # Else that means throttling up the reactor does not allow to follow the load. In that case we still throttle it up and we use the
                    # storage system as a gap filler to match the load:
                    else :
                        P_core[t] += reac.P_grad*reac.P_max
                        P_core[t+1] = P_core[t]
                        if stored_energy[t] == 0:
                            P_unload[t] = 0
                        else:
                            P_unload[t] = min(P_grid[t] - P_core[t], P_unload_max) # Storage system serving as stopgap for rapid load following
                        stored_energy[t+1] = max(0,stored_energy[t] - MW_to_W(P_unload[t])*dt)
                        
            # If the load goes beyond the rated power of the reactor, we start unloading the storage system:
            else:
                if stored_energy[t] == 0:
                    P_unload[t] = 0
                else:
                    P_unload[t] = min(P_grid[t] - reac.P_max, P_unload_max)
                stored_energy[t+1] = max(0,stored_energy[t] - MW_to_W(P_unload[t])*dt)
                P_core[t] = reac.P_max
                P_core[t+1] =  P_core[t]

    return (Time, P_core, P_load, P_unload, stored_energy)




