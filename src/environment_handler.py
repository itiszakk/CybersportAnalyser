import sys
import os
import subprocess
import zipfile
import pkg_resources
import config as cfg

def install_py_libs():
    installed_libs = {pkg.key for pkg in pkg_resources.working_set}
    missing_libs = cfg.required_libs - installed_libs
    
    if missing_libs:
        for lib in missing_libs:    
            print("Installing python lib: {}".format(lib))
            subprocess.run([sys.executable, "-m", "pip", "install", "--no-build-isolation", lib], stdout=subprocess.DEVNULL)

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