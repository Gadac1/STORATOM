import math as m

# All temps in °C
# All masses in kg
# All power in MWth
# All volumes in m3

class Reactor: 
    def __init__(self, P_max, P_grad, T_out, T_in):
        self.P_max = P_max
        self.P_grad = P_grad
        self.T_out = T_out
        self.T_in = T_in

class Fluid:
    def __init__(self, rho, cp, k):
        self.rho = rho
        self.cp = cp
        self.k = k

class Tank:
    def __init__(self, V_max, fluid, T_tank):
        self.V_max = V_max
        self.fluid = fluid
        self.T_tank = T_tank


class Heat_exchanger:
    ###
    # All powers in MWth
    ###
    def __init__(self, P, T_hot_in, T_hot_out, T_cold_in, T_cold_out):
        self.P = P
        self.T_hot_in = T_hot_in
        self.T_hot_out = T_hot_out
        self.T_cold_in = T_cold_in
        self.T_cold_out = T_cold_out
    
    def LMTD(self):
        return ((self.T_hot_in - self.T_cold_out) - (self.T_hot_out - self.T_cold_in))/m.log((self.T_hot_in - self.T_cold_out)/(self.T_hot_out - self.T_cold_in))

    def UA(self):
        return self.P/self.LMTD()

def MW_to_W(P):
    return P*1e6

def Joules_to_MWh(E):
    return E/3.6e9
# natrium = reactor(345,112,0.05)
# print(natrium.P)
# natrium.P=natrium.P-natrium.P_grad*natrium.P_max
# print(natrium.P)

# nitrate_salt = fluid(2090,1443,0.443)
# nitrate_salt_v2 = fluid(lambda T: 2090-0.636*T,1443,0.443)
# hot_tank = tank(3015,3015,nitrate_salt, 500)
# print(hot_tank.fluid_mass())

