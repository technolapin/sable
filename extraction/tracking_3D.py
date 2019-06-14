#suivi de grains

#importations
import pickle
import os
import numpy as np
#donnes
n_tempo = 16 # nb de temps
n_coupes_xy = 250 # dimensions des colones en nombres de coupes
n_coupes_xz = 80
n_coupes_yz = 80

seuil = 170 #pour les images en noir et blanc





#appel de fc de pink
def command(cmd):
    os.system("../pink/linux/bin/"+cmd)
    

#pour recuperer les elements d un .list
def parse_list(file_name):
    f = open(file_name, "r")
    line = f.readline()
    mode = line[0]
    n_els = int(line[2:][:-1])
    liste = []
    for i in range(n_els):
        liste.append([])
        line = f.readline()[:-1];
        for s in line.split(" "):
            liste[i].append(int(s))
    f.close()
    return liste

def export_list(liste, file_name):
    os.system("rm "+file_name)
    f = open(file_name, "w")
    f.write("_ "+str(len(liste))+"\n")
    for elements in liste:
        f.write(" ".join(str(el) for el in elements)+"\n")
    f.close()


#fonction pour numeroter les fichiers
def numerote(n, l):
   s = str(n)
   while len(s) < l:
       s = '0' + s
   return s   
    
formes=[]





#Enleve les formes qui ne sont pas des grains de la liste des barry

for t in range(0, n_tempo):
    
    padding_temporel = numerote(t, 2) # pour pas trop recalculer

    #enleve de la liste les grains de vol<100
    liste= parse_list("../extraction/bary_3D/liste/bary_list_t"+padding_temporel+".list")
    volume_min=100
    g=0
    while g< len(liste):
        if (liste[g][3]<volume_min):
            del(liste[g])
        g += 1
        
    formes.append(liste)
        

grains = []

"""
[
grain1 [vol, [[x0, y0, z0], [x1, y1, z1]]]
]

"""

def dist2(g1, g2):
    return pow(g1[0]-g2[0], 2) + pow(g1[1]-g2[1], 2) + pow(g1[2]-g2[2], 2)



seuil_volume = 1000

for grain in formes[0]:
    grains.append(
            [grain[3],
             [grain[:3]]
            ])
    for t in range(1, n_tempo):
        gr_prec = grains[len(grains)-1][1][t-1]
        dist_min = dist2(gr_prec, formes[t][0])
        plus_proche = formes[t][0]        

        for suivant in formes[t]:
            d2 = dist2(gr_prec, suivant)
            if (d2 < dist_min and abs(gr_prec[0]-suivant[0]) < seuil_volume):
                dist_min = d2
                plus_proche = suivant
        grains[len(grains)-1][1].append(plus_proche[:3])
#print(grains)


resultats = []
for grain in grains:
    x = []
    y = []
    z = []
    for coords in grain[1]:
        x.append(coords[0])
        y.append(coords[1])
        z.append(coords[2])
    resultats.append([x, y, z])
    
np.save("../extraction/tracking_3D/resultats.npy", resultats)
"""
for meh in resultats:
    for yolo in meh:
        print(yolo)
    print("\n\n\n\n")
"""

def retrouve_grain(x,y,z,t):
    
    padding_temporel = numerote(t, 2)
    
    #retrouve le grain et sa coupe
    command ("selectcomp ../extraction/images_3D/image_3D_superpose_inv_t"+padding_temporel+".pgm 26 "+str(x)+" "+str(y)+" "+str(z)+
             " ../extraction/tracking_3D/track_t_"+padding_temporel+"_"+str(x)+"_"+str(y)+"_"+str(z)+".pgm")    
    
    #barycentre
    command("3dlabel ../extraction/tracking_3D/track_t_"+padding_temporel+"_"+str(x)+"_"+str(y)+"_"+str(z)+
            ".pgm ../extraction/labels_3D/label_t_"+padding_temporel+"_"+str(x)+str(y)+str(z)+".pgm")
    
    command("barycentrelab ../extraction/labels_3D/label_t_"+padding_temporel+"_"+str(x)+str(y)+str(z)+
            ".pgm ../extraction/bary_3D/bary_3D_t"+padding_temporel+"_"+str(x)+str(y)+str(z)+".pgm")
    
    command("pgm2list ../extraction/bary_3D/bary_3D_t"+padding_temporel+"_"+str(x)+str(y)+str(z)+
            ".pgm B ../extraction/bary_3D/liste/bary_list_t"+padding_temporel+"_"+str(x)+str(y)+str(z)+".list")
    
    bary= parse_list("../extraction/bary_3D/liste/bary_list_t"+padding_temporel+"_"+str(x)+str(y)+str(z)+".list")
    print(bary)
    xb=bary[0][0]
    yb=bary[0][1]
    zb=bary[0][2]
    for grain in range(len(resultats)):
        if(resultats[grain][0][t]==xb and resultats[grain][1][t]==yb and resultats[grain][2][t]==zb):
            return resultats[grain]
#    
    
    
    
    
    
    
    
    
    
    
    
NB_IMGS = 4000
INTERVALLE_XY = 250
INTERVALLE_XZ = 80
INTERVALLE_YZ = 80
URL_PGM = "../extraction/coupes_3D/"
URL_VTK = "../extraction/vtks/"
URL_GRAPHIQUE_3D = "../extraction/tracking_3D/resultats.npy"
"""
EXPORTATION
"""
# Bade de Données
bdd = {} 
bdd["NB_IMGS"] = NB_IMGS
bdd["INTERVALLE_XY"] = INTERVALLE_XY
bdd["INTERVALLE_XZ"] = INTERVALLE_XZ
bdd["INTERVALLE_YZ"] = INTERVALLE_YZ
bdd["URL_PGM"] = URL_PGM
bdd["URL_VTK"] = URL_VTK
bdd["URL_GRAPHIQUE_3D" ] = URL_GRAPHIQUE_3D

# Its important to use binary mode
fichierBdd = open('woopwoop', 'ab')

# source, destination
pickle.dump(bdd, fichierBdd)                 
fichierBdd.close()
