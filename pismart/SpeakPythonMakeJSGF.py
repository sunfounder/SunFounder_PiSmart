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

import antlr3;
import sqlite3;
import pickle;
import sys, os;
import re;

from pismart.SpeakPythonJSGFLexer import SpeakPythonJSGFLexer;
from pismart.SpeakPythonJSGFParser import SpeakPythonJSGFParser;

def parse(fileList, dirName):

	parser = None;
	tr = [];
	topRules = [];

	for f in fileList:
	
		#join filename with current directory path	
		fileName = os.path.join(dirName, f);

		#if f is a file, parse and extract rules
		if os.path.isfile(fileName):
			char_stream = antlr3.ANTLRFileStream(fileName);
			lexer = SpeakPythonJSGFLexer(char_stream);
			tokens = antlr3.CommonTokenStream(lexer);

#			for t in lexer:
#				print t;

			parser = SpeakPythonJSGFParser(tokens);
			parser.prog();

			if parser.parseFailed:
				print "Parse failed.";
				sys.exit(1);

			#get the list of top-level rules
			tr = parser.rules;

		otherFileParse = ([],"");

		#if f is a dir, pass list of files into recursive call
		if os.path.isdir(fileName):
			subFiles = os.listdir(fileName);
			otherFileParse = parse(subFiles, fileName);

		tr.extend(otherFileParse[0]);

		ruleFileName = re.sub(r"[\.].*", "", fileName);
		ruleFileName = re.sub(r"/;:", "_", ruleFileName);

		#accumulate all alias rules together while using the file path as a prefix so as not to overlap aliases
		aliasText = "";
		for ar in parser.aliasRules:

			#fix the alias references in the expressions to fit the prefixed version to
			alteredExp = re.sub(r"<([^>]+)>", "<" + ruleFileName + r"_\1>", parser.aliasRules[ar]);

			#concat finished alias rule together
			print alteredExp;
			aliasText += "<" + ruleFileName + "_" + ar + "> = " + alteredExp + ";\n";

		aliasText += "\n";

		#prefix alias names of the top-most rules associated with the urrently parsed file
		topRules = []
		for r in tr:
			alteredExp = re.sub(r"<([^>]+)>", "<" + ruleFileName + r"_\1>", r);
			topRules.append( alteredExp );
			
	return (topRules, aliasText + otherFileParse[1]);

def main(argv):	

	name = argv[1] + '.jsgf';

	rules = parse(argv[2:], '');

	ruleCount = 0;
	ruleText = "";
	topRule = "#JSGF V1.0;\ngrammar " + argv[1] + ";\npublic <topRule> = ";

	for rule in rules[0]:

		if ruleCount > 0:
			topRule += " | <rule" + str(ruleCount) + ">";
		else:
			topRule += "<rule" + str(ruleCount) + ">"; 

		ruleText += "<rule" + str(ruleCount) + "> = " + rule + ";\n";
		ruleCount += 1;

	topRule += ";\n\n";

	#concat top rule, all alias rules, and the top-level rules together
	grammarText = topRule + rules[1] + ruleText;

	f = open(name, 'w', 0);
	f.write(grammarText);
	f.close();

main(sys.argv);
