import sys
import csv
# TODO make a database with viruses
# TODO make the python script read in the database of viruses
# TODO make the python script look at system files
# TODO make the python script keep track of what files it has read
# TODO make the python script check files for the signatures of the viruses
# TODO make the python script quarantine the files that have a virus signature
    # TODO decide what we mean by quarantine
# The file path should just be 
filepath = sys.argv[1]
def readInSignatures(filepath):
    with open(filepath, "r") as signature_database:
        signature_reader = csv.reader(signature_database, delimiter=',')
        for line in signature_reader:
            print('Part of the CSV ' + str(line))
            # virus_signature_parts = line.rsplit(',', 2)
            # print('virus name ' + virus_signature_parts[0])
            # print('virus signature ' + virus_signature_parts[1])
readInSignatures(filepath)