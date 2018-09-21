#!/bin/bash
rm output_.midi
rm output_.pdf
rm out/output_.ly
python create.py 123456 40 bass_8 48 72 slow fast medium faster quiet more_medium tasto_y_funny

cd out/123456

/Applications/LilyPond.app/Contents/Resources/bin/lilypond fullOutput.ly
open fullOutput.pdf
open fullOutput.midi
cd ../..