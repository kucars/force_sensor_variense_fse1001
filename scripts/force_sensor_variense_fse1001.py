#!/usr/bin/env python
import time
import binascii
import serial
import struct
import rospy
from std_msgs.msg import Float32

portName = '/dev/ttyACM0'

def ForceSensor():
    pub = rospy.Publisher('/force_values', Float32, queue_size=100)
    serialPort = serial.Serial(
        port=portName,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = None
    )
    rospy.init_node('force_sensor', anonymous=True)
    rate = rospy.Rate(1000) # 1000
    while not rospy.is_shutdown():    
        binaryIn = serialPort.read()
        hexaIn   =  binascii.hexlify(binaryIn).decode('utf-8')
        print "FirstRead:", hexaIn
        while hexaIn != '0d':
            binaryIn = serialPort.read()
            hexaIn   = binascii.hexlify(binaryIn).decode('utf-8')
        # message size
        binaryIn    = serialPort.read()
        messageSize = binascii.hexlify(binaryIn).decode('utf-8')    
        print "Message Size:", messageSize," mSize:",struct.unpack('B', binaryIn)[0]

        # message type
        binaryIn    = serialPort.read()
        messageType = binascii.hexlify(binaryIn).decode('utf-8')
        print "Message Type:", messageType
        if messageType!= '66':
            print "Incorrent message type"
            serialPort.write('F')
            serialPort.write('z')
            continue
        else:
            print "Message type is correct"
        # timestamp 
        binaryIn         = serialPort.read(4)
        timeStamp        = struct.unpack('I', binaryIn)[0]
        timeStampSwapped = struct.unpack("<I", struct.pack(">I", timeStamp))[0]
        print "Time Stamp:",timeStamp," swapped:",timeStampSwapped

        # timestamp 
        binaryIn    = serialPort.read(4)
        forceValue  = struct.unpack('<f', binaryIn)[0]
        forceValueSwapped = struct.unpack("<f", struct.pack(">f", forceValue))[0]
        print "Force:",forceValue," swapped:",forceValueSwapped

        binaryIn = serialPort.read()
        hexaIn   = binascii.hexlify(binaryIn).decode('utf-8')

        if hexaIn == 'ff':
            print "End Detected"
        else:
            print "Incorrect message"
        
        pub.publish(forceValueSwapped)
        rate.sleep()

if __name__ == '__main__':
    try:
        ForceSensor()
    except rospy.ROSInterruptException:
        pass