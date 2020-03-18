## Note: multiple commented lines have been added by KUYDIGITAL

import snowboydecoder
import sys
import signal

## import os

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)

detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)


###############################################################################
## Here's a sample on how to add your own callbacks by using os.system
## callbacks = [lambda: os.system("espeak -v m1 -g 5 'Yes sir!'") & os.system("python3 /home/pi/servos/pivot-1.py"),
##              lambda: os.system("espeak -v m1 -g 5 'Yes sir!'") & os.system("mplayer /home/pi/Music/*.flac")]

## Note: You can add mulitple os.system commands by using "&". Each callback is separated by ","

## Usage: pi@raspberrypi:~ $ python snowboy_demo2.py model1.pmdl model2.pmdl
## Note on usage: When you list your models, they should match the order of your callbacks
###############################################################################


callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
