#!/usr/bin/python

from __future__ import division
import getopt, sys, re
import ConfigParser, os
import time
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

mh = Adafruit_MotorHAT(addr = 0x60)
 
def main():
    # Initial values
    x = 0 # x axis view angle in deg
    y = 0 # y axis view angle in deg
    o = 10 # minimum frame overlap in % of view angle 
    config = '/opt/owl/etc/owl.conf'
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hx:y:o:c:", ["help",])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for k, a in opts:
        if k == "-v":
            verbose = True
        elif k in ("-h", "--help"):
            usage()
        elif k in ("-x"):
            if re.match('^\d+$', a):
                x = a
            else:
                usage()
            
        elif k in ("-y"):
            if re.match('^\d+$', a):
                y = a
            else:
                usage()
        elif k in ("-o"):
            if re.match('^\d+$', a):
                o = a
            else:
                usage()
        elif k in ("-c"):
            if os.path.isfile(a):
                config = a
            else:
                print 'Given config does not exists'
                usage()
        else:
            assert False, "unhandled option"
 
    if o > 99 :
        print 'X angle is '+str(x)+' Y angle is '+str(y)+' Overlap is '+str(o)
        print 'Overlap greater than 99%!'
        usage()

    # Read config
    config = ConfigParser.RawConfigParser()
    config.read('/opt/owl/etc/owl.conf')
    xsteps = config.getint('motors','xsteps')
    ysteps = config.getint('motors','ysteps')
    xspeed = config.getint('motors','xspeed')
    yspeed = config.getint('motors','yspeed')

    
    # Step - angle transformation
    xStep = config.getfloat('motors','xangle') / config.getint('gears','xratio')
    yStep = config.getfloat('motors','yangle') / config.getint('gears','yratio')
    
    # Stepper motors config
    XStepper = mh.getStepper(xsteps, 1)
    XStepper.setSpeed(xspeed)
    YStepper = mh.getStepper(ysteps, 2)
    YStepper.setSpeed(yspeed)
 
    if x and y:
        print 'X angle is '+str(x)+' Y angle is '+str(y)+' Overlap is '+str(o)
 
        print 'Park on top'
        print 'Take photo'
        YCounter = 0
 
        while YCounter < 360:
            YCounter = YCounter + getYDeg(int(y),o)
            print ''
            print 'Move Y to '+ str(YCounter),
            # Count steps
            YSteps = getYDeg(int(y),o) / yStep
            YStepper.step(int(YSteps), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE) 
            XCounter = 0
            print str(XCounter)+';',
            while XCounter < 360:
                XCounter = XCounter + getXDeg(int(x),o)
                XSteps = getXDeg(int(y),o) / xStep
                XStepper.step(int(XSteps), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE) 
                print str(XCounter)+';',
#                sys.stdout.write(str(XCounter)+';')
#                sys.stdout.flush()
#                print 'Take photo'
                time.sleep(2)
    else:
        usage()
        sys.exit()
 
def usage():
    print 'pano-runer.py -x x-axis-view-angle -y y-axis-view-angle -o frame-overlap-in-percent -c path-to-config'
    sys.exit()
 
def getXDeg(x,o):
    X = x - 2 * o
    return -(-360//X)
 
def getYDeg(y,o):
    Y = y - 2 * o
    return -(-360//Y)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

 
if __name__ == "__main__":
    main()
