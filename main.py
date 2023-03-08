from solver import *
from load_interpolation import *
from class_definition import *
import numpy as np
import matplotlib.pyplot as plt    
from matplotlib.ticker import StrMethodFormatter
import math

def compute_flows(P_core, P_load, P_unload, stored_energy):

    primary_flow = MW_to_W(P_core) / (sodium.cp((reac_T_out + reac_T_in)/2) * (reac_T_out - reac_T_in))
    load_flow = MW_to_W(P_core) / (nitrate_salt.cp((T_stock_hot + T_stock_cold)/2) * (T_stock_hot - T_stock_cold))
    unload_flow = MW_to_W(P_unload) / (nitrate_salt.cp((T_stock_hot + T_stock_cold)/2) * (T_stock_hot - T_stock_cold))
    

    return(primary_flow, load_flow, unload_flow)

def Nu_h_Gnielinski(fluid, flow, Di, f, T):

    velocity = flow / (fluid.rho(T) * (np.pi/4)*Di**2)
    Re = velocity*Di*fluid.rho(T)/fluid.mu(T)
    Pr = fluid.cp(T)*fluid.mu(T)/fluid.k(T)

    Nu = (f/8)*(Re - 1000)*Pr/(1 + 12.7*m.sqrt(f/8)*(Pr**(2/3) - 1))
    h = Nu*fluid.k(T) / Di

    return (Pr, Re,Nu,h)

def Nu_h_Cheng_Tak(fluid, flow, Di, n, T):

    velocity = (flow/n) / (fluid.rho(T) * (np.pi/4)*Di**2)
    Re = velocity*Di*fluid.rho(T)/fluid.mu(T)
    Pr = fluid.cp(T)*fluid.mu(T)/fluid.k(T)

    Pe = Pr * Re

    Nu = 3.6 + 0.018 * Pe**(0.8)
    h = Nu*fluid.k(T) / Di

    return (velocity, Pr, Re, Pe, Nu, h)

def print_load_graph(P_grid, reac, max_stored_energy, Time, P_core, P_load, P_unload, stored_energy, x1, x2):

    range = (x1,x2)
    fig = plt.figure()
    gs = gridspec.GridSpec(2,2)

    ax1=fig.add_subplot(gs[0,0])
    ax1.plot(Time[range[0]:range[1]]/1440, Joules_to_MWh(stored_energy[range[0]:range[1]]),'orange', linewidth='3')
    ax1.set_title("Stored energy")
    ax1.set_xlabel("Time (Days)")
    ax1.set_ylabel("Stored energy (MWh)")
    ax1.set_ylim(-0.05*max(Joules_to_MWh(stored_energy)), 1.05*Joules_to_MWh(max_stored_energy)) 
    ax1.grid(which='major', color='#DDDDDD', linewidth=1)
    ax1.grid()
    ax1.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax1.minorticks_on()
    ax1.grid()


    ax2=fig.add_subplot(gs[1,:])
    ax2.plot(Time[range[0]:range[1]]/1440, (P_core[range[0]:range[1]] + P_unload[range[0]:range[1]])*eta, 'r', label = "Total output power", linewidth='3')
    ax2.plot(Time[range[0]:range[1]]/1440, P_core[range[0]:range[1]]*eta, label = "Reactor power level", linewidth='3')
    ax2.plot(Time[range[0]:range[1]]/1440, P_grid[range[0]:range[1]]*eta, 'y--', label = "Grid electrical load", linewidth='3')
    ax2.set_title("Load following of reactor and storage system")
    ax2.set_xlabel("Time (Days)")
    ax2.set_ylabel("Power (MW)")
    ax2.legend(loc='best')
    ax2.set_ylim(-20,max(P_grid)*eta*1.05)
    ax2.grid(which='major', color='#DDDDDD', linewidth=1)
    ax2.grid()
    ax2.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax2.minorticks_on()
    ax2.grid()

    ax3=fig.add_subplot(gs[0,1])
    ax3.plot(Time[range[0]:range[1]]/1440, (P_load[range[0]:range[1]] - P_unload[range[0]:range[1]])*eta,'r', linewidth='3')
    ax3.set_xlabel("Time (h)")
    ax3.set_ylabel("Power (MW)")
    ax3.set_title("Storage system input load")
    ax3.set_ylim(-(system_max_power - reac.P_max*eta),reac.P_max*1.05*eta)
    ax3.grid(which='major', color='#DDDDDD', linewidth=1)
    ax3.grid()
    ax3.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax3.minorticks_on()
    ax3.grid()
    plt.show()

def print_flows(Time, primary_flow, load_flow, unload_flow, x1, x2):

    range = (x1,x2)
    plt.plot(Time[range[0]:range[1]]/1440, primary_flow[range[0]:range[1]], 'r', label = "Primary flow", linewidth='3')
    plt.plot(Time[range[0]:range[1]]/1440, load_flow[range[0]:range[1]], label = "Load loop flow", linewidth='3')
    plt.plot(Time[range[0]:range[1]]/1440, unload_flow[range[0]:range[1]], 'y--', label = "Unload loop flow", linewidth='3')
    plt.title("Computed flows in each fluid loops")
    plt.xlabel("Time (Days)")
    plt.ylabel("Mass flow rate (kg/s)")
    plt.legend(loc='best')
    plt.ylim(-20,max(max(primary_flow), max(load_flow), max(unload_flow))*1.05)
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid()
    plt.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    plt.minorticks_on()
    plt.grid()

    plt.show()

def load_factor(P_core, max_pow):
    energy_reactor = 0
    for p in P_core:
        energy_reactor += p*dt
    return int(100*(energy_reactor/((max_pow)*len(P_core)*dt)))

def grid_equilibrium(P_grid, P_core, P_unload):
    eq = np.rint((P_core[:-1] + P_unload[:-1] - P_grid[:-1])).astype(int)
    eq_boolean = True
    E_missed = 0
    c = 0
    for i in eq:
        if i<0:
            c+=1
            eq_boolean = False 
            # E_missed += (P_grid[i]-P_core[i]) * eta * dt * 1e6
    return eq_boolean,c, E_missed


def run(PN_reac, storage_time, profile): #Simple run function for single storage experiment

    (reac, hot_tank, cold_tank, max_stored_energy, P_unload_max)  = system_initialize(PN_reac, storage_time)
    P_grid = np.array(profile)*(system_max_power/eta)/100
    (Time, P_core, P_load, P_unload, stored_energy) = load_following(P_grid, reac, max_stored_energy, P_unload_max)
    (primary_flow, load_flow, unload_flow) = compute_flows(P_core, P_load, P_unload, stored_energy)
    
    print()
    print('Case study :')
    print('     Profile: ' + season + ", " + str(rate) + "% VRE penetration rate")
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
    eq, c, E_missed = grid_equilibrium(P_grid, P_core, P_unload)
    print('     Consumption-Production equilibrium: ' + str(eq))
    if eq == False:
        print('     Failed hours: ' + str(int(c/60)) + 'h / ' + str(int((100*c/len(P_grid))*10)/10) + "%")
        print('     Missed energy production: ' + str(E_missed) + " MWh")

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
        eq,couv,E_missed = grid_equilibrium(P_grid, P_core, P_unload)
        couv = 100 - (100*couv/len(P_grid))
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

    for P in range(25,int(sys_max_pow),25):
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
    ax2.set_yticks(np.arange(0, max(salt_mass), int(10**(math.ceil(math.log10(max(salt_mass))))/20)))
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
    ax3.set_xticks(np.arange(0, max(nominal_power), 25))
    ax3.set_yticks(np.arange(0, 105, 5))
    plt.ylabel('Capacity factor (%)')
    plt.xlabel('Reactor nominal power')
    ax3.grid(which='major', color='#DDDDDD', linewidth=1)
    ax3.grid()
    ax3.grid(which='minor', color='#EEEEEE', linestyle='--', linewidth=0.75)
    ax3.minorticks_on()
    ax3.grid()
    ax3.legend(loc='best')
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