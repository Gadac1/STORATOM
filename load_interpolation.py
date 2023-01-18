import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def interpolation(profil) :

    df = pd.read_excel(profil) # can also index sheet by name or fetch all sheets
    print(df)
    donnees = df['Puissance'].tolist()

    n = len(donnees)
    donnees_interpo = []
    for i in range(n-1):
        donnees_interpo.append(donnees[i])
        coeff = (donnees[i+1] - donnees[i])/30
        for j in range(29):
            donnees_interpo.append(donnees[i]+coeff*j)

    donnees_interpo.append(donnees[n-1])
    
    return donnees_interpo

df = pd.read_excel('Profils/profil_50_pic1.xlsx', sheet_name='Feuil1') # can also index sheet by name or fetch all sheets
enri_50_pic1 = df[0].tolist()

df = pd.read_excel('Profils/profil_80_pic1.xlsx', sheet_name='Feuil1') # can also index sheet by name or fetch all sheets
enri_80_pic1 = df[0].tolist()

df = pd.read_excel('Profils/profil_90_pic1.xlsx', sheet_name='Feuil1') # can also index sheet by name or fetch all sheets
enri_90_pic1 = df[0].tolist()

profil_90EnR_pic3 = interpolation('Profils/DonnéesPDI-90_EnR-Pic3.xlsx')
profil_80EnR_pic3 = interpolation('Profils/DonnéesPDI-80_EnR-Pic3.xlsx')
profil_50EnR_pic3 = interpolation('Profils/DonnéesPDI-50_EnR-Pic3.xlsx')


