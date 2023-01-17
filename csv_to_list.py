import pandas as pd

df = pd.read_excel('Profils/profil_50_pic1.xlsx', sheet_name='Feuil1') # can also index sheet by name or fetch all sheets
print(df.info())
enri_50_pic1 = df[0].tolist()

df = pd.read_excel('Profils/profil_80_pic1.xlsx', sheet_name='Feuil1') # can also index sheet by name or fetch all sheets
print(df.info())
enri_80_pic1 = df[0].tolist()
