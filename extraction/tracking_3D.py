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
    

#fonction pour numeroter les fichiers
def numerote(n, l):
   s = str(n)
   while len(s) < l:
       s = '0' + s
   return s   
    

os.system("mkdir area")



def retrouve_grain(x,y,z,t):
    
    os.system("mkdir area")
    command("selectcomp images_3D/image_3D_t"+numerote(t,2)+".pgm "+str(x)+" "+str(y)+" "+str(z)+" tracking_3D/track_t_"+str(t)+"_"+str(x)+"_"+str(y)+"_"+str(z)+".pgm")
    command("area tracking_3D/track_t_"+str(t)+"_"+str(x)+"_"+str(y)+"_"+str(z)+".pgm  area/area_test.list")
    