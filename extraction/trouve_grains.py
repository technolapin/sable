import os 

##extraction des images
n_tempo = 16 #nb de temps
n_coupe = 250
seuil = 170 #pour les images en noir et blanc

#permet de nomer les fichiers par padding
def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s

for t in range(0, n_tempo):
    os.system("rm -R rangee/" + numerote(t, 2)) #supprime les dossiers et son contenu contenant les images
    os.system("mkdir rangee/" + numerote(t, 2)) #créé les dossiers contenant les images

os.system("rm images/*")    #supprimer
os.system("mkdir tmp")
os.system("convert gros_sable.tif tmp/test.bmp") #extraction des images du tif en images bmp dans tmp



for i in range(0, n_tempo*n_coupe):
    print("Image "+str(i)+" en cours de traîtement...")
    os.system("convert tmp/test-"+str(i)+".bmp images/test-"+str(i)+".pgm") #conversion des images en pgm + indexation
    coupe = numerote(i % 250, 4) #donne le numero de la coupe
    temp = numerote(i // 250, 2)    #donne le temps
    
#seuillage
    os.system("../pink/linux/bin/seuil images/test-"
              + str(i)
              + ".pgm "
              + str(seuil)
              + " rangee/"
              + temp
              + "/tranche-"
              + coupe
              + "t"
              + temp
              + ".pgm")

    
os.system("rm -R tmp")
