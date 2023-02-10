import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rd

# Données pour construire les profils de consommation selon jour de la semaine, saison et aléas 
# Jalons été
jalons_sem_été_norm = [60000,55000,90000,75000,82000]
jalons_we_été_norm = [55000,55000,85000,70000,77000]
jalons_sem_été_max = [70000,65000,110000,90000,100000]
jalons_we_été_max = [65000,62000,105000,85000,95000]
jalons_sem_été_min = [55000,50000,83000,70000,75000]
jalons_we_été_min = [50000,45000,80000,65000,70000]

# Jalons hiver
jalons_sem_hiv_norm = [80000,80000,100000,87000,90000]
jalons_we_hiv_norm = [75000,75000,95000,82000,85000]
jalons_sem_hiv_max = [95000,95000,125000,105000,110000]
jalons_we_hiv_max = [90000,90000,120000,100000,105000]
jalons_sem_hiv_min = [70000,70000,90000,75000,80000]
jalons_we_hiv_min= [65000,65000,85000,70000,75000]

# Jalons printemps/automne
jalons_sem_print_norm = [70000,65000,80000,70000,72000]
jalons_we_print_norm = [65000,60000,75000,65000,67000]
jalons_sem_print_max = [75000,70000,90000,85000,87000]
jalons_we_print_max = [70000,65000,85000,80000,82000]
jalons_sem_print_min = [60000,55000,75000,65000,67000]
jalons_we_print_min = [55000,50000,70000,60000,62000]


def jour(pas, jalons, suivant) :
    periode = 0 #variable période, dépend hx successifs et pas
    coeff = 0 #variable coefficient linéaire, dépend hx successifs et periode
    var = 0 #variable variabilité des valeurs consommation
    
    # Introduction de variabilité sur les jalons
    for i in range (len(jalons)):
        var = rd.gauss(0,1.55)*1E-2
        jalons[i] = int(jalons[i]*(1+var))
        
    h1 = jalons[0]
    h2 = jalons[1]
    h3 = jalons[2]
    h4 = jalons[3]
    h5 = jalons[4]
    
    var = rd.gauss(0,1.55)*1E-2
    suiv = int(suivant[0]*(1+var))
    
    # liste valeurs consommation d'une journée initialisée avec conso à 00:00
    jour = [h1] 
    
    # ajout valeurs entre 00:30-06:00
    periode =  int(5.5/pas)
    coeff = int((h2-h1)/periode)
    for i in range(periode):
        nouv_val = coeff*(i+1) + h1
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
    
    # ajout valeurs entre 06:30-12:00
    periode =  int(5.5/pas)
    coeff = int((h3-h2)/periode)
    for i in range(periode):
        nouv_val = coeff*(i+1) + h2
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
    
    # ajout valeurs entre 12:30-13:30
    periode =  int(1/pas)
    for i in range(periode):
        nouv_val = h3
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
        
    # ajout valeurs entre 14:00-18:00
    periode =  int(4/pas)
    coeff = int((h4-h3)/periode)
    for i in range(periode):
        nouv_val = coeff*(i+1) + h3
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
    
    # ajout valeurs entre 18:30-19:30
    periode =  int(1/pas)
    coeff = int((h5-h4)/periode)
    for i in range(1,periode):
        nouv_val = coeff*(i+1) + h4
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
        
    # ajout valeurs entre 20:00-23:30
    periode =  int(3.5/pas)
    coeff = int((suiv-h5)/periode)
    for i in range(periode):
        nouv_val = coeff*(i+1) + h5
        var = rd.gauss(0,1.55)*1E-2
        nouv_val = int(nouv_val*(1+var))
        jour.append(nouv_val)
        
    return jour

test = jour(0.5, jalons_sem_été_norm, jalons_sem_été_norm)
print("Longueur jour est", len(test))
plt.plot(test)
plt.show()


def semaine(pas,jalons_semaine,jalons_weekend, jalons_sem_suivante):
    semaine = [] #liste valeurs consommation d'une semaine
    
    lundi = jour(pas,jalons_semaine,jalons_semaine) #journée lundi consommation en semaine
    mardi = jour(pas,jalons_semaine,jalons_semaine) #journée mardi consommation en semaine
    mercredi = jour(pas,jalons_semaine,jalons_semaine) #journée mercredi consommation en semaine
    jeudi = jour(pas,jalons_semaine,jalons_semaine) #journée jeudi consommation en semaine
    vendredi = jour(pas,jalons_semaine,jalons_weekend) #journée vendredi consommation en semaine
    samedi = jour(pas,jalons_weekend, jalons_weekend) #journée samedi consommation en week-end
    dimanche = jour(pas,jalons_weekend,jalons_sem_suivante) #journée samedi consommation en week-end
    
    # Ajout de lundi
    for x in lundi :
        semaine.append(x)
    
    # Ajout de mardi
    for x in mardi :
        semaine.append(x)
    
    # Ajout de mercredi
    for x in mercredi :
        semaine.append(x)
    
    # Ajout de jeudi
    for x in jeudi :
        semaine.append(x)
    
    # Ajout de vendredi
    for x in vendredi :
        semaine.append(x)
        
    # Ajout de samedi 
    for x in samedi :
        semaine.append(x)
        
    # Ajout de dimanche 
    for x in dimanche :
        semaine.append(x)
        
    return semaine

test2 = semaine(0.5, jalons_sem_été_norm, jalons_we_été_norm, jalons_sem_été_norm)
print("longueur semaine est", len(test2))
plt.plot(test2)
plt.show()

# Nombres semaines sur une saison
# Comme une saison a 89-93 jours, on considérera qu'une saison fait 13 semaines
nbsem_norm = 9 # Nombre semaine consommation normale (80% cas)
nbsem_max = 2 # Nombre semaine consommation maximale (10% cas)
nbsem_min = 2 # Nombre semaine consommation minimale (10% cas)

def saison(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_max, jalons_we_max,jalons_sem_min, jalons_we_min, jalons_sem_suiv) :
    saison = []
        
    # Ajout de 3 semaines consommation normale
    semaine_norm1 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_norm)
    semaine_norm2 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_norm)
    semaine_norm3 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_min)
    
    for x in semaine_norm1 :
        saison.append(x)   
    
    for x in semaine_norm2 :
        saison.append(x)   
    
    for x in semaine_norm3 :
        saison.append(x)   
    
    # Ajout de 1 semaine consommation minimale
    semaine_min = semaine(pas, jalons_sem_min, jalons_we_min, jalons_sem_norm)
    for x in semaine_min :
        saison.append(x)
            
    # Ajout de 2 semaines consommation normale
    semaine_norm4 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_norm)
    semaine_norm5 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_max)
    
    for x in semaine_norm4 :
        saison.append(x)
        
    for x in semaine_norm5 :
        saison.append(x)
    
    # Ajout de 2 semaines consommation maximale
    semaine_max = semaine(pas, jalons_sem_max, jalons_we_max, jalons_sem_max)
    semaine_max2 = semaine(pas, jalons_sem_max, jalons_we_max, jalons_sem_norm)
    
    for x in semaine_max :
            saison.append(x)   
               
    for x in semaine_max2 :
            saison.append(x)    
            
    # Ajout de 1 semaines consommation normale
    semaine_norm6 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_min)
    
    for x in semaine_norm6 :
        saison.append(x)
    
    # Ajout de 1 semaines consommation minimale
    semaine_min2 = semaine(pas, jalons_sem_min, jalons_we_min, jalons_sem_norm)

    for x in semaine_min2 :
        saison.append(x)
    
    # Ajout de 3 semaines consommation normale
    semaine_norm7 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_norm)
    semaine_norm8 = semaine(pas, jalons_sem_norm, jalons_we_norm, jalons_sem_norm)   
    semaine_norm_suiv = semaine(pas, jalons_sem_norm, jalons_we_norm,jalons_sem_suiv)
    
    for x in semaine_norm7 :
        saison.append(x)
        
    for x in semaine_norm8 :
        saison.append(x)
        
    for x in semaine_norm_suiv :
        saison.append(x)
            
    return saison

# Visualisation des profils saisonniers

hiver = saison(0.5, jalons_sem_hiv_norm, jalons_we_hiv_norm,jalons_sem_hiv_max, jalons_we_hiv_max,jalons_sem_hiv_min, jalons_we_hiv_min, jalons_sem_print_norm)
print("longuer hiver est", len(hiver))
été = saison(0.5, jalons_sem_été_norm, jalons_we_été_norm, jalons_sem_été_max, jalons_we_été_max, jalons_sem_été_min, jalons_we_été_min, jalons_sem_print_norm)
printemps = saison(0.5, jalons_sem_print_norm, jalons_we_print_norm, jalons_sem_print_max, jalons_we_print_max, jalons_sem_print_min, jalons_we_print_min, jalons_sem_été_norm)
automne = saison(0.5, jalons_sem_print_norm, jalons_we_print_norm, jalons_sem_print_max, jalons_we_print_max, jalons_sem_print_min, jalons_we_print_min, jalons_sem_hiv_norm)

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

np.savetxt("V2 Profils consommations hiver.csv", val_hiver, delimiter =", ", fmt ='% s')
np.savetxt("V2 Profils consommations été.csv", val_été, delimiter =", ", fmt ='% s')
np.savetxt("V2 Profils consommations printemps.csv", val_printemps, delimiter =", ", fmt ='% s')
np.savetxt("V2 Profils consommations automne.csv", val_automne, delimiter =", ", fmt ='% s')
