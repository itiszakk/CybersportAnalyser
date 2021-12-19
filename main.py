import os
import zipfile

def createDirectory():
    if (os.path.exists("temp")):
        removeDirectory()
    else:
        os.mkdir("temp")

def removeDirectory():
    for root, dirs, files in os.walk("temp", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir("temp")

def installSoft():
    print("Installing PostgreSQL...")
    postgresZip = zipfile.ZipFile("vendor\postgresql-14.1-1-windows-x64-binaries.zip")
    postgresZip.extractall("temp")
    postgresZip.close()

def main():
    print("Creating directory...")
    createDirectory()

    print("Installing soft...")
    installSoft()

    os.system("pause")
    print("Removing directory...")
    removeDirectory()

if __name__ == "__main__":
    main()