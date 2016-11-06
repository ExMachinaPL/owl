#!/bin/bash

# Bootstrap scipt version 0.01

# This script will install required packages
# As installation is system wide 
# You'll be asked for sudo password each time its required

echo 'Installing basic system packages'
sudo apt-get update
sudo install git gphoto2 python-dev sense-hat python-configparser python-smbus 

# Add lines to /etc/modules
sudo echo 'i2c-bcm2708' >> /etc/modules
sudo echo 'i2c-dev' >> /etc/modules

sudo echo 'dtparam=i2c1=on' >> /boot/config.txt
sudo echo 'dtparam=i2c_arm=on' >> /boot/config.txt

# Adafruit libraries install
echo 'Installing adafruit libraries'
cd && git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git && cd Adafruit-Motor-HAT-Python-Library && sudo python setup.py install

echo 'Finished!'
