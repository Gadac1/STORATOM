# Thermal Storage for Sodium-Cooled Fast Neutron Reactors
Python software simulating the use of a thermal storage system to complement a sodium-cooled fast neutron nuclear reactor.

The objective of STORATOM is to be a tool for studying and sizing a molten salt storage system in complement of a complement a sodium-cooled fast neutron nuclear reactor. 

The purpose of this software is to determine the main parameters governing such a system by taking as input an electricity production profile consistent with the situation on the French electricity network at the horizon 2050. It thus measures the impact that such a system would have on the modulation needs of the reactor itself. Indeed, a reactor that produces electricity in a stable manner is immediately more competitive and subject to less aging constraints on its systems.

The software allows two types of studies:

- Single system: Simulate a powerplant given a total power output, a reactor nomminal power and a storage duration over any of our given load profiles.
- Parametric: Find out what are the the most optimized system available in terms of capacity factor and storage size for a given load profile. A coverage parameter as a criteria of success for our powerplant. 100% means the entire load profile is satisfied by the production capabilities of our system. Beware, this might lead to a very high requirement of storage over an entire season ! Computations can take some time on seasonal profiles

Python 3.11 is used
