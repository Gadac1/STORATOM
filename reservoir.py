import matplotlib.pyplot as plt
import numpy as np

#A terme le reservoir sera thermostaté, il faudra donc calculer a la place la puissance requise pour cela en fonction du temps.

#Q_in is the charging load profile from the reactor in steps of one minute
#ΔT is the change in temperature of the tank over time
#Δt is the time interval over which the temperature is being measured
#Q_in_values is the array of rates at which heat is being added to the tank through the heat exchanger. Each value corresponds to a minute.
#Q_out is the rate at which heat is being lost from the tank through its walls
#m is the mass of the substance inside the tank
#c is the specific heat capacity of the substance inside the tank.

def plot_tank_temperature(T_initial, m, c, h, A_tank, T_ambient, Q_in_values):
  # Initialize variables
  T_tank = T_initial
  time_steps = len(Q_in_values)
  time = np.linspace(0, time_steps, time_steps)  
  temperatures = np.empty(time_steps)
  P_out = np.zeros(time_steps)

  # Calculate temperature of tank at each time step
  for i in range(time_steps):
    Q_in = Q_in_values[i]
    Q_out = h * A_tank * (T_tank - T_ambient)
    P_out[i] = Q_out
    delta_T = (Q_in - Q_out) * 60 / (m * c)
    T_tank += delta_T
    temperatures[i] = T_tank
  
  # Plot results
  plt.plot(time/1440, temperatures)
  plt.xlabel("Time (days)")
  plt.ylabel("Temperature (°C)")
  plt.show()

  plt.plot(time/1440, P_out/1e6)
  plt.xlabel("Time (days)")
  plt.ylabel("P (MW)")
  plt.show()

# Test
Q_in = np.zeros(144000)
plot_tank_temperature(550,6300e6,1443,400,1000,20,Q_in)

