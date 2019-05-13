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

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)


for i in range(0, n_tempo*n_coupe):
    print("Image "+str(i)+" en cours de traîtement...")
    os.system("convert tmp/test-"+str(i)+".bmp images/test-"+str(i)+".pgm") #conversion des images en pgm + indexation
#    os.system("ls")
    coupe = numerote(i % 250, 4) #donne le numero de la coupe
    temp = numerote(i // 250, 2)    #donne le temps
    
#seuillage

    input_file = "images/test-" + str(i) + ".pgm"
      
    output_file = "rangee/" + temp + "/tranche-" + coupe + "t" + temp + ".pgm"

        
    command("seuil "+input_file+" "+str(seuil)+" tmp/seuil.pgm")
    command("inverse tmp/seuil.pgm tmp/seuil_inverse.pgm")
    command("dist tmp/seuil_inverse.pgm 80 tmp/dist.pgm")
    command("inverse tmp/dist.pgm tmp/dist_inv.pgm")
    command("minima tmp/dist_inv.pgm 4 tmp/minimas.pgm")
    command("watershed tmp/dist_inv.pgm tmp/minimas.pgm 8 tmp/watershed.pgm")
    command("add tmp/seuil_inverse.pgm tmp/watershed.pgm tmp/superpose.pgm")
    os.system("ls")
    command("inverse tmp/superpose.pgm "+output_file)


    
os.system("rm -R tmp")
