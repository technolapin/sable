import os
import imageio as io
import numpy as np

##extraction des images
n_tempo = 16 #nb de temps
n_coupe = 250
seuil = 170 #pour les images en noir et blanc

#permet de numeroter les fichiers avec padding
def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s

#pour utiliser plus facilement les outils de pink
def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

#pour ajouter l'aire à la liste des centres
def add_area(file_name, image_name):
    f = open(file_name, "r")
    lines = f.readlines();
    f.close()
    f = open(file_name, "w")
    f.write(lines[0])
    f.close()
    for i in range(1, len(lines)):
        command("showpoint "+image_name+" "+lines[i][:-1]+" 0 | trucs_en_c/filtre_showpoint >> " + file_name)

#pour récupérer les éléments d'un .list
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



os.system("rm -R formes")
os.system("rm -R centres")
os.system("rm -R labels")
os.system("rm -R appercu")
os.system("rm -R images")
os.system("rm -R tmp")
os.system("mkdir formes")
os.system("mkdir centres")
os.system("mkdir labels")
os.system("mkdir appercu")
os.system("mkdir images")
os.system("mkdir tmp")


for t in range(0, n_tempo):
    #créé les dossiers contenant les image
    os.system("mkdir formes/" + numerote(t, 2))
    os.system("mkdir centres/" + numerote(t, 2))
    os.system("mkdir labels/" + numerote(t, 2))
    os.system("mkdir appercu/" + numerote(t, 2))

#extraction des images du tif en images bmp dans tmp
os.system("convert gros_sable.tif tmp/test.bmp")


donnees = []
for i in range (0, n_tempo):
    donnees.append([])

    
for i in range(0, n_tempo*n_coupe):
    print("Image "+str(i)+" en cours de traîtement...")
    #conversion des images en pgm + indexation
    os.system("convert tmp/test-"+str(i)+".bmp images/test-"+str(i)+".pgm")
    coupe = numerote(i % n_coupe, 4)  #donne le numero de la coupe
    temps = numerote(i // n_coupe, 2) #donne le temps
    

    #paths des fichiers d'entrée et de sortie
    input_file = "images/test-" + str(i) + ".pgm"
    output_file_formes = "formes/" + temps + "/tranche-" + coupe + "t" + temps + ".pgm"
    output_file_center = "centres/" + temps + "/tranche-" + coupe + "t" + temps + ".list"
    output_file_labels = "labels/" + temps + "/tranche-" + coupe + "t" + temps + ".pgm"
    output_file_appercu = "appercu/" + temps + "/tranche-" + coupe + "t" + temps + ".png"

    # pre-traitement (seuil, nettoyage, inversion ...)
    command("seuil "+input_file+" "+str(seuil)+" tmp/seuil.pgm")
    command("deletewells tmp/seuil.pgm 8 tmp/seuil_hclean.pgm")
    command("deletepeaks tmp/seuil_hclean.pgm 8 tmp/seuil_clean.pgm")
    command("inverse tmp/seuil_clean.pgm tmp/seuil_inverse.pgm")

    # carte des distances
    command("dist tmp/seuil_inverse.pgm 0 tmp/dist.pgm")
    command("inverse tmp/dist.pgm tmp/dist_inv.pgm")

    # minimas
    command("minima tmp/dist_inv.pgm 4 tmp/minimas.pgm")
    command("barycentre tmp/minimas.pgm 8 tmp/centres.pgm")
    command("pgm2list tmp/centres.pgm b "+output_file_center)

    # ligne de separation des eaux
    command("watershed tmp/dist_inv.pgm tmp/minimas.pgm 8 tmp/watershed.pgm")
    command("add tmp/seuil_inverse.pgm tmp/watershed.pgm tmp/superpose.pgm")
    command("inverse tmp/superpose.pgm "+output_file_formes)

    # numerote les formes connexes
    # pas utilise pour l'instant
    command("label "+output_file_formes+" 8 fgd "+output_file_labels)

    # calcule l'aire des formes connexes
    command("attribute "+output_file_formes+" 8 0 0 0 tmp/attributes.pgm")

    #on recupere l'aire de chaque forme detectee, et on importe dans centres
    add_area(output_file_center, "tmp/attributes.pgm")
    centres = parse_list(output_file_center)


    #on ne prend pas en compte les trop petites formes
    aire_min = 10
    j = 0
    while j < len(centres):
        if centres[j][2] < aire_min:
            del(centres[j])
        j += 1
        

    

    ## Algo qui suit:
    # on fusionnes les formes trop proches par rapport a leur taille
    # pour etre des grains differents
    # suppose que les grains sont vaguements ronds
    # complexite: (nombre de formes)²

    # variable correspondant a la qualite des cercles
    # = 1: on suppose cercles parfaits
    # < 1: l'algorithmes sera plus laxe 
    circlisme = 1.0
    """
    flag =  True
    while flag:
        flag = False
        for i_a in range(0, len(centres)):
            for i_b in range(0, len(centres)):
                if i_a != i_b:
                    dist = np.sqrt(np.power(centres[i_a][0]-centres[i_b][0], 2) + np.power(centres[i_a][1]-centres[i_b][1], 2))
                    area_a = centres[i_a][2]
                    area_b = centres[i_b][2]
                    r_a = np.sqrt(area_a/np.pi)
                    r_b = np.sqrt(area_b/np.pi)
                    print("distance entre "+str(i_a)+" et "+str(i_b) +" = "+ str(dist), str((r_a+r_b)*circlisme))
                    if dist < (r_a+r_b)*circlisme:
                        command("drawline "+output_file_formes+" "+str(centres[i_a][0])+" "+str(centres[i_a][1])+" "+str(centres[i_b][0])+ " "+str(centres[i_b][1])+" "+output_file_formes)

                        
                        x = (centres[i_a][0]*area_a+centres[i_b][0]*area_b)/(area_a+area_b)
                        y = (centres[i_a][1]*area_a+centres[i_b][1]*area_b)/(area_a+area_b)
                        centres[i_a][0] = x
                        centres[i_a][1] = y
                        centres[i_a][2] = area_a+area_b
                        del centres[i_b]
                        flag = True
                        break
            if flag:
                break
    """
    export_list(centres, "tmp/centrestmp.list")
    os.system("./trucs_en_c/fusionne_proches tmp/centrestmp.list tmp/centres_fusion.list "+str(circlisme))

    centres = parse_list("tmp/centres_fusion.list")
    
    f = open("tmp/centres.lst", "w")
    f.write("b "+str(len(centres))+"\n")
    for forme in centres:
        f.write(str(int(forme[0]))+" "+str(int(forme[1]))+"\n")
    f.close()

    # on transpose la liste finale des centres en pgm puis en png
    # pour visualiser avec de la couleur
    # (cf la doc)
    
    command("list2pgm tmp/centres.lst 80 80 1 tmp/filtered_centres.pgm")
    command("genlut 256 0 200 0 255 0 2550 lut.lut")
    command("pgm2ppm tmp/filtered_centres.pgm lut.lut tmp/colored_centers.ppm")
    # vire le fond noir de l'image en le rendant transparent
    os.system("convert tmp/colored_centers.ppm -transparent black tmp/transp_centers.png")
    # superpose l'image des formes et celles des centres colores
    os.system("composite -compose over tmp/transp_centers.png "+output_file_formes+" "+output_file_appercu)
    
    # on sauvegarde les resulats dans la liste des resultats
    donnees[i//n_coupe].append(centres)


#on ecrit l'ensemble des resultats dans un fichier texte
file = open("donnees","w")
for t in range(0, n_tempo):
    print(t)
    for z in range(0, n_coupe):
        for forme in donnees[t][z]:
            file.write(str(forme[0])+" "+str(forme[1])+" "+str(forme[2])+"\n")
        file.write("\n")
    file.write("####\n")
file.close()

#os.system("rm -R tmp")


