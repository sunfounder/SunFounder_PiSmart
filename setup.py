from setuptools import setup, find_packages

from codecs import open
from os import path


def remove_line(tfile,sstr):
    i2c_list = []
    try:
        lines=open(tfile,'r').readlines()
        flen=len(lines)
        for i in range(flen):
            if sstr in lines[i]:
		print i, lines[i]
                i2c_list.append(i)
        for i in range(len(i2c_list)-1, -1, -1):
            print i2c_list[i]
            lines.remove(lines[i2c_list[i]])
        open(tfile,'w').writelines(lines)
        
    except Exception,e:
        print 'remove_line:', e

def add_line(tfile,sstr):
    try:
        lines=open(tfile,'r').readlines()
        lines.append(sstr)
        open(tfile,'w').writelines(lines)
        
    except Exception,e:
        print 'add line:', e

remove_line('/boot/config.txt', 'dtparam=i2c_arm=')
remove_line('/boot/config.txt', 'gpio-poweroff')
add_line('/boot/config.txt', '\ndtparam=i2c_arm=on')
add_line('/boot/config.txt', '\ndtoverlay=gpio-poweroff:gpiopin=13\n')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SunFounder_PiSmart',
   
    version='1.0.0',

    description='Python package for PiSmart from SunFounder',
    long_description=long_description,

    url='https://github.com/sunfounder/SunFouner_PiSmart',

    author='SunFounder',
    author_email='support@sunfounder.com',

    license='GPL',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: GPL License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='RaspberryPi PiSmart setuptools development',

    packages=find_packages(exclude=['example', 'docs', 'tests*', 'offset', 'log']),

    install_requires=['peppercorn'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={
        'pirobot': ['package_data.dat'],
    },

    entry_points={
        'console_scripts': [
            'pismart=pismart:main',
        ],
    },
)

