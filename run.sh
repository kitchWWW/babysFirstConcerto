#!/bin/bash
echo "Starting from Concerto Server Call"
echo $1
cd engines/Baby-First-Generator-master
mkdir out/$1
python create.py $1 $2 $3 $4 $5
echo "Completed run"
cd out/$1
/Applications/Lilypond.app/Contents/Resources/bin/lilypond fullOutput.ly
lilypond fullOutput.ly