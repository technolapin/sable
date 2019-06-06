##3D traitement

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

#gestion des repertoires
   
os.system("rm -R images_3D")
os.system("mkdir images_3D")

os.system("rm -R images_2D_for_3D")
os.system("mkdir images_2D_for_3D")

os.system("rm -R coupes_3D")
os.system("mkdir coupes_3D")
os.system("mkdir coupes_3D/x_y")
os.system("mkdir coupes_3D/x_z")
os.system("mkdir coupes_3D/y_z")

os.system("rm -R labels_3D")
os.system("mkdir labels_3D")

os.system("rm -R bary_3D")
os.system("mkdir bary_3D")
os.system("mkdir bary_3D/liste")

#copie des images de test et renommage aux standard de la fc catpgm
for i in range(0, n_tempo*n_coupes_xy):
    os.system("cp images/test-"+str(i)+".pgm images_2D_for_3D/image_2D_for_3D_"+numerote(i,4)+".pgm")


#traitement pour chaque temps
    
for t in range(0, n_tempo):
    
    print("image 3D numero "+str(t)+" en traitement")

    debut_colone = t * n_coupes_xy
    fin_colone   = debut_colone + n_coupes_xy - 1

    padding_temporel = numerote(t, 2) # pour pas trop recalculer
    
    
    #generation de l image 3D a partir des 250 coupes
    command("catpgm images_2D_for_3D/image_2D_for_3D_ "+
            str(debut_colone)+" "+str(fin_colone)+
            " [80 80 250] images_3D/image_3D_t"+padding_temporel+".pgm")

    
    #seuillage
    command("seuil images_3D/image_3D_t"+padding_temporel+".pgm "+
            str(seuil)+" "+
            "images_3D/image_3D_s_t"+padding_temporel+".pgm")
    
    command("inverse images_3D/image_3D_s_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_s_inv_t"+padding_temporel+".pgm")

    
     # carte des distances, avec distance euclidienne
    command("dist images_3D/image_3D_s_inv_t"+padding_temporel+".pgm "+
            "0 images_3D/image_3D_dist_proc_t"+padding_temporel+".pgm")

    command("long2byte images_3D/image_3D_dist_proc_t"+padding_temporel+".pgm "+
            "0 images_3D/image_3D_dist_t"+padding_temporel+".pgm")
    
    command("inverse images_3D/image_3D_dist_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_dist_inv_t"+padding_temporel+".pgm")
    

    # minimas
    command("minima images_3D/image_3D_dist_inv_t"+padding_temporel+".pgm "+
            "6 images_3D/image_3D_min_t"+padding_temporel+".pgm")

    
    #ligne de separation des eaux
    command("watershed images_3D/image_3D_dist_inv_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_min_t"+padding_temporel+".pgm "+
            "26 images_3D/image_3D_wat_t"+padding_temporel+".pgm")
    
    command("add images_3D/image_3D_s_inv_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_wat_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_superpose_t"+padding_temporel+".pgm")
    
    command("inverse images_3D/image_3D_superpose_t"+padding_temporel+".pgm "+
            "images_3D/image_3D_superpose_inv_t"+padding_temporel+".pgm ")




    #barycentres
    
    command("3dlabel images_3D/image_3D_superpose_inv_t"+padding_temporel+".pgm labels_3D/label_t_"+padding_temporel+".pgm")
    command("barycentrelab labels_3D/label_t_"+padding_temporel+".pgm bary_3D/bary_3D_t"+padding_temporel+".pgm")
    command("pgm2list bary_3D/bary_3D_t"+padding_temporel+".pgm B bary_3D/liste/bary_list_t"+padding_temporel+".list")





    #extraction des coupes 2D sur les 3 plans
    

     # pour moins de repetitions
    debut_commande = "extractplane images_3D/image_3D_superpose_inv_t"+padding_temporel+".pgm "



    #extraction des coupes sur (x,y)
    
    os.system("mkdir coupes_3D/x_y/"+padding_temporel)

    for u in range(0, n_coupes_xy):

        command(debut_commande+str(u)+" xy "+ "coupes_3D/x_y/"+padding_temporel+"/t_"+padding_temporel+"coupe_xy_"+numerote(u,4)+".pgm")
        
        
    #extraction des coupes sur (x,z)
    
    os.system("mkdir coupes_3D/x_z/"+padding_temporel)
    
    for u in range(0, n_coupes_xz):
    
        command(debut_commande+str(u)+" xz "+ "coupes_3D/x_z/"+padding_temporel+"/t_"+padding_temporel+"coupe_xz_"+numerote(u,4)+".pgm")
        
    
    #extraction des coupes sur (y,z)
    
    os.system("mkdir coupes_3D/y_z/"+padding_temporel)
    
    for u in range(0, n_coupes_yz):
        
        command(debut_commande+str(u)+" yz "+ "coupes_3D/y_z/"+padding_temporel+"/t_"+padding_temporel+"coupe_yz_"+numerote(u,4)+".pgm")        
        
#        prefix_sortie = "coupes_3D_/y_z/"+padding_temporel+"/t_"+padding_temporel+"coupe_yz_"+numerote(u,4)
#        image_coupe = prefix_sortie + ".pgm"
#    
#        command(debut_commande + str(u)+" yz "+ image_coupe)
       
