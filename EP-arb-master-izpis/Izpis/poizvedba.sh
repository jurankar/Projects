#!/bin/bash

#	Skripta pozene program Networking.java in
#	nato rezultate takoj commit-a na github
#	v obliki markdowna

echo "Hello, who am I talking to?"

read name

echo "Pozdravljeni $name!"
echo ""

DATE=`date +%Y-%m-%d`
	
# ustvari datoteko in vanjo vpise osnovne podatke
echo "# Arbitražni rezultati" > out.md
echo "\`" "author: $name" "\`" >> out.md
echo "\`""date : $DATE""\`" >> out.md
echo "---" >> out.md

echo "## Vrnjeni rezultati poizvedbe:" >> out.md

# prevedemo in pozenemo aplikacijo
javac -cp ".:./json-20180813.jar" Networking.java
java -cp ".:./json-20180813.jar" Networking

# commitamo na github
git add out.md
git commit out.md -m "Poizvedba dne: $DATE, ime = $name"
git push origin master
