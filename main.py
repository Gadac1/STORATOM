from solver import *
from load_interpolation import *
import numpy as np

def run(PN_reac, storage_time):

    (reac, hot_tank, cold_tank, storage_load_hx, max_stored_energy, P_unload_max)  = system_initialize(PN_reac, storage_time)
    P_grid = np.array(profil_80EnR_sem_hiver)*(system_max_power/eta)/100
    (Time, P_core, P_load, P_unload, stored_energy) = load_following(P_grid, reac, hot_tank, cold_tank, storage_load_hx, max_stored_energy, P_unload_max)

    print('')
    print('Case study :')
    print('     Reactor nominal power: ' + str(PN_reac) + 'MWe')
    print('     Storage system power: ' + str(system_max_power - PN_reac) + 'MWe')
    print('     Nominal storage time: ' + str(storage_time) + 'h')
    print('')
    print('Results :')
    print('     Storage capacity: ' + str(int(Joules_to_MWh(max_stored_energy))) + 'MWh')
    print('     Mass of nitrate salt: ' + str(int(hot_tank.V_max*nitrate_salt.rho/1000)) + 't')
    print('     Load factor of reactor with storage: ' + str(load_factor(P_grid, P_core, reac)) + '%')
    print('     Consumption-Production equilibrium: ' + str(grid_equilibrium(P_grid, P_core, P_unload)))
    print('')

    print_load_graph(P_grid, reac, hot_tank, cold_tank, storage_load_hx, max_stored_energy, P_unload_max, Time, P_core, P_load, P_unload, stored_energy, 0, len(P_grid)-1)

def storage_time_study(PN_reac):
    c = 0
    eq = False
    while eq == False: 
        c+=1
        (reac, hot_tank, cold_tank, storage_load_hx, max_stored_energy, P_unload_max)  = system_initialize(PN_reac, c)
        P_grid = np.array(profil_80EnR_sem_hiver)*(system_max_power/eta)/100
        (Time, P_core, P_load, P_unload, stored_energy) = load_following(P_grid, reac, hot_tank, cold_tank, storage_load_hx, max_stored_energy, P_unload_max)
        eq = grid_equilibrium(P_grid, P_core, P_unload)
    return c
