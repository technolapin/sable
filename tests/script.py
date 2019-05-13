import os
os.system("ls")
root = ".."
libs = root + "/pink/linux/bin/"

os.system("rm *.pgm")

def command(cmd):
    os.system(libs+cmd)

os.system("cp ../extraction/rangee/00/tranche-0000t00.pgm  seuil.pgm")
os.system("cp ../extraction/images/test-0.pgm originale.pgm")

command("inverse seuil.pgm seuil_inverse.pgm")
command("dist seuil_inverse.pgm 80 dist.pgm")
command("inverse dist.pgm dist_inv.pgm")
command("minima dist_inv.pgm 4 minimas.pgm")
command("watershed dist_inv.pgm minimas.pgm 8 watershed.pgm")
command("add seuil_inverse.pgm watershed.pgm superpose.pgm")
os.system("ls")
command("inverse superpose.pgm final.pgm")


