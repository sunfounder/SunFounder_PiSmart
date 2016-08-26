from setuptools import setup, find_packages

from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SunFounder_PiRobot',
   
    version='1.0.0',

    description='Python package for PiRobot from SunFounder',
    long_description=long_description,

    url='https://github.com/sunfounder/SunFouner_PiRobot',

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

    keywords='RaspberryPi PiRobot setuptools development',

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
            'pirobot=pirobot:main',
        ],
    },
)

