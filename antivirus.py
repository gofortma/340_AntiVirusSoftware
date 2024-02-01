import sys
import csv
from pathlib import Path
import hashlib
import shutil
# TODO make a database with viruses
# TODO make the python script read in the database of viruses
# TODO make the python script look at system files
# TODO make the python script keep track of what files it has read
# TODO make the python script check files for the signatures of the viruses
# TODO make the python script quarantine the files that have a virus signature
    # TODO decide what we mean by quarantine
# To run do python3 antivirus.py ./signatures.csv . Quarantine
signatureToVirus = dict()
fileToHash = dict()
dangerousFiles = []
quarentineRestoreLocations = dict()

filepath = sys.argv[1]
startingLocation = sys.argv[2]
quarantineLocation = sys.argv[3]

def readInSignatures(filepath):
    with open(filepath, "r") as signature_database:
        signature_reader = csv.reader(signature_database, delimiter=',')
        for line in signature_reader:
            signatureToVirus[line[1]] = line[0]

readInSignatures(filepath)
print(signatureToVirus)

def scanFolder(startingLocation):
    startingPath = Path(startingLocation)
    for item in startingPath.iterdir():
        if item.is_dir():
            scanFolder(item)
        else:
            with open(item, "rb") as fileToScan:
                sha256 = hashlib.new('sha256')
                fileContents = fileToScan.read()
                sha256.update(fileContents)
                fileToHash[item] = sha256.hexdigest()

scanFolder(startingLocation)
print(fileToHash)

def findViruses():
    for file, hash in fileToHash.items():
        if hash in signatureToVirus:
            print("Found the virus " + str(signatureToVirus[hash]) + " in the file " + str(file))
            dangerousFiles.append(file)

findViruses()

def quarantineViruses():
    for file in dangerousFiles:
        fileInfo = Path.lstat(file)
        print("The file info is " + str(fileInfo))
        # Path.chmod(file, 0o444) #This should be read only
        #TODO backup old file permissions
        #TODO backup old file locatoin
        #TODO find a location in quarantine
        #TODO associate quarantined file with old file location and permissions
        #TODO make file read only
        break
        # shutil.move(file, quarantineLocation)
        # quarentineRestoreLocations[file] = 
        # fileToHash.pop(file)
quarantineViruses()

