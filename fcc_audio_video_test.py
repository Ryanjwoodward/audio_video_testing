#------------------------------------------------------------------------------------------------
# Author       : Ryan Woodward
# Date Created : Aug 15, 2023
#-------------------------------------------------------------------------------------------------

#------------------------------
# IMPORTS
#------------------------------
import time
import asyncio
import subprocess
import os
import io
import gpiod
import signal
import socket
import sys
from typing import *
import keyboard
import cv2
import requests
from datetime import datetime

#------------------------------
#   GLOBAL VARIABLES
#------------------------------
    #!--- VIDEO RELATED VARIABLES ---!#

#? Set up the OpenCV (cv2) object for the video capture device
camera = cv2.VideoCapture(0) #! This Address will need to be changed depending on the system

#? Set the time duration for the video stream
duration = 5

#? Initialize a flag to keep streaming video
keep_streaming = True

    #!--- AUDIO RELATED VARIABLES ---!#
#? Path to the Audio file for the FCC test
audio_file_path = 'beethoven.wav'   #! THis will need to be changed depending on what audio files are available

#? Path & name of the video file to be recorded to
video_file_path = "fcc_recording.avi"

#------------------------------
#   FUNCTIONS
#------------------------------

"""
"""
def fcc_audio_test():
    print("FCC audio testing function")

    subproc = subprocess.Popen(['aplay', audio_file_path])
    subproc.wait()


"""
    This function verifies the presence of a capture device, such as a webcam,
    and attempts to capture an image from it. It prints status messages for
    device verification and image capture. If the device is not available,
    the function releases any resources and returns. If an image is successfully
    captured, it is saved to a file. If image capture fails, an error message
    is printed.
"""
def fcc_image_capture():
    print("Verifying capture device is present...")
    time.sleep(2)

    #? Check if the capture device is present
    if not camera.isOpened():
        print("Camera device is not available.")
        
        #? Release any resources held by the variable or capture device
        camera.release()
        return
    print("Capture Device is present...\n")
    time.sleep(1)

    print("Capturing an Image...")
    time.sleep(2)

    #? Attempt to read an image from the capture device
    result, image = camera.read()

    #? Check if image capture was successful
    if result:
        #? save the captured screenshot
        cv2.imwrite("fcc_test_image.jpg", image)
        print("Successfully captured an image.")
    else:
        print("Image capture failed.")



def fcc_record_video():
    print("Recording video...")
    time.sleep(2)
    

    #? Get the frames per second (fps) of the camera
    fps = camera.get(cv2.CAP_PROP_FPS)

    #? Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file_path, fourcc, fps, (640, 480))  #? Adjust the resolution here
    
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        result, frame = camera.read()
        if result:
            out.write(frame)
        else:
            print("No frame captured. Please try again.")

    print("Video recording stopped and saved.")

"""
    This function performs the FCC video test, capturing and streaming video from a capture device.
    It verifies the presence of the capture device, initiates the video stream, and displays the
    live stream in a window. The stream continues for a specified duration, during which users can
    press the 'q' key to stop the stream. After the test, the capture device is released, and
    OpenCV windows are closed.
"""
def fcc_video_stream_test():

    print("Performing FCC video test...")
    time.sleep(2)

    #? Get the current time as the start time of the test
    start_time = time.time()

    #? Calculate the end time of the test by adding the specified duration
    end_time = start_time + duration

    #? Loop until the end time is reached or the streaming flag is False
    while keep_streaming and time.time() < end_time:
        #? Read a frame from the capture device
        result, image = camera.read()

        #? Check if the frame was successfully read
        if result:
            #? Display the captured frame in a window titled "Camera Stream"
            cv2.imshow("Camera Stream", image)
            
            #? Check if the 'q' key is pressed (to stop streaming)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No image detected. Please try again.")

    #? Release the capture device
    camera.release()

    #? Close all OpenCV windows
    cv2.destroyAllWindows()

    print("Camera stream stopped.")


"""
    Entry point function: Initiates the FCC Audio and Video Test.
    It starts by printing a message indicating the beginning of the test,
    then proceeds to execute the FCC Video Test. Afterward, it informs
    that the audio test won't be performed until connected to the board,
    and finally calls the FCC Audio Test function if needed in the future.
"""
def fcc_start_test():
    print("Beginning FCC Audio and Video Test...")

    #? Use Camera to Capture an Image
    fcc_image_capture()

    #? User Camera to Record a Video
    fcc_record_video()

    #? Use Camera to Stream video to Display
    fcc_video_stream_test()

    #? Start the FCC Audio Test
    print("Won't test audio until connected to the board.")
    fcc_audio_test()

#------------------------------
#   ENTRY POINT CALL
#------------------------------
fcc_start_test()
