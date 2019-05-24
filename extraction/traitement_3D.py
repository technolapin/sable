##3D traitement

#importations
import os


n_tempo = 16 #nb de temps
n_coupe = 250
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
    
os.system("rm -R images_3D")
os.system("rm -R images_2D_for_3D")
os.system("rm -R coupes_3D")
os.system("mkdir images_3D")
os.system("mkdir images_2D_for_3D")
os.system("mkdir coupes_3D")
os.system("mkdir coupes_3D/x_y")
os.system("mkdir coupes_3D/x_z")
os.system("mkdir coupes_3D/y_z")

#copie des images de test et renommage aux standard de la fc catpgm
for i in range(0, n_tempo*n_coupe):
    os.system("cp images/test-"+str(i)+".pgm images_2D_for_3D/image_2D_for_3D_"+numerote(i,4)+".pgm")


    
coupe=0
for i in range(0,n_tempo):
    print("image 3D numero "+str(i)+" en traitement")
    fin_coupe=coupe+n_coupe-1
    
    #generation de l image 3D a partir des 250 coupes
    ligne="catpgm images_2D_for_3D/image_2D_for_3D_ "+ str(coupe)+ " "+str(fin_coupe)+" [80 80 250] images_3D/image_3D_t"+numerote(i,2)+".pgm"
    command(ligne)
    
    #seuillage + nettoyage d impurtes
    command("seuil images_3D/image_3D_t"+numerote(i,2)+".pgm"" "+str(seuil)+" "+"images_3D/image_3D_s_t"+numerote(i,2)+".pgm")
    command("inverse images_3D/image_3D_s_t"+numerote(i,2)+".pgm images_3D/image_3D_s_inv_t"+numerote(i,2)+".pgm")
    
     # carte des distances, 180:18dist 3D (byte outpout)
    command("dist images_3D/image_3D_s_inv_t"+numerote(i,2)+".pgm 0 images_3D/image_3D_dist_proc_t"+numerote(i,2)+".pgm")
    command("long2byte images_3D/image_3D_dist_proc_t"+numerote(i,2)+".pgm 0 images_3D/image_3D_dist_t"+numerote(i,2)+".pgm")
    command("inverse images_3D/image_3D_dist_t"+numerote(i,2)+".pgm images_3D/image_3D_dist_inv_t"+numerote(i,2)+".pgm")
    
    # minimas
    command("minima images_3D/image_3D_dist_inv_t"+numerote(i,2)+".pgm 6 images_3D/image_3D_min_t"+numerote(i,2)+".pgm")

    #ligne de separation des eaux
    command("watershed images_3D/image_3D_dist_inv_t"+numerote(i,2)+".pgm images_3D/image_3D_min_t"+numerote(i,2)+".pgm 26 images_3D/image_3D_wat_t"+numerote(i,2)+".pgm")
    command("add images_3D/image_3D_s_inv_t"+numerote(i,2)+".pgm images_3D/image_3D_wat_t"+numerote(i,2)+".pgm images_3D/image_3D_superpose_t"+numerote(i,2)+".pgm")
    command("inverse images_3D/image_3D_superpose_t"+numerote(i,2)+".pgm images_3D/image_3D_superpose_inv_t"+numerote(i,2)+".pgm ")
    
    #extraction des coupes sur (x,y)
    os.system("mkdir coupes_3D/x_y/"+numerote(i,2))
    for u in range(0,n_coupe):
        command("extractplane images_3D/image_3D_t"+numerote(i,2)+".pgm u xy coupes_3D/x_y/"+numerote(i,2)+"/t_"+numerote(i,2)+"coupe_xy_"+numerote(u,4)+"pgm")
    
    
    #extraction des coupes sur (x,z)
    os.system("mkdir coupes_3D/x_z/"+numerote(i,2))
    for u in range(0,n_coupe):
        command("extractplane images_3D/image_3D_t"+numerote(i,2)+".pgm u xz coupes_3D/x_z/"+numerote(i,2)+"/t_"+numerote(i,2)+"coupe_xz_"+numerote(u,4)+"pgm")
    
    
    #extraction des coupes sur (y,z)
    os.system("mkdir coupes_3D/y_z/"+numerote(i,2))
    for u in range(0,n_coupe):
        command("extractplane images_3D/image_3D_t"+numerote(i,2)+".pgm u yz coupes_3D/y_z/"+numerote(i,2)+"/t_"+numerote(i,2)+"coupe_yz_"+numerote(u,4)+"pgm")
    
    coupe=coupe+250
    
    