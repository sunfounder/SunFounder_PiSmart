#!/usr/bash
#Installation

##Tested on:

#- Raspbian (RaspberryPi - think of those possibilities)

#```

# All of these commands are run from the base folder (SunFounder_PiRobot), wherever you clone it to

if [ "$(whoami)" != "root" ] ; then
	echo "You must run setup.sh as root."
	exit
fi

sudo apt-get update
sudo apt-get upgrade -y

###################################
# install espeak festival pico runtime #
###################################
    echo "Installinging \n espeak \n festival \n libttspico-utils \n tts-engine"
    if sudo apt-get install espeak festival libttspico-utils -y; then
    	echo "Successfully installed espeak festival pico"
    else
    	echo "Failed to installed espeak festival pico"
    	exit
    fi

###################################
# install pocketsphinx i2c-tools python-smbus runtime #
###################################
    echo "Installinging \n pocketsphinx \n i2c-tools \n python-smbus"
    if sudo apt-get install pocketsphinx i2c-tools python-smbus -y; then
    	echo "Successfully installed pocketsphinx i2c-tools python-smbus"
    else
    	echo "Failed to installed pocketsphinx i2c-tools python-smbus"
    	exit
    fi

###################################
# install antlr3.4 python runtime #
###################################
	
	cd dependencies
	if tar -xf antlr-3.4.tar.gz && \
		cd antlr-3.4/runtime/Python && \
		sudo python setup.py install; then
		echo "Successfully installed antlr3.4 runtime."
	else
		echo "Failed to install antlr3.4 runtime."
		exit
	fi
	cd ../../..		# dependence

#NOTE: You can stop here if you don't care about speech recognition support and just desire usage of the text-based capabilities of SpeakPython

####################
# install GStreamer#
####################

# Install GStreamer using:
	echo "Installing gstreamer dependencies..."
	if sudo apt-get install python-gst0.10 gstreamer-0.10 \
            gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly -y; then
		echo "Successfully installed gstreamer and python gst."
	else
		echo "Failed to install gstreamer and python gst."
		exit
	fi

    if sudo apt-get install gstreamer0.10-pocketsphinx -y; then
		echo "Successfully installed gstreamer pocketsphinx plugin."
	else
		echo "Failed to install gstreamer pocketsphinx plugin."
		exit
	fi

#needed for ./configure in next step
    if sudo apt-get install bison -y; then
		echo "Successfully installed bison."
	else
		echo "Failed to install bison."
		exit
	fi

#needed for make
        if sudo apt-get install make -y; then
		echo "Successfully installed make."
	else
		echo "Failed to install make."
		exit
	fi
        if sudo apt-get install python-dev -y; then
		echo "Successfully installed python-dev."
	else
		echo "Failed to install python-dev."
		exit
	fi
        if sudo apt-get install swig -y; then
		echo "Successfully installed swig."
	else
		echo "Failed to install swig."
		exit
	fi

######################
# install sphinxbase #
######################
	if tar -xf sphinxbase-5prealpha.tar.gz && \
		cd sphinxbase-5prealpha && \
		./configure && \
		make clean && \
		make && \
		sudo make install && \
		cd .. ; then

		echo "Successfully installed sphinxbase."
	else
		echo "Failed to install sphinxbase."
		exit
	fi
		
########################
# install pocketsphinx #
########################
	if tar -xf pocketsphinx-5prealpha.tar.gz && \
		cd pocketsphinx-5prealpha && \
		./configure && \
		make clean && \
		make && \
		sudo make install && \
		cd .. ; then
	
		echo "Successfully installed pocketsphinx."
	else
		echo "Failed to install pocketsphinx."
		exit
	fi

# Install pocketsphinx for Python
	if sudo apt-get install python-pocketsphinx -y; then
		echo "Successfully installed pocketsphinx."
	else
    ##OR
		echo 'Trying to install pocketsphinx using pip instead...'
        	sudo apt-get install python-pip -y
        	sudo pip install pocketsphinx 
	fi

# Configure shared library paths
	echo 'Exporting library paths...'
	export LD_LIBRARY_PATH=/usr/local/lib
	export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

    export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-0.10

# Make sure there's a pocketsphinx configuration (should output a folder called 'model')
#	ls /usr/share/pocketsphinx/

# If this folder exists, we can replace it with the command below
#this will replace the existing model with one trained with suitable data for our application
# wsj1 is by default the ptm version of cmu-us-en-5.2, utilize untar and use the non-ptm version for slower, more resource-intensive, and accurate recognition
	if tar -xf wsj1.tar.gz && \
		sudo cp -r wsj1 /usr/share/pocketsphinx/model/hmm/ ; then
		echo "Successfully copied pocketsphinx model."
	else
		echo "Failed to copy pocketsphinx model."
	fi
#```

#Install g2p.py for word to phoneme conversion (optional)
	if tar -xf Sequitur-g2p.tar.gz && \
		cd Sequitur-g2p/g2p && \
		sudo python setup.py install --prefix /usr/local && \
		cd .. ; then
		echo "Successfully installed Sequitur-g2p (g2p.py)"
	else
		echo "Failed to install Sequitur-g2p (g2p.py)"
	fi
	cd ..  # dependencies
		sudo rm -rf antlr-3.4 wsj1  Sequitur-g2p sphinxbase-5prealpha pocketsphinx-5prealpha 
		echo 'remove antlr-3.4 wsj1 Sequitur-g2p sphinxbase-5prealpha pocketsphinx-5prealpha'
	
#speakpython dictionary 
	cd /home/pi/SunFounder_PiRobot
	chmod +x ./pirobot/MakeSpeechProject.py
    chmod +x ./pirobot/SpeakPythonMakeDB.py
    chmod +x ./pirobot/SpeakPythonMakeJSGF.py
    sudo cp ./pirobot/MakeSpeechProject.py /usr/local/bin
    sudo cp ./pirobot/SpeakPythonMakeDB.py /usr/local/bin
    sudo cp ./pirobot/SpeakPythonMakeJSGF.py /usr/local/bin
    sudo cp ./pirobot/model-5 /usr/local/bin
    sudo cp ./pirobot/pocketsphinx.dic /usr/local/bin
	sudo cp /usr/local/lib/libsphinxbase.so.3 /usr/lib
	echo 'cp files success'

	echo 'all done, enjoy it'
# Usage

#- Stick MakeSpeechProject.py, SpeakPython (whole folder), SpeakPythonMakeDB.py inside of the project where your main python application rests.

#```
#	cp speakpython/SpeakPython/bin/* [my project directory]
#```

#- run 'python MakeSpeechProject.py [appName] [sps file name]' to generate your speech application database
#- An example is 'python MakeSpeechProject.py calc calc.sps' for the calculator app
#- Theoretically a folder can be used in place of calc.sps (untested)

#Congrats! If everything is typed and set up correctly, your speech application should be working.

#Take a look at the [Usage Patterns](https://bitbucket.org/matthew3/speakpython/wiki/Usage%20Patterns) of SpeakPython. It's really easy!

#Take a look at the [SPS file format](https://bitbucket.org/matthew3/speakpython/wiki/The%20SPS%20File%20Format) for instructions on creating a file used for recognition.
