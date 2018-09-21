import random
import math
import sys

myArgs = sys.argv
timestamp = myArgs[1]
favoritePitch = int(myArgs[2])
clefToUse = myArgs[3]
lowestAccomp = int(myArgs[4])
highestAccomp = int(myArgs[5])
waysToPlay = myArgs[6:]

TRANSPOSITION_FACTOR = (int(favoritePitch)-2)%12#because origionally written in D.
SOLO_SECTION = 'solo'

ACTUAL_FUCKING_PITCH = favoritePitch%12
ACTUAL_FUCKING_OCTAVE = int(favoritePitch/12) - 4
highestNote = highestAccomp
lowestNote = lowestAccomp


directions = []
for item in waysToPlay:
	if 'A_LABEL_TO_USE_' in item:
		item = item.replace("A_LABEL_TO_USE_",'')
		directions.append(['^\\markup{{"{message}"}}'.format(message=item.replace('_',' ')),''])

directions.append([SOLO_SECTION,SOLO_SECTION])

if len(directions)> 4:
	directions.append([SOLO_SECTION,SOLO_SECTION])
if len(directions) > 10:
	directions.append([SOLO_SECTION,SOLO_SECTION])

random.shuffle(directions)


def notGood(myList):
	for i in range(len(myList)-1):
		if myList[i][0]==myList[i+1][0] and myList[i][0] == SOLO_SECTION:
			return True
	return False

while notGood(directions):
	random.shuffle(directions)


chords = []
for i in range(len(directions)):
	chords.extend([[6, 14],[2,9], [7,11],[2,9],
	[6, 14],[2,9], [7,11],[4,9],
	[6, 14],[2,9], [7,11],[2,9],
	[6, 14],[7,11],[4,9],[2,9]])




centered = 48 #where 'zero octave' is


RESET = ' \\ottava #0'

noteNames = [[],[],[]]
noteNames[0] = ['c', 'cis', 'd', 'dis', 'e', 'f','fis','g','gis','a','ais','b'] # all sharp
noteNames[1] = ['c', 'des', 'd', 'ees', 'e', 'f','ges','g','aes','a','bes','b'] # all flat
noteNames[2] = ['c', 'des', 'd', 'ees', 'e', 'f','fis','g','aes','a','bes','b'] # mix / names
keyType = [2,1, 0,1,0,1,0,0,1,0,1,0]




def stringForNote(note,octave):
	ret = noteNames[keyType[ACTUAL_FUCKING_PITCH]][note%12]
	direction = int((math.floor(note/12) + octave))
	# print(note,octave,direction)
	if direction > 0:
		ret += '\''*direction
	elif direction < 0:
		ret += ','*(-1*direction)
	return ret

def optionsFromChord(notes):
	possibleOctaves = []
	for i in range(-4, 7):
		isValid = True
		for note in notes:
			testNote = note + 12*i + centered
			if testNote > highestNote or testNote<lowestNote:
				isValid = False
		if isValid:
			possibleOctaves.append(i)
	if(possibleOctaves==[]):
		print("BIG ERROR, OUT OF RANGE, USING CENTERED")
		return [0]

	return possibleOctaves

def makeContFromNotes(notes):
	if len(notes) == 0:
		return " r1 \n"
	return " < "+" ".join(notes)+" >1 \n"

def octaveCheck(note, octave):
	absolute = note+12*offset
	if absolute > 48:
		return "upper","  \\ottava #2 "
	elif absolute > 36:
		return "upper","  \\ottava #1 "
	elif absolute < -24:
		return "lower","  \\ottava #-2 "
	elif absolute < -12:
		return "lower","  \\ottava #-1 "
	return "",""


newChords = []
for chord in chords:
	newChords.append([chord[0]+TRANSPOSITION_FACTOR,chord[1]+TRANSPOSITION_FACTOR])
chords = newChords

hands = [[],[],[]]

prevUpperMessage = ""
prevLowerMessage = ""

for i in range(len(chords)):
	chord = chords[i]
	offset = random.choice(optionsFromChord(chord))
	upperNotes = []
	lowerNotes = []
	octavaMessage = ""
	octaveDir = ""
	postMessage = ''
	for note in chord:
		if note+12*offset > 12:
			upperNotes.append(stringForNote(note, offset))
		else:
			lowerNotes.append(stringForNote(note, offset))
		if(octaveDir == ""):
			octaveDir, octavaMessage = octaveCheck(note, offset)
	if i % 16 == 0:
		if(directions[int(i/16)][1]==SOLO_SECTION):
			postMessage = '^"Solo"'
		else:
			postMessage = directions[int(i/16)][1]
	upperMessage = octavaMessage if (octaveDir == "upper") else ("" if prevUpperMessage == "" or prevUpperMessage == RESET else RESET)
	lowerMessage = octavaMessage if (octaveDir == "lower") else ("" if prevLowerMessage == "" or prevLowerMessage == RESET else RESET)
	upperCont = upperMessage+ makeContFromNotes(upperNotes)	+ postMessage
	lowerCont = lowerMessage+ makeContFromNotes(lowerNotes)
	hands[0].append(upperCont)
	hands[1].append(lowerCont)
	prevUpperMessage = upperMessage
	prevLowerMessage = lowerMessage

for i in range(int(len(chords)/16)):
	pitchString = stringForNote(ACTUAL_FUCKING_PITCH,ACTUAL_FUCKING_OCTAVE)
	pitchAccentString = stringForNote(2+ACTUAL_FUCKING_PITCH,ACTUAL_FUCKING_OCTAVE)
	measure = ' r4 {pitch}2. '.format(pitch=pitchString)
	measureAccent = ' r4 {pitch}2. '.format(pitch=pitchAccentString)
	phrase = ' {mea} {add} ( {mea} {mea} {mea2} ) \n'
	if(directions[i][0] == SOLO_SECTION):
		hands[2].append(" R1*16 \\break \n")
	else:
		hands[2].append(phrase.format(add=directions[i][0],mea=measure,mea2=measure))
		hands[2].append(phrase.format(add="",mea=measure,mea2=measureAccent)+' \\break \n ')
		hands[2].append(phrase.format(add="",mea=measure,mea2=measure))
		hands[2].append(phrase.format(add="",mea=measure,mea2=measure) +' \\break \n ')


hands[0].insert(1," \\sustainOn ")
hands[1].insert(1," \\sustainOn ")

parts = []
for hand in hands:
	parts.append(" ".join(hand))


fd = open('template.ly')
out = open('out/'+timestamp+'/fullOutput.ly','w')
for l in fd:
	if '%key' in l:
		out.write('\\key {letter} \\major'.format(letter=noteNames[2][ACTUAL_FUCKING_PITCH]))
	elif '%part' in l:
		partNo = int(l[5:])
		out.write(parts[partNo])
	elif '%time' in l:
		out.write(timestamp)
	elif '%clef' in l:
		out.write('\\clef "'+clefToUse+'"\n')
	else:
		out.write(l)
fd.close()
out.close()



