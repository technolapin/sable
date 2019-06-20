import os
import numpy as np
def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s



 
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


def inverse(image_in, image_out):
    command("inverse "+image_in+" "+image_out)
    return image_out

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

def frame(image_modele, image_out):
    command("frame "+image_modele+" "+image_out)
    return image_out

def geodilat(image_in, mask, connexity, n_iterations, image_out):
    command("geodilat "+image_in+" "+mask+" "+str(connexity)+" "+str(n_iterations)+" "+image_out)
    return image_out
    
## l'image doit etre binaire
def vire_bord(image_in, image_out):
    fr = frame(image_in, "TMP_frame_azljebagambmqojbbbljzab")
    dil = geodilat(fr, image_in, 26, -1, image_out)
    os.system("rm "+fr)
    return sub(image_in, dil, image_out)


image = "../extraction/images_3D/image_3D_superpose_inv_t00.pgm"
#inv = inverse(image, "inv")
vire_bord(image, "borderless.pgm")

extrait_coupes(vire_bord(image, "borderless.pgm"), "xy", 0, 250, "tmp/bor")
extrait_coupes(image, "xy", 0, 250, "tmp/ori")
    
