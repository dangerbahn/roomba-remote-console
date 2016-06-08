import struct
import sys, glob
import serial
import time

connection = None


class TetheredDriveApp():
    # sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
    def sendCommandASCII(self, command):
        print "send raw..." + command
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        print "sending..." + cmd
        self.sendCommandRaw(cmd)

    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        print "here we go raw"

        try:
            if connection is not None:
                print "writing...." + command
                connection.write(command)
            else:
                print "Not connected."
        except serial.SerialException:
            print "Lost connection"
            connection = None

        print ' '.join([ str(ord(c)) for c in command ])

    # getDecodedBytes returns a n-byte value decoded using a format string.
    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection

        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print "Lost connection"
            connection = None
            return None
        except struct.error:
            print "Got unexpected data from serial port."
            return None

    # get8Unsigned returns an 8-bit unsigned value.
    def get8Unsigned(self):
        return getDecodedBytes(1, "B")

    # get8Signed returns an 8-bit signed value.
    def get8Signed(self):
        return getDecodedBytes(1, "b")

    # get16Unsigned returns a 16-bit unsigned value.
    def get16Unsigned(self):
        return getDecodedBytes(2, ">H")

    # get16Signed returns a 16-bit signed value.
    def get16Signed(self):
        return getDecodedBytes(2, ">h")

    def connect(self):
        global connection
        port = "/dev/ttyUSB0"
        if port is not None:
            print "Trying " + str(port) + "... "
            try:
                connection = serial.Serial(port, baudrate=115200, timeout=1)
                print "Connected!"

            except:
                print "Failed."

if __name__ == "__main__":
    app = TetheredDriveApp()
    app.connect()
    time.sleep(2)
    print "ok...."

    print "Enter Passive"
    self.sendCommandASCII('128')

    time.sleep(2)

    print "Enter Safe"
    self.sendCommandASCII('131')

    time.sleep(2)

    print "BEEP"
    self.sendCommandASCII('140 3 1 64 16 141 3')
