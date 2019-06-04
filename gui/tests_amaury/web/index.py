#!/usr/bin/env python

# NB : Il faut que ce script soit executable !  

# J'aime le Web


""" CGI """
import cgitb
cgitb.enable()

print("Content-Type: text/html; charset=utf-8\n")


""" GENERER LE HTML """
html = '''<!DOCTYPE html>
<head>
<title>Page Web</title>
</head>

<body>
<p><b>Blabla</p>'''


"""
# https://stackoverflow.com/questions/14824522/dynamically-serving-a-matplotlib-image-to-the-web-using-python
format = "png"
sio = cStringIO.StringIO()
pyplot.savefig(sio, format=format)
print "Content-Type: image/%s\n" % format
msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY) # Needed this on windows, IIS
sys.stdout.write(sio.getvalue())

html += '''<img src="data:image/png;base64,''' + sio.getvalue().encode("base64").strip() + '''/>'''
"""

html +='''
</body>
</html>'''


""" ENVOYER """
print(html)
