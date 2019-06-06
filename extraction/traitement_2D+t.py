#2D+t

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



#gestion des repertoires
os.system("rm -R images_2D+t")
os.system("rm -R images_2D+t_visu")
os.system("rm -R images_process_2D+t")
os.system("mkdir images_2D+t")
os.system("mkdir images_process_2D+t")
os.system("mkdir images_2D+t_visu")

#copie des images de test et renommage aux standard de la fc catpgm
t=0
j=0
for i in range(0, n_tempo*n_coupe):
    os.system("cp images/test-"+str(i)+".pgm images_process_2D+t/image_process_coupe_"+numerote(j,3)+"_t_"+numerote(t,4)+".pgm")
    if (j==249):
        t=t+1
        j=0
    else:
        j=j+1
    
    
for i in range(0,n_coupe):
    print("image 2D+t coupe "+str(i)+" en traitement")
    
    #generation de l image 2D+t a partir d une meme coupe a diff temps
    ligne="catpgm images_process_2D+t/image_process_coupe_"+numerote(j,3)+"_t_ "+ str(0)+ " "+str(15)+" [80 80 16] images_2D+t/image_2D+t_coupe_"+numerote(i,3)+".pgm"
    command(ligne)
    command("seuil images_2D+t/image_2D+t_coupe_"+numerote(i,3)+".pgm "+str(seuil)+" images_2D+t/image_2D+t_s_coupe_"+numerote(i,3)+".pgm")
    command("pgm2vtk images_2D+t/image_2D+t_s_coupe_"+numerote(i,3)+".pgm 2 images_2D+t_visu/image_2D+t_visu_coupe_"+numerote(i,3)+".vtk")
    