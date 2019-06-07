#suivi de grains

#importations
import os

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

#traitement pour chaque temps

for t in range(0, n_tempo):
    
    padding_temporel = numerote(t, 2) # pour pas trop recalculer

    #enleve de la liste les grains de vol<100
    liste= parse_list("bary_3D/liste/bary_list_t"+padding_temporel+".list")
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
        grains[len(grains)-1][1].append(suivant[:3])
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


from ../gui_unfiée/class_TabGraphique3D import TabGraphique3D


def retrouve_grain(x,y,z,t):
    
    os.system("mkdir area")
    command ("selectcomp images_3D/image_3D_superpose_inv_t"+numerote(t,2)+".pgm 26 "+str(x)+" "+str(y)+" "+str(z)+" tracking_3D/track_t_"+str(t)+"_"+str(x)+"_"+str(y)+"_"+str(z)+".pgm")    
   