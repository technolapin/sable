import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

command("seuil originale.pgm 170 seuil.pgm")
command("inverse seuil.pgm seuil_inv.pgm")
command("dist seuil_inv.pgm 0 dist.pgm")
command("long2byte dist.pgm 0 dist_byte.pgm")
command("mult dist_byte.pgm gris.pgm dist_enhanced.pgm")
command("inverse dist_byte.pgm dist_inv.pgm")
command("minima dist_inv.pgm 8 minima.pgm")
