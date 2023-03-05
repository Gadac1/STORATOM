from solver import *
from load_interpolation import *
from class_definition import *
import numpy as np
import matplotlib.pyplot as plt    
from matplotlib.ticker import StrMethodFormatter



def run(PN_reac, storage_time, profile): #Simple run function for single storage experiment

    (reac, hot_tank, cold_tank, max_stored_energy, P_unload_max)  = system_initialize(PN_reac, storage_time)
    P_grid = np.array(profile)*(system_max_power/eta)/100
    (Time, P_core, P_load, P_unload, stored_energy) = load_following(P_grid, reac, max_stored_energy, P_unload_max)
    (primary_flow, load_flow, unload_flow) = compute_flows(P_core, P_load, P_unload, stored_energy)
    
    print()
    print('Case study :')
    print('     Reactor nominal power: ' + str(PN_reac) + 'MWe')
    print('     Storage system power: ' + str(system_max_power - PN_reac) + 'MWe')
    print('     Nominal storage time: ' + str(storage_time) + 'h')
    print()
    print('Results :')
    print('     Storage capacity: ' + str(int(Joules_to_MWh(max_stored_energy))) + 'MWh')
    print('     Mass of nitrate salt: ' + str(int(hot_tank.V_max*nitrate_salt.rho(hot_tank.T_tank)/1000)) + 't')
    print('     Hot salt volume: ' + str(int(hot_tank.V_max)) + 'm3')
    print('     Load factor of reactor with storage: ' + str(load_factor(P_core, reac.P_max)) + '%')
    print('     Load factor of equivalent reactor without storage: ' + str(load_factor(P_grid*eta, system_max_power)) + '%')
    eq, c = grid_equilibrium(P_grid, P_core, P_unload)
    print('     Consumption-Production equilibrium: ' + str(eq))
    if eq == False:
        print('Failed hours: ' + str(int(c/60)) + 'h / ' + str(int((100*c/len(P_grid))*10)/10) + "%")
    print()

    # eq = np.rint((P_core + P_unload - P_grid)).astype(int)
    # print(eq)
    print_load_graph(P_grid, reac, max_stored_energy, Time, P_core, P_load, P_unload, stored_energy, 0, len(P_grid)-1)
    print_flows(Time, primary_flow, load_flow, unload_flow, 0, len(P_grid)-1) 

def min_storage_time(PN_reac, profile, couverture): # Computes minimum storage capacity in hours to mach the grid
    c = 0
    eq = False
    couv = 0
    while couv < couverture: 
        c+=1
        (reac, hot_tank, cold_tank, max_stored_energy, P_unload_max)  = system_initialize(PN_reac, c)
        P_grid = np.array(profile)*(system_max_power/eta)/100
        (Time, P_core, P_load, P_unload, stored_energy) = load_following(P_grid, reac, max_stored_energy, P_unload_max)
        eq,couv = grid_equilibrium(P_grid, P_core, P_unload)
        couv = 100 - int((100*couv/len(P_grid))*10)/10
        print(str(c) + 'h')

    kp = load_factor(P_core, reac.P_max)
    kp_without = load_factor(P_grid*eta, system_max_power)
    m_salt = int(hot_tank.V_max*nitrate_salt.rho(T_stock_hot)/1000)

    return c, kp, kp_without, m_salt

def storage_time_study(profile, sys_max_pow):
    capacity = []
    nominal_power = []
    kp = []
    kp_without = []
    salt_mass = []

    for P in range(50,int(sys_max_pow),25):
        print('Studying ' + str(P) + 'MW reactor...')
        (c,k,k_w, mass) = min_storage_time(P, profile,couverture)
        capacity.append(c)
        kp.append(k)
        kp_without.append(k_w)
        salt_mass.append(mass)
        nominal_power.append(P)

    print('')
    print('Done !')
    print('Displaying results...')

    fig = plt.figure()
    gs = gridspec.GridSpec(2,2)

    ax1=fig.add_subplot(gs[0,0])
    ax1.plot(nominal_power,capacity, 'k.', label = 'Storage capacity in hours')
    ax1.set_title('Minimum storage capacity in hours to match grid requirements')
    plt.ylabel('Storage capacity (h)')
    plt.xlabel('Reactor nominal power')
    ax1.set_xticks(np.arange(0, max(nominal_power), 50))
    ax1.set_yticks(np.arange(0, max(capacity), 5))
    ax1.grid(which='major', color='#DDDDDD', linewidth=1)
    ax1.grid()
    ax1.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax1.minorticks_on()
    ax1.grid()


    ax2=fig.add_subplot(gs[0,1])
    ax2.plot(nominal_power,salt_mass, 'k.', label = 'Storage capacity in salt mass')
    ax2.set_title('Minimum storage capacity in salt mass to match grid requirements')
    ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,}'))
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ax2.set_xticks(np.arange(0, max(nominal_power), 50))
    ax2.set_yticks(np.arange(0, max(salt_mass), 50000))
    plt.ylabel('Salt mass (t)')
    plt.xlabel('Reactor nominal power')
    ax2.grid(which='major', color='#DDDDDD', linewidth=1)
    ax2.grid()
    ax2.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax2.minorticks_on()
    ax2.grid()

    ax3=fig.add_subplot(gs[1,:])
    ax3.plot(nominal_power, kp, 'k.', label = 'Capacity factor at minimal storage requirements')
    ax3.plot(nominal_power, kp_without, 'r.', label = 'Capacity factor of equivalent reactor without storages')
    ax3.set_title('Capacity factor at minimal storage requirement')
    ax3.yaxis.set_major_formatter(StrMethodFormatter('{x:,}'))
    ax3.set_xticks(np.arange(0, max(nominal_power), 50))
    ax3.set_yticks(np.arange(0, 105, 5))
    plt.ylabel('Capacity factor (%)')
    plt.xlabel('Reactor nominal power')
    ax3.grid(which='major', color='#DDDDDD', linewidth=1)
    ax3.grid()
    ax3.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax3.minorticks_on()
    ax3.grid()
    plt.show()

def interface():

    if season == 'Winter':
        if rate == 50:
            profile = profil_50EnR_winter
        elif rate == 80:
            profile = profil_80EnR_winter
        else:
            profile = profil_90EnR_winter
    elif season == 'Summer':
        if rate == 50:
            profile = profil_90EnR_sum
        elif rate == 80:
            profile = profil_90EnR_sum
        else:
            profile = profil_90EnR_sum
    elif season == 'Winter week':
        if rate == 50:
            profile = profil_50EnR_sem_winter
        elif rate == 80:
            profile = profil_80EnR_sem_winter
        else:
            profile = profil_90EnR_sem_winter
    else:
        if rate == 50:
            profile = profil_50EnR_sem_sum
        elif rate == 80:
            profile = profil_80EnR_sem_sum
        else:
            profile = profil_90EnR_sem_sum

    if study == 'Single system':
        run(reactor_power, storage_duration, profile)
    else:
        storage_time_study(profile, system_max_power)
        print("Parametric")

interface()

# run(150,12,profil_80EnR_winter)
# storage_time_study(profil_80EnR_sem_sum)

# print(min_storage_time(200, profil_80EnR_sem_winter))

# run(200, 8, profil_80EnR_sem_winter)