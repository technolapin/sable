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

command("inverse originale.pgm originale_inverse.pgm")
command("maxima dist.pgm 4 maxima.pgm")
command("inverse dist.pgm dist_inv.pgm")
command("minima dist_inv.pgm 4 minimas.pgm")

command("seuil dist.pgm 1 dist_seuil.pgm")

print("test")
command("watershed originale_inverse.pgm dist.pgm 4 watershed.pgm")

command("add seuil.pgm watershed.pgm supperpose.pgm")

