#!/usr/bin/env python
import antlr3;
import sqlite3;
import pickle;
import sys, os;
import re;

from pismart.SpeakPython import SpeakPython;
from pismart.SpeakPythonLexer import SpeakPythonLexer;
from pismart.SpeakPythonParser import SpeakPythonParser;

#sort results based on length of labels
def sortResults(results):
	l = len(results);
	if l == 1 or l == 0:
		return results;

	s1 = sortResults(results[:l/2]);
	s2 = sortResults(results[l/2:]);

	res = [];

	si1 = 0;
	si2 = 0;

	sl1 = len(s1);
	sl2 = len(s2);

	max = sl1 + sl2;
	for i in range(0, max):
		if si1 == sl1:
			res.extend(s2[si2:]);
			break;
		if si2 == sl2:
			res.extend(s1[si1:]);
			break;

		if len(s1[si1].labels) > len(s2[si2].labels):
			res.append( s1[si1] );
			si1 += 1;
		else:
			res.append( s2[si2] );
			si2 += 1;

	return res;

def makeDB(conn):
	c = conn.cursor();

	try:
		c.execute("DROP TABLE matches");
		c.execute("DROP TABLE functions");
		c.execute("DROP TABLE kleene")
		conn.commit();
	except Exception as e:
		conn.rollback();

	c.execute("CREATE TABLE matches (order_id INTEGER PRIMARY KEY, keywords TEXT, regex TEXT, results BLOB)");
	c.execute("CREATE TABLE functions (name TEXT, regex TEXT, results BLOB)");
	c.execute("CREATE TABLE kleene (id TEXT PRIMARY KEY, regexes BLOB)");

	#index the keywords to speed up text search
	c.execute("CREATE INDEX IF NOT EXISTS keyword_idx ON matches (keywords)");
	c.execute("CREATE INDEX IF NOT EXISTS func_name_idx ON functions (name)");

	conn.commit();

def performTestCases(exp, testCases):	
	print "Testing: ", exp
	for t in testCases:
		m = re.match(exp, t);
		if m == None:
			print "Test case failed: ", t;
			return False;

	return True;

def insertIntoDB(conn, matches, functions):

	matchEntries = [];
	kleeneEntries = [];
	funcEntries = [];

	print "Running test cases for matches...";

	idCount = 0;

	for m in matches:
		#perform in-suite test cases
		succeededTests = performTestCases(m.exp, m.testCases);

		if not succeededTests:
			return;

		k = ','.join(m.keywords);
		m.results = sortResults(m.results);

		if len(m.kGroupRegexes) > 0:
			kleeneEntries.append((str(idCount), pickle.dumps(m.kGroupRegexes)));
		
		matchEntries.append((idCount, k, m.exp, pickle.dumps(m.results)));

		idCount += 1;

	print "All match test cases passed.";

	c = conn.cursor();

	c.executemany("INSERT INTO matches VALUES (?,?,?,?)", matchEntries);

	conn.commit();

	print "Running test cases for functions...";

	for f in functions:
		f = functions[f];

		#perform in-suite test cases
		succeededTests = performTestCases(f, f.testCases);

		if not succeededTests:
			return;

		#save all regex groups in database under function name
		if len(f.kGroupRegexes) > 0:
			kleeneEntries.append((f.getName(), pickle.dumps(f.kGroupRegexes)));

		f.results = sortResults(f.results);
		funcEntries.append((f.getName(), f.getExp(), pickle.dumps(f.getResults())));

	print "All function test cases passed";

	c.executemany("INSERT INTO functions VALUES (?,?,?)", funcEntries);
	c.executemany("INSERT INTO kleene VALUES (?,?)", kleeneEntries);
	
	conn.commit();

	print "Functions:";
	for row in c.execute("SELECT * FROM functions"):
		print row, '\n';
	print "\n";

	print "Matches:";
	for row in c.execute("SELECT * FROM matches"):
		print row, '\n';
	print "\n";

	print "Kleene:";
	for row in c.execute("SELECT * FROM kleene"):
		print row, '\n';
	print "\n";

	conn.close();

def parse(conn, fileList, dirName):

	parser = None;
	otherGlobalTests = {};

	for f in fileList:
	
		#join filename with current directory path	
		fileName = os.path.join(dirName, f);

		#if f is a file, parse and insert into db
		if os.path.isfile(fileName):

			char_stream = antlr3.ANTLRFileStream(fileName);
			lexer = SpeakPythonLexer(char_stream);
			tokens = antlr3.CommonTokenStream(lexer);

#			for t in lexer:
#				print t;

			parser = SpeakPythonParser(tokens);
			parser.prog();

			insertIntoDB(conn, parser.matches, parser.aliases);

		#if f is a dir, pass list of files into recursive call
		if os.path.isdir(fileName):
			subFiles = os.listdir(fileName);
			otherGlobalTests = parse(conn, subFiles, fileName);

	globalTests = {};

	if parser == None:
		print "Parser not defined."
	else:
		globalTests = parser.globalTests;

	globalTests.update(otherGlobalTests);

	return globalTests;

def main(argv):	

	name = argv[1] + '.db';

	conn = sqlite3.connect(name);

	makeDB(conn);

	globalTests = parse(conn, [argv[2]], '');

	for gt in globalTests:
		sp = SpeakPython(name);
		r = sp.matchResult(gt);

		resultStr = '';
		if r != None:
			resultStr = r.getResult();

		if resultStr != globalTests[gt]:
			print "Value test case failed: (" + gt + ") does not return (" + globalTests[gt] + "), but instead returns (" + resultStr + ")";

main(sys.argv);
