import stat,os

'''f=os.popen(f'df -h /home/douaa|tr -s " " " " |tail -1|cut -d " " -f3')
for l in f.readlines():
            c=l[0:len(l)-1] 
print(c[len(c)-1])
print(10**6)'''
'''l={'K':1,'M':1000,'G':10**6,'T':10**9}
u='12,5G'
d='16,34975956T'
uu=u[len(u)-1] 
ud=d[len(d)-1] 
print(d[0:len(d)-1])
for k,v in l.items():
            if(uu==k):
                u=float(u[0:len(u)-1].replace(',','.'))* (int(v))
                u=('{:.2f}'.format(u))+'K'
            if(ud==k):
                d=float(d[0:len(d)-1].replace(',','.'))* (int(v))
                d=('{:.2f}'.format(d))+'K'
print(u)
print(d)'''
'''import matplotlib.pyplot as plt

# données pour le pie chart
labels = ['12,5G', '28T']
sizes = [28, 2000-28]

# créer le pie chart
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
#ax.axis('equal')

# afficher le pie chart dans une fenêtre
plt.show()'''

'''import matplotlib.pyplot as plt

# Obtenez les informations d'espace disque pour l'utilisateur courant
espace_utilise = os.statvfs(os.path.expanduser('/home/dev')).f_frsize * os.statvfs(os.path.expanduser('/home/dev')).f_blocks
espace_restant = os.statvfs(os.path.expanduser('/home/dev')).f_frsize * os.statvfs(os.path.expanduser('/home/dev')).f_bfree

# Convertir l'espace en gigaoctets
espace_utilise = round(espace_utilise / (1024**3), 2)
espace_restant = round(espace_restant / (1024**3), 2)

# Création d'une liste avec les deux valeurs
donnees = [espace_utilise, espace_restant]
print(donnees)
# Étiquettes pour le graphique
etiquettes = ['Espace utilisé', 'Espace restant']

# Couleurs pour chaque partie du graphique
couleurs = ['#FFA07A', '#ADD8E6']

# Création du graphique pie
plt.pie(donnees, labels=etiquettes, colors=couleurs, autopct='%1.1f%%')

# Ajout du titre
plt.title('Espace disque pour l\'utilisateur courant')

# Affichage du graphique
plt.show()'''