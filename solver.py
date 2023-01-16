from class_definition import *
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.pyplot as mplt

# All temps in °C
# All masses in kg
# All powers in MWth
# All volumes in m3

eta = 0.33
dt = 60
storage_level = 0.5 # Level of thermal storage system at the start of the simulation

reac = Reactor(345/eta, 200/eta, 0.05, 550, 400)
sodium = Fluid(927, 1230, 84)

nitrate_salt = Fluid(1772, 1500, 0.443)
hot_tank = Tank(15700, storage_level*15700, nitrate_salt, 500)
cold_tank = Tank(hot_tank.V_max, hot_tank.V_max - hot_tank.V, nitrate_salt, 290)
storage_load_hx = Heat_exchanger(345/eta, reac.T_out, reac.T_in, cold_tank.T_tank, hot_tank.T_tank)
max_stored_energy = hot_tank.V_max * nitrate_salt.rho * hot_tank.fluid.cp * (hot_tank.T_tank - cold_tank.T_tank)
P_unload_max = 155/eta 

a = (np.zeros(550) + 200)/eta
c = np.array([200,195,190,185,180,175,170,165,160,155,150,145,140,135,130,125,120,115,110])/eta
b = (np.zeros(890) + 100)/eta
d = np.concatenate((a,c))
P_grid = np.concatenate((d,b))
# P_grid = np.zeros(3*1440)+200/eta
Time = np.zeros(len(P_grid))

P_core = np.zeros(len(P_grid))
P_core[0] = reac.P
P_load = np.zeros(len(P_grid))
P_unload = np.zeros(len(P_grid))

V_hot_tank = np.zeros(len(P_grid))
V_hot_tank[0] = hot_tank.V
V_cold_tank = np.zeros(len(P_grid))
V_cold_tank[0] = cold_tank.V

mfr_secondary_tot = np.zeros(len(P_grid))
mfr_storage = np.zeros(len(P_grid))

stored_energy = np.zeros(len(P_grid))
stored_energy[0] = hot_tank.fluid_mass()*hot_tank.fluid.cp*(storage_load_hx.T_cold_out - storage_load_hx.T_cold_in) # Amount of energy currently in the thermal storage system

test = np.zeros(len(P_grid))

for t in range(len(P_grid)-1):

    Time[t] = t
    mfr_secondary_tot[t] = reac.P / (sodium.cp * (reac.T_out - reac.T_in))

    if P_grid[t] <= 0:
        t_reac_stop = reac.P/(reac.P_grad*reac.P_max) # Time to stop the reactor in minutes starting now in min
        test[t] = t_reac_stop

        if stored_energy[t] + MW_to_W(reac.P)*dt*t_reac_stop/2 < max_stored_energy - MW_to_W(reac.P)*dt: # Checking if the storage system would be saturated if we did not cut the reactor power now           
            P_load[t] = reac.P
            stored_energy[t+1] = stored_energy[t] + MW_to_W(reac.P)*dt

            if reac.P < reac.P_max:
                if reac.P_max - reac.P < reac.P_grad*reac.P_max:
                    reac.P = reac.P_max
                    P_core[t+1] = reac.P
                else:
                    reac.P += reac.P_grad*reac.P_max
                    P_core[t+1] = reac.P
            else:
                P_core[t+1] = reac.P

        else:
            if reac.P-reac.P_grad*reac.P_max <=0:
                reac.P = 0
                P_core[t+1] = reac.P
            else:
                reac.P -= reac.P_grad*reac.P_max
                P_core[t+1] = reac.P
            P_load[t] = reac.P
            stored_energy[t+1] = stored_energy[t] + MW_to_W(reac.P)*dt        

    else:
        t_reac_grid = (reac.P-P_grid[t])/(reac.P_grad*reac.P_max) #Time for the reactor to match the grid power level

        if P_grid[t] <= reac.P:
            if stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt*t_reac_grid/2 < max_stored_energy - (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt:
                P_load[t] = reac.P - P_grid[t]
                stored_energy[t+1] = stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt

                if reac.P < reac.P_max:
                    if reac.P_max - reac.P < reac.P_grad*reac.P_max:
                        reac.P = reac.P_max
                        P_core[t+1] = reac.P
                    else:
                        reac.P += reac.P_grad*reac.P_max
                        P_core[t+1] = reac.P
                else:
                    P_core[t+1] = reac.P                

            else:
                if reac.P-reac.P_grad*reac.P_max <= P_grid[t]:
                    reac.P = P_grid[t]
                    P_core[t+1] = reac.P
                else:
                    reac.P -= reac.P_grad*reac.P_max
                    P_core[t+1] = reac.P
                P_load[t] = reac.P - P_grid[t]
                stored_energy[t+1] = stored_energy[t] + (MW_to_W(reac.P) - MW_to_W(P_grid[t]))*dt
        



def print_graph():
    range = (0,1439)
    # range = (90,120)

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
    plt.gca().set_ylim(-10,350)
    plt.grid()
    plt.show()

    plt.plot(Time[range[0]:range[1]], P_load[range[0]:range[1]]*eta)
    plt.xlabel("Time (min)")
    plt.ylabel("Storage input power (MW)")
    plt.gca().set_ylim(-10,350)
    plt.grid()
    plt.show()

    print((stored_energy[-1])/3.6e9)

# if __name__ == '__main__':
#     print_graph()
