import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)


command("seuil image_3D_t00.pgm 170 seuil.pgm")
command("inverse seuil.pgm seuil_inv.pgm")
command("dist seuil_inv.pgm 80 dist.pgm")
command("seuil dist.pgm 3 dist_seuil.pgm")
command("inverse dist_seuil.pgm dist_inv.pgm")
command("minima dist_inv.pgm 4 minimas.pgm")
command("pgm2vtk minimas.pgm 1 test.vtk")
