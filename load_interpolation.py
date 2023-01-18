import pandas as pd

def interpolation(profil) :

    df = pd.read_excel(profil) # can also index sheet by name or fetch all sheets
    print(df)
    donnees = df['Puissance'].tolist()

    n = len(donnees)
    donnees_interpo = []
    pos_interpo = 0

    for i in range(n-1):
        donnees_interpo.append(donnees[i])
        coeff = (donnees[i+1] - donnees[i])/30
        for j in range(29):
            nouv_point = donnees_interpo[pos_interpo]+coeff
            donnees_interpo.append(nouv_point)
            pos_interpo += 1
    donnees_interpo.append(donnees[n-1])
    
    return donnees_interpo

profil_90EnR_pic3 = interpolation('DonnéesPDI-90%EnR-Pic3.xlsx')
profil_80EnR_pic3 = interpolation('DonnéesPDI-80%EnR-Pic3.xlsx')
profil_50EnR_pic3 = interpolation('DonnéesPDI-50%EnR-Pic3.xlsx')
