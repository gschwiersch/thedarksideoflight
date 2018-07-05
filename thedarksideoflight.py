#imports
from __future__ import division
from sense_hat import SenseHat
sense = SenseHat()

import datetime
import time
from time import sleep
import picamera
import numpy as np

#LED Matrix Setup
def matrix():
    r=(0,0,255)
    b=(0,0,0)
    picture = [
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        ]

    for i in range(60):
        picture[i] = r
        sleep(.1)
        sense.set_pixels(picture)

# loop to collect data
while True:

    # Capture the image in YUV format
    
    width = 128
    height = 112
    stream = open('image.data', 'w+b')

    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, 'yuv')
        
    #timestamp the data
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Rewind the stream for reading
    stream.seek(0)

    # Calculate the actual image size in the stream (accounting for rounding
    # of the resolution)
    fwidth = (width + 31) // 32 * 32
    fheight = (height + 15) // 16 * 16

    # Load the Y (luminance) data from the stream
    Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))

    #save Y values as a .csv file named after timestamp

    f = open("TheDarkSideOfLight.csv" , "a")
    f.write(time_stamp + ", ")
    f.write("\n")
    for a in range(112):
        for b in range(128):
            f.write(str(Y[a][b]))
            f.write(", ")
        f.write("\n")

    #LED Matrix notification for 1 minute
    matrix()

    
# done #############################
