#!/usr/bin/env python
#SpeakPython allows developers to add speech recognition support to their Python applications
#Copyright (C) 2015  Eric Matthews

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of 
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os;
import sys;

def printHelp():
	print "\nRun this module by typing:\n\n\tpython MakeProject.py <appName> [sps file/folder]\n\n\tExample: python MakeProject.py calc calc.sps\n\n";

if len(sys.argv) < 2:
	print "Invalid command.";
	printHelp();
	sys.exit();

appName = sys.argv[1];
spsName = appName + ".sps";

if len(sys.argv) > 2:
	spsName = sys.argv[2];

#make database files
print "Trying to create database (" + appName  + ".db) from sps files...";
retCode = os.system("sudo SpeakPythonMakeDB.py " + appName + " " + spsName);

if retCode != 0:
    print "Build has errors: code " + str(retCode);
    sys.exit(retCode);

print "Trying to create jsgf grammar used for speech recognition from sps files...";
retCode = os.system("sudo SpeakPythonMakeJSGF.py " + appName + " " + spsName);

#do only if JSGF parse succeeded
if retCode == 0:
    print "Trying to convert jsgf grammar into an fsg grammar using sphinx_jsgf2fsg for use with pocketsphinx speech recognition...";
    retCode = os.system("sphinx_jsgf2fsg -jsgf " + appName + ".jsgf -fsg " + appName + ".fsg");

    if retCode == 0:
        print "Converted JSGF successfully!";
    else:
	print "Build completed with errors!";
	sys.exit(2);

else:
    print "Failed to create jsgf grammar (THIS IS FINE FOR NON-SPEECH PROJECTS). Code:" + str(retCode);
    print "Text-only build completed successfully!";
    sys.exit(1);

#########################################################
#only reaches here if successfully converted JSGF to FSG#
#########################################################

wordsFile = "grammar_words_temp.txt";

print "Extracting words from jsgf grammar...";

#copy pocketsphinx dictionary words from default dic file to appName.dic
retCode = os.system("cp /usr/local/bin/pocketsphinx.dic " + appName + ".dic");
if retCode != 0:
	print "Failed to copy pocketsphinx default dictionary from /usr/local/bin/pocketsphinx.dic.";
	sys.exit(4);	

retCode = os.system("cp " + appName + ".jsgf " + wordsFile);

if retCode != 0:
	print "Failed to copy jsgf file to temporary file (" + wordsFile + ").";
	sys.exit(5);

#replace everything in JSGF but the words
retCode = os.system(r"perl -p -i -e 's/#[^\n]+/ /sg' " + wordsFile);

#exit if perl fails
if retCode != 0:
	print r"The perl command (perl -p -i -e 's/#[^\n]+/ /sg' " + wordsFile + ") failed to properly run. Please make sure perl is installed."
	sys.exit(3);

os.system(r"perl -p -i -e 's/public/ /sg' " + wordsFile);
os.system(r"perl -p -i -e 's/grammar [a-zA-Z0-9_]+;/ /sg' " + wordsFile);
os.system(r"perl -p -i -e 's/\<[a-zA-Z0-9_]+\>/ /sg' " + wordsFile);
os.system(r"perl -p -i -e 's/[\|\[\]\(\)=;]/ /sg' " + wordsFile);

os.system("perl -p -i -e 's/\\s+/\n/sg' " + wordsFile);

#read each line and sort by length of word descending
lines = [];
with open(wordsFile, "r") as f:
	lines = [x.strip("\n") for x in f]

lines.sort(key=len);

print "Appending new words to dictionary..."

#if the word does not appear in the dictionary already, append it
wf = open(wordsFile, "w");
newWordsExist = False;

for word in lines:
	if word:
		#find instance of word in dictionary
		grepRet = os.system("grep -q '^" + word + "\\s' " + appName + ".dic");
		if grepRet != 0: #we didn't find the word in the dictionary
			wf.write(word + "\n\n"); #add it to word list temp
			newWordsExist = True;

wf.close();

#use g2p.py module (if installed), to convert the words above to dictionary entries (this will take care of proper nouns and odd words)
#this command will add the transcriptions directly to the dictionary file and remove the temp word list
retCode = 0;
if os.path.isfile("grammar_words_temp.txt"):
	if newWordsExist:
		print "transcribing words to phonemes using g2p.py..."
		retCode = os.system("g2p.py --model /usr/local/bin/model-5 --apply " + wordsFile + " >> " + appName + ".dic && rm " + wordsFile);
	else:
		retCode = os.system("rm " + wordsFile);
		sys.exit(0);

if retCode != 0:
	print "Something went wrong while trying to use g2p.py to transcribe words in your grammar to the dictionary. See if g2p.py is installed. If not, try installing it using the SpeakPython INSTALL readme.";
else:
	print "Successfully extended the dictionary with new words."

print "Compilation finished. Happy speaking!"
