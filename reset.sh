#!/bin/bash
touch evil.txt
echo "EVIL CODE!" > evil.txt
touch AFolder/superevil.txt
echo "EVIL CODE!" > AFolder/superevil.txt
chmod +x evil.txt
chmod +x AFolder/superevil.txt
rm -r Quarantine
mkdir Quarantine