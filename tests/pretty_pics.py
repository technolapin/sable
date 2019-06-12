import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s

couche = "197"

input_file = " ../extraction/images/test-"+couche+".pgm "
input_color = " input_color "
seuil = " seuil "
seuil_inv = " seuil_inv "
dist = " dist "
lut = " lut "
lut_nb = " lut_nb "
lut_2 = " lut_2 "
dist_color = " beau_dist_color "
lut_bord = " lut_bord "
lut_wat = " lut_wat "



#command("genlut 1000 0 1 0 200 200 200"+lut) marche bien
command("genlut 1000 0 1 0 200 200 200"+lut)
command("genlut 256 0 256 0 255 0 255"+lut_2)
command("genlut 256 0 0 0 256 0 0"+lut_nb)
command("genlut 256 0 0 0 255 255 255"+lut_bord)
command("genlut 256 0 0 0 255 255 255"+lut_wat)


command("seuil"+input_file+"170"+seuil)

command("inverse"+seuil+seuil_inv)

command("dist"+seuil_inv+"0"+dist)


command("colorize"+dist+lut+dist_color)
seuil_inv_ppm = " seuil_inv_ppm "
command("pgm2ppm "+seuil+lut_nb+seuil_inv_ppm)

command("add"+seuil_inv_ppm+dist_color+" aaa")
command("colorize"+input_file+lut_2+input_color)




input_border = " ../extraction/border_3D/border_3D_t_00.pgm "
input_3D = " ../extraction/images_3D/image_3D_t00.pgm "
input_water = " ../extraction/images_3D/image_3D_wat_t00.pgm "
os.system("mkdir borderland")
command("seuil "+input_3D+" 170 "+seuil)
for i in range(190, 200):

    brut = " borderland/brut_"+numerote(i, 3)+" "
    bord = " borderland/bord_"+numerote(i, 3)+" "
    wat = " borderland/wat_"+numerote(i, 3)+" "
    brut_col = " borderland/col_brut_"+numerote(i, 3)+" "
    bord_col = " borderland/col_bord_"+numerote(i, 3)+" "
    wat_col = " borderland/col_wat_"+numerote(i, 3)+" "
    add = " borderland/add_"+numerote(i, 3)+" "
    sl = " borderland/sl_"+numerote(i, 3)+" "
    sl_col = " borderland/col_sl_"+numerote(i, 3)+" "
    waterseuil = " borderland/waterseuil_"+numerote(i, 3)+" "
    command("extractplane "+input_border+str(i)+" xy"+bord)
    command("extractplane "+input_3D+str(i)+" xy"+brut)
    command("extractplane "+input_water+str(i)+" xy"+wat)
    command("extractplane "+seuil+str(i)+" xy"+sl)
#    command("sub"+brut+bord+brut)
    command("colorize"+bord+lut_bord+bord_col)
    command("colorize"+wat+lut_wat+wat_col)
    command("pgm2ppm"+sl+sl+sl+sl_col)
    command("pgm2ppm"+brut+brut+brut+brut_col)
    command("sub "+brut_col+bord_col+add)
    command("sub "+sl_col+wat_col+waterseuil)


os.system("cp borderland/add_"+couche+" beau_border.ppm")
os.system("cp borderland/waterseuil_"+couche+" beau_watershed.ppm")
os.system("cp borderland/col_sl_"+couche+" beau_seuil.ppm")
os.system("cp borderland/col_brut_"+couche+" beau_brut.ppm")
min_3D = " ../extraction/images_3D/image_3D_min_t00.pgm "
mn = " miiin "
mn_col = " beau_min "
#command("extractplane "+min_3D+str(couche)+" xy"+mn)
command("inverse "+dist+" inv_dist")
command("long2byte inv_dist inv_dist")
command("minima inv_dist 8 "+mn)
command("pgm2ppm"+mn+mn+mn+mn_col)
