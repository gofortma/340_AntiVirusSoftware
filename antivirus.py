import sys
import csv
from pathlib import Path
import hashlib
import shutil
import uuid
from stat import S_IREAD, S_IRGRP, S_IROTH
from pwd import getpwnam
# TODO make a database with viruses
# TODO make the python script read in the database of viruses
# TODO make the python script look at system files
# TODO make the python script keep track of what files it has read
# TODO make the python script check files for the signatures of the viruses
# TODO make the python script quarantine the files that have a virus signature
    # TODO decide what we mean by quarantine
# To run do python3 antivirus.py ./signatures.csv . .Quarantine
user = "root"
rootUid = getpwnam(user).pw_uid
rootGid = getpwnam(user).pw_gid
signatureToVirus = dict()
fileToHash = dict()
dangerousFiles = []
quarantineRestoreInformation = dict()
class fileRestoreInformation:
    def __init__(self, originalPath, originalPermissions):
        self.originalPath = originalPath
        self.originalPermissions = originalPermissions
    def __str__(self):
        return f"{self.originalPath},{self.originalPermissions}"

filepath = sys.argv[1]
startingLocation = sys.argv[2]
quarantineLocation = sys.argv[3]
quarantinePath = Path(quarantineLocation)

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
print("The dangerous files are " + str(dangerousFiles))

def quarantineViruses():
    for file in dangerousFiles:
        print("Beginning quarantine of dangerous file " + str(file))
        #Need to assign the file a UUID maybe to avoid duplicates? In the quarantine bucket have a new name.
        #Associate with the original name
        virusFileId = uuid.uuid4().hex #This one is cyrytographically secure
        fileInfo = file.lstat()
        virusStore = fileRestoreInformation(file, fileInfo)
        quarantineRestoreInformation[virusFileId] = virusStore
        print("The virus UUID is " + virusFileId)
        print("The virus restore information is " + str(virusStore))
        newVirusPath = quarantinePath.joinpath(virusFileId)
        trueVirusPath = shutil.move(file, newVirusPath)
        print("The virus should not be located in " + str(newVirusPath))
        trueVirusPath.chmod(S_IREAD|S_IRGRP|S_IROTH) #This turns on read only for Windows. For linux it should make the file have the proper permissions
        shutil.chown(trueVirusPath, rootUid, rootGid)
        # Path.chmod(file, 0o444) #This should be read only
        # filesPath = shutil.move(file, quarantineLocation)
        # print("Maybe moved to " + str(filesPath))
        # newNamesFile = Path.with_name(filesPath, virusFileId)
        # Path.joinpath(quarantineLocation, virusFileId)
        #TODO possibly make the file owned by a different account as well so the owner cannot restore their permissions
        #TODO there may be more permissions possible for quarantining
        # shutil.move(file, quarantineLocation)
        # quarentineRestoreLocations[file] = 
        # fileToHash.pop(file)
quarantineViruses()
# for fileId, fileRestoreInfo in quarantineRestoreInformation.items():
    # print("The virus restore information for item " + fileId + " is " + fileRestoreInfo)

