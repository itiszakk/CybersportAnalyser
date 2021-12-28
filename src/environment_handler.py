import os
import subprocess
import zipfile

def createDirectory(path):
    if os.path.exists(path):
        removeDirectory(path)
    print("Creating path: {}".format(path))
    os.mkdir(path)

def removeDirectory(path):
    print("Removing path: {}".format(path))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def installSoft(fromPath, toPath, zipName):
    print("Installing: {}".format(zipName))
    zip = zipfile.ZipFile(fromPath + r"\{}".format(zipName))
    zip.extractall(toPath)
    zip.close()

def execFile(filepath, arguments):
    print("Running: {} {}".format(filepath, arguments))
    subprocess.run(filepath + " " + arguments, stdout=subprocess.DEVNULL)