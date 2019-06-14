import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

def numerote(n, l):
    s = str(n)
    while len(s) < l:
        s = '0' + s
    return s

couche = "085"

input_file = " borderland/sl_"+couche+" "

minimum = "30"

command("attribute"+input_file+"8 "+minimum+" 1 0 attributes")
command("long2byte attributes attributes")
command("attribute attributes 8 "+minimum+" 1 0 attributes")
command("long2byte attributes attributes")
command("seuil attributes 1 propre")


os.system("mkdir tmp")


input_file = " ../extraction/images_3D/image_3D_s_t00.pgm "
#input_file = " ../extraction/border_3D/border_3D_t_00.pgm "

for i in range(250):
    image = "tmp/"+numerote(i, 3)
    command("extractplane"+input_file+str(i)+" xy "+image)
