#!/bin/bash
touch evil.txt
echo "EVIL CODE!" > evil.txt
touch AFolder/superevil.txt
echo "EVIL CODE!" > AFolder/superevil.txt
chmod +x evil.txt
chmod +x AFolder/superevil.txt
chown marcussr AFolder/superevil.txt
chgrp marcussr AFolder/superevil.txt
rm -rf .Quarantine
mkdir -m 444 .Quarantine