import numpy as np
import os
import random

resultats = np.load("../extraction/tracking_3D/resultats.npy")
n_tempo = 16
def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s

empty3D = " empty "
command("genimage 3D/00 0 "+empty3D)


 
def genimage(image_name, colour, image_modele):
    command("genimage "+image_modele+" "+str(colour)+" "+image_name)
    return image_name

def pgm2ppm(red, green, blue, image_out):
    command("pgm2ppm "+red+" "+green+" "+blue+" "+image_out)
    return image_out

def into_ppm(image_pgm, image_out):
    return pgm2ppm(image_pgm, image_pgm, image_pgm, image_out)

def add(image_a, image_b, image_out):
    command("add "+image_a+" "+image_b+" "+image_out)
    return image_out

def sub(image_a, image_b, image_out):
    command("sub "+image_a+" "+image_b+" "+image_out)
    return image_out

def extractplane(image_3D, plane, couche, image_out):
    command("extractplane "+image_3D+" "+str(couche)+" "+plane+" "+image_out)
    return image_out

def drawball(image_in, radius, x, y, z, image_out):
    command("drawball "+image_in+" "+str(rayon)+" "+str(x)+" "+str(y)+" "+str(z)+" "+image_out)
    return image_out

def extrait_coupes(image_3D, plane, debut, fin, prefixe):
    n = int(np.log(fin)) -1
    for i in range(debut, fin):
        extractplane(image_3D, plane, i, prefixe+numerote(i, n))


def colorie(image_pgm, color, image_out):
    tmp_name = "TMP_colorie_image_mienglknzarmkazemkfanzzaf"
    aplat_rouge = genimage(tmp_name+"aR", 255-color[0], image_pgm)
    aplat_vert  = genimage(tmp_name+"aG", 255-color[1], image_pgm)
    aplat_bleu  = genimage(tmp_name+"aB", 255-color[2], image_pgm)
    rouge = sub(image_pgm, aplat_rouge, aplat_rouge+ "s")
    vert  = sub(image_pgm, aplat_vert , aplat_vert + "s")
    bleu  = sub(image_pgm, aplat_bleu , aplat_bleu + "s")
    rgb = pgm2ppm(rouge, vert, bleu, image_out)
    os.system("rm "+aplat_rouge)
    os.system("rm "+aplat_vert)
    os.system("rm "+aplat_bleu)
    os.system("rm "+rouge)
    os.system("rm "+vert)
    os.system("rm "+bleu)
    return rgb



image_in = "3D/00"
"""

extrait_coupes(image_in, "xy", 0, 250, "Redessine/gris_")
for i in range(250):
    colorie("Redessine/gris_"+numerote(i, 4), [250, 0, 0], "Redessine/col_"+numerote(i, 4))
"""

blank = genimage("blank", 0, image_in)
colors = []
for i in range(len(resultats)):
    grain = resultats[i]
    colors.append([random.randrange(255) for i in range(3)])

rayon = 4
for t in range(n_tempo):
    print("t=", t)
    padding_temporel = numerote(t, 2)
    os.system("mkdir Redessine/"+padding_temporel)
    dossier = "Redessine/"+padding_temporel+"/"
    dossier_somme = dossier+"somme/"
    os.system("mkdir "+dossier_somme[:-1])
    print("initializing...")
    for i_couche in range(250):
        couche_pad = numerote(i_couche, 4)
        into_ppm(blank, dossier_somme+couche_pad)
    print("starting process")
    for i in range(len(resultats)):
        print("grain", i, "/", len(resultats)-1)
        indice = numerote(i, 3)
        [x, y, z] = [resultats[i][j][t] for j in range(3)]
        balle = drawball(blank, rayon, x ,y, z, dossier+"nb_"+indice)

        os.system("mkdir "+ dossier+"grain_nb_"+indice)
        dossier_grain = dossier+"grain_nb_"+indice +"/"
        extrait_coupes(balle, "xy", 0, 250, dossier_grain)

        os.system("mkdir "+ dossier+"grain_col_"+indice)
        dossier_grain_col = dossier+"grain_col_"+indice +"/"
        for i_couche in range(max(z-rayon, 0), min(z+rayon+1, 250)):
            couche_pad = numerote(i_couche, 4)
            nom_image = dossier_grain+couche_pad
            couche_col = colorie(nom_image, colors[i], dossier_grain_col+couche_pad)
            add(dossier_somme+couche_pad, couche_col, dossier_somme+couche_pad)
        os.system("rm -R "+dossier_grain)
        os.system("rm "+balle)
        
    
"""
## TODO
for t in range(n_tempo):
    padding_temporel = numerote(t, 2)
    os.system("mkdir Redessine/"+padding_temporel)
    image_somme = genimage("Redessine/"+padding_temporel+"/")
    for i in range(len(resultats)):
        [x, y, z] = [resultats[i][j][t] for j in range(3)]
        color = colors[i]
        
        
"""
