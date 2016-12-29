# Usage Patterns

- follow this usage pattern when using the module
- look at examples for more info, located in speakpython/SpeakPython/examples/
- required files can be found in speakpython/SpeakPython/bin

## For Purely Text-Based Applications

```
#!Python

####################################
#for purely text-based applications#
####################################

# add the following lines to your imports:

from SpeakPython.SpeakPython import SpeakPython
from SpeakPython.Result import Result

sp = SpeakPython("[appName].db");
r = sp.matchResult(input);

if r == None:
	#couldn't match anything
else:
	rStr = r.getResult();

	#now do something with the resulting output string such as:

	#direct execution
	exec rStr;

	#simple output
	print rStr;

	#system control commands
	#(see SpeakPython/examples/LinuxCommands/)

	#parsing output for execution/post-processing
	#(depends on parse)
```

## For Speech Applications

```
#!Python

#####################################
#for speech recognition applications#
#####################################
#taken from the HouseCommands example

from SpeakPython.SpeakPythonRecognizer import SpeakPythonRecognizer

#define callback function with 1 parameter (string)
def execute(s):
        print s;
        #exec s;

#creates recognition instance
#param 1 - function accepting 1 string argument - used as callback
#param 2 - appName - used to read [appName].fsg and [appName].db
recog = SpeakPythonRecognizer(execute, "houseCommands");

# sets the level of debug output
# 1 is the most output, 10 is the least
# default level is 3
#recog.setDebug(1);

#call this to start recognizing speech
#I believe this call utilizes current thread. Please multi-thread it yourself if necessary.
recog.recognize();

```

Take a look at the [SPS file format](https://bitbucket.org/matthew3/speakpython/wiki/The-SPS-File-Format.md) for instructions on creating a file used for recognition.