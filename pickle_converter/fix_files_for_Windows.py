import os
import subprocess

rootdir = "./The-NELA-Toolkit/"
for subdir, dirs, fns in os.walk(rootdir):
    for fn in fns:
        if fn.endswith(".sav"):
            print "Converting to Windows format: ", fn
            subprocess.check_call([r"dos2unix.exe", subdir + os.sep + fn])