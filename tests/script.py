import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

"""
command("seuil image_3D_t00.pgm 170 seuil.pgm")
command("inverse seuil.pgm seuil_inv.pgm")
command("dist seuil_inv.pgm 80 dist.pgm")
command("seuil dist.pgm 3 dist_seuil.pgm")
command("inverse dist_seuil.pgm dist_inv.pgm")
command("minima dist_inv.pgm 4 minimas.pgm")
command("pgm2vtk minimas.pgm 1 test.vtk")
"""

input_file = "image_3D_t00.pgm"
seuil = 170
output_file_formes = "formes.pgm"
output_file_labels = "labels.pgm"

# pre-traitement (seuil, nettoyage, inversion ...)
command("seuil "+input_file+" "+str(seuil)+" seuil.pgm")
command("inverse seuil.pgm seuil_inverse.pgm")

# carte des distances
command("dist seuil_inverse.pgm 0 dist_long.pgm")
command("long2byte dist_long.pgm 0 dist.pgm")
command("inverse dist.pgm dist_inv.pgm")

# minimas
command("minima dist_inv.pgm 26  minimas.pgm")

# ligne de separation des eaux
command("watershed dist_inv.pgm minimas.pgm 26 watershed.pgm")
command("add seuil_inverse.pgm watershed.pgm superpose.pgm")
command("inverse superpose.pgm "+output_file_formes)
command("3dlabel "+output_file_formes+" labels.pgm")
#command("long2byte labels.pgm 0 "+output_file_labels)
command("pgm2vtk labels.pgm 2 test.vtk")
command("barycentrelab labels.pgm bary.pgm")
command("pgm2vtk bary.pgm 2 bary.vtk")
command("add labels.pgm bary.pgm labels.pgm")
command("pgm2list bary.pgm B bary.list")


def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s


for i in range(250):
    num = numerote(i, 4)
    print(num)
    command("extractplane labels.pgm "+num+" xy images/couche_xy-"+num+".pgm")
    command("randrgb images/couche_xy-"+num+".pgm images/couche_xy_colored-"+num+".pgm ")  

for i in range(80):
    num = numerote(i, 4)
    print(num)
    command("extractplane labels.pgm "+num+" xz images/couche_xz-"+num+".pgm")
    command("randrgb images/couche_xz-"+num+".pgm images/couche_xz_colored-"+num+".pgm ")  
    
