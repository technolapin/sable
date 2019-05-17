##importations
import os 
import matplotlib.image as mpimg
import numpy as np
from scikit-image import io

##extraction des images
n_tempo = 16 #nb de temps
n_coupe = 250
seuil = 170 #pour les images en noir et blanc
#seuil = 120

#permet de nomer les fichiers par padding
def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s


os.system("rm -R formes")
os.system("rm -R centres")
os.system("rm -R labels")
os.system("mkdir formes")
os.system("mkdir centres")
os.system("mkdir labels")

for t in range(0, n_tempo):
    os.system("mkdir formes/" + numerote(t, 2)) 
    os.system("mkdir centres/" + numerote(t, 2)) 
    os.system("mkdir labels/" + numerote(t, 2)) 
os.system("rm images -R")    #supprimer
os.system("mkdir images")

os.system("mkdir tmp")
os.system("convert gros_sable.tif tmp/test.bmp") #extraction des images du tif en images bmp dans tmp

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

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


    
donnees = []
for i in range (0, n_tempo):
    donnees.append([])

    
for i in range(0, n_tempo*n_coupe):
    print("Image "+str(i)+" en cours de traitement...")
    os.system("convert tmp/test-"+str(i)+".bmp images/test-"+str(i)+".pgm") #conversion des images en pgm + indexation
#    os.system("ls")
    coupe = numerote(i % n_coupe, 4) #donne le numero de la coupe
    temps = numerote(i // n_coupe, 2)    #donne le temps
    

    input_file = "images/test-" + str(i) + ".pgm"
      
    output_file_forme = "formes/" + temps + "/tranche-" + coupe + "t" + temps + ".pgm"
    output_file_center = "centres/" + temps + "/tranche-" + coupe + "t" + temps + ".list"
    
    #seuillage
    command("seuil "+input_file+" "+str(seuil)+" tmp/seuil.pgm")
    
    #destruction defaults noirs connexes < 8 pixels
    command("deletewells tmp/seuil.pgm 8 tmp/seuil_clean.pgm")
    
    command("inverse tmp/seuil_clean.pgm tmp/seuil_inverse.pgm")
    
    #carte des distances
    command("dist tmp/seuil_inverse.pgm 80 tmp/dist.pgm")
    
    #command("long2byte tmp/dist_long.pgm 0 tmp/dist.pgm")
    #command("areaclosing tmp/dist.pgm 8 100 tmp/dist_filtered.pgm")
    
    command("inverse tmp/dist.pgm tmp/dist_inv.pgm")
    command("minima tmp/dist_inv.pgm 4 tmp/minimas.pgm")
    
    #ligne de separation des eaux, trouve la ligne de separation des grains qui sont colles
    command("watershed tmp/dist_inv.pgm tmp/minimas.pgm 8 tmp/watershed.pgm")
    
    #superpose watershed sur seuil_inverse
    command("add tmp/seuil_inverse.pgm tmp/watershed.pgm tmp/superpose.pgm")
    command("inverse tmp/superpose.pgm tmp/superpose_inverse.pgm")

    command("barycentre tmp/minimas.pgm 8 tmp/centres.pgm")
    
    os.system("cp tmp/superpose_inverse.pgm "+output_file_forme)
    #os.system("cp tmp/centres.pgm "+output_file_center)
    
    #creation de la liste des centres
    command("pgm2list tmp/centres.pgm b "+output_file_center)
    
    #numerotation des formes connexes
    command("label tmp/superpose_inverse.pgm 8 fgd tmp/lab.pgm")

    output_file_label = "labels/" + temps + "/tranche-" + coupe + "t" + temps + ".pgm"
    
    #cette convertion a juste pour but de faciliter le visionnage
    #on pert potentiellement de l'information ce faisant
    command("long2byte tmp/lab.pgm 0 "+output_file_label)

    #seuillage des formes connexes en fonction de leur aire
    command("attribute tmp/superpose_inverse.pgm 8 0 0 0 tmp/attributes.pgm")
    command("long2byte tmp/attributes.pgm 0 tmp/attributes_scaled.pgm")
    
    centres = parse_list(output_file_center)

    
    fr_aires=open("tmp/attributes_scaled.pgm","r")
    lines=fr_aires.readlines()
    fr_aires.close()
    
    fr_aires=open("tmp/attributes_scaled.pgm","w")
    fr_aires.write(bytes("P5\n","AsCII"))
    fr_aires.write(lines[1])
    fr_aires.write(bytes("42949672895\n","ASCII"))
    for line in lines[3:]:
        fr_aires.write(line)
    fr_aires.close()
        
    img_aires=io.imread("tmp/attributes_scaled.pgm")

    for forme in centres:
        x = forme[0]
        y = forme[1]
        forme.append(img_aires[y][x])

    donnees[i//n_coupe].append(centres)
    """
    img_centres = mpimg.imread("tmp/centres.pgm")
    centres = []
    for j in range(0, len(img_centres)):
        for i in range(0, len(img_centres[j])):
            if img_centres[i][j] > 0:
                centres.append([j, i])
    for coords in centres:
        cmd = ("selectcomp "
        +output_file_forme
                +" 8 "
                +str(coords[0])
                +" "
                +str(coords[1])
                +" 0 tmp/select.pgm")
        command(cmd)
        
        img_forme =  mpimg.imread("tmp/select.pgm")
        area = 0
        for i in range(0, len(img_forme)):
            for j in range(0, len(img_forme[i])):
                if img_forme[i][j] > 0:
                    area += 1
        print(coords)
        coords.append(area)
        """
        
        
     #permet de resoudre le pb de séparation d'un meme grain fait par le watershed 
    flag =  True
    while flag:
        flag = False
        for i_a in range(0, len(centres)):
            for i_b in range(0, len(centres)):
                if i_a != i_b:
                    dist = np.sqrt(np.power(centres[i_a][0], 2) + np.power(centres[i_b][1], 2))
                    area_a = centres[i_a][2]
                    area_b = centres[i_b][2]
                    r_a = np.sqrt(area_a/np.pi)
                    r_b = np.sqrt(area_b/np.pi)
                    if dist < (r_a+r_b)*0.7:
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
    print(centres)
    donnees[i // n_coupe].append(centres)
    
    
#creation du fichier de donne
file = open("donnees","w")
for t in range(0, n_tempo):
    print(t)
    for z in range(0, n_coupe):
        for forme in donnees[t][z]:
            file.write(str(forme[0])+" "+str(forme[1])+" "+str(forme[2])+"\n")
        file.write("\n")
    file.write("####\n")
file.close()
os.system("rm -R tmp")


