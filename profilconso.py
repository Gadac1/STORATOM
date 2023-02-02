import matplotlib.pyplot as plt
import numpy as np
import csv

# Données pour construire les profils de consommation selon jour de la semaine, saison et aléas 
# Jalons été
jalons_sem_été_norm = [60000,55000,90000,75000,77000]
jalons_we_été_norm = [60000,50000,85000,70000,72000]
jalons_sem_été_max = [60000,65000,110000,90000,92000]
jalons_we_été_max = [60000,62000,105000,85000,87000]
jalons_sem_été_min = [60000,50000,83000,70000,72000]
jalons_we_été_min = [60000,45000,80000,65000,67000]

# Jalons hiver
jalons_sem_hiv_norm = [80000,80000,100000,87000,90000]
jalons_we_hiv_norm = [80000,75000,95000,82000,85000]
jalons_sem_hiv_max = [80000,95000,125000,105000,110000]
jalons_we_hiv_max = [80000,90000,120000,100000,105000]
jalons_sem_hiv_min = [80000,70000,90000,75000,80000]
jalons_we_hiv_min= [80000,65000,85000,70000,75000]

# Jalons printemps/automne
jalons_sem_print_norm = [70000,65000,80000,70000,72000]
jalons_we_print_norm = [70000,60000,75000,65000,67000]
jalons_sem_print_max = [70000,70000,90000,85000,87000]
jalons_we_print_max = [70000,65000,85000,80000,82000]
jalons_sem_print_min = [70000,55000,75000,65000,67000]
jalons_we_print_min = [70000,50000,70000,60000,62000]

# Nombres semaines sur une saison
# Comme une saison a 89-93 jours, on considérera qu'une saison fait 13 semaines
nbsem_norm = 9 # Nombre semaine consommation normale (80% cas)
nbsem_max = 2 # Nombre semaine consommation maximale (10% cas)
nbsem_min = 2 # Nombre semaine consommation minimale (10% cas)

def jour(pas, jalons) :
    jour = [] #liste valeurs consommation d'une journée
    periode = 0 #variable période, dépend hx successifs et pas
    coeff = 0 #variable coefficient linéaire, dépend hx successifs et periode
    h1 = jalons[0]
    h2 = jalons[1]
    h3 = jalons[2]
    h4 = jalons[3]
    h5 = jalons[4]
    
    # ajout valeurs entre 00:00-06:00
    periode =  int(6/pas)
    coeff = int((h2-h1)/periode)
    for i in range(periode):
        nouv_val = coeff*i + h1
        jour.append(nouv_val)
    
    # ajout valeurs entre 06:00-12:00
    periode =  int(6/pas)
    coeff = int((h3-h2)/periode)
    for i in range(periode):
        nouv_val = coeff*i + h2
        jour.append(nouv_val)
    
    # ajout valeurs entre 12:00-14:00
    periode =  int(2/pas)
    for i in range(periode):
        jour.append(h3)
        
    # ajout valeurs entre 14:00-18:00
    periode =  int(4/pas)
    coeff = int((h4-h3)/periode)
    for i in range(periode):
        nouv_val = coeff*i + h3
        jour.append(nouv_val)
    
    # ajout valeurs entre 18:00-19:30
    periode =  int(1.5/pas)
    coeff = int((h5-h4)/periode)
    for i in range(periode):
        nouv_val = coeff*i + h4
        jour.append(nouv_val)
        
    # ajout valeurs entre 19:30-23:30
    periode =  int(4/pas)
    coeff = int((h1-h5)/periode)
    for i in range(periode):
        nouv_val = coeff*i + h5
        jour.append(nouv_val)
            
    return jour

def semaine(pas,jalons_semaine,jalons_weekend):
    semaine = [] #liste valeurs consommation d'une semaine
    
    jour_semaine = jour(pas,jalons_semaine) #journée consommation en semaine, 
    jour_weekend = jour(pas,jalons_weekend) #journée consommation en week-end
    
    # Ajout des 5 jours de semaine
    for i in range(5):
        for x in jour_semaine:
            semaine.append(x)
    
    # Ajout des 2 jours du week-end
    for i in range(2):
        for x in jour_weekend:
            semaine.append(x)
    
    return semaine

def saison(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_max, jalons_we_max,jalons_sem_min, jalons_we_min) :
    saison = []
    
    semaine_norm = semaine(pas, jalons_sem_norm, jalons_we_norm)
    semaine_max = semaine(pas, jalons_sem_max, jalons_we_max)
    semaine_min = semaine(pas, jalons_sem_min, jalons_we_min)
    
    # Ajout de 3 semaines consommation normale
    for i in range(3):
        for x in semaine_norm :
            saison.append(x)
    
    # Ajout de 1 semaine consommation minimale
    for i in range(1) : 
        for x in semaine_min :
            saison.append(x)
            
    # Ajout de 2 semaines consommation normale
    for i in range(2):
        for x in semaine_norm :
            saison.append(x)
    
    # Ajout de 2 semaines consommation maximale
    for i in range(2):
        for x in semaine_max :
            saison.append(x)        
            
    # Ajout de 1 semaines consommation normale
    for i in range(1):
        for x in semaine_norm :
            saison.append(x)
    
    # Ajout de 1 semaines consommation minimale
    for i in range(1):
        for x in semaine_min :
            saison.append(x)
    
    # Ajout de 3 semaines consommation normale
    for i in range(3):
        for x in semaine_norm :
            saison.append(x)
            
    return saison

# Comparaison des cas de consommation pour chaque saison 
semaine_hiv_norm = semaine(0.5, jalons_sem_hiv_norm, jalons_we_hiv_norm)
semaine_hiv_max  = semaine(0.5, jalons_sem_hiv_max, jalons_we_hiv_max)
semaine_hiv_min  = semaine(0.5, jalons_sem_hiv_min, jalons_we_hiv_min)

semaine_été_norm = semaine(0.5, jalons_sem_été_norm, jalons_we_été_norm)
semaine_été_max  = semaine(0.5, jalons_sem_été_max, jalons_we_été_max)
semaine_été_min  = semaine(0.5, jalons_sem_été_min, jalons_we_été_min)

semaine_print_norm = semaine(0.5, jalons_sem_print_norm, jalons_we_print_norm)
semaine_print_max  = semaine(0.5, jalons_sem_print_max, jalons_we_print_max)
semaine_print_min  = semaine(0.5, jalons_sem_print_min, jalons_we_print_min)

plt.figure(1)
plt.subplot(221)
plt.plot(semaine_hiv_norm, 'r^', semaine_hiv_max, 'g^', semaine_hiv_min, 'b^')
plt.title('Hiver')

plt.subplot(222)
plt.plot(semaine_été_norm, 'r^', semaine_été_max, 'g^', semaine_été_min, 'b^')
plt.title('Ete')

plt.subplot(223)
plt.plot(semaine_print_norm, 'r^', semaine_print_max, 'g^', semaine_print_min, 'b^')
plt.title('Printemps/Automne')


# Visualisation des profils saisonniers
hiver = saison(0.5, jalons_sem_hiv_norm, jalons_we_hiv_norm,jalons_sem_hiv_max, jalons_we_hiv_max,jalons_sem_hiv_min, jalons_we_hiv_min)
été = saison(0.5, jalons_sem_été_norm, jalons_we_été_norm, jalons_sem_été_max, jalons_we_été_max, jalons_sem_été_min, jalons_we_été_min)
printemps = saison(0.5, jalons_sem_print_norm, jalons_we_print_norm, jalons_sem_print_max, jalons_we_print_max, jalons_sem_print_min, jalons_we_print_min)
automne = saison(0.5, jalons_sem_print_norm, jalons_we_print_norm, jalons_sem_print_max, jalons_we_print_max, jalons_sem_print_min, jalons_we_print_min)

plt.figure(2)
plt.subplot(221)
plt.plot(hiver)
plt.title('Hiver')

plt.subplot(222)
plt.plot(été)
plt.title('Ete')

plt.subplot(223)
plt.plot(printemps)
plt.title('Printemps')

plt.subplot(224)
plt.plot(automne)
plt.title('Automne')

plt.show()

# Conversion profils de consommation saisonnier en CSV
val_hiver = np.array(hiver)
val_été = np.array(été)
val_printemps = np.array(printemps)
val_automne = np.array(automne)

np.savetxt("Profils/DataPDI-90_EnR_hiver.csv", val_hiver, delimiter =", ", fmt ='% s')
np.savetxt("Profils/DataPDI-90_EnR_ete.csv", val_été, delimiter =", ", fmt ='% s')
# np.savetxt("Profils consommations printemps.csv", val_printemps, delimiter =", ", fmt ='% s')
# np.savetxt("Profils consommations automne.csv", val_automne, delimiter =", ", fmt ='% s')