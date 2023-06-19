from picamera import PiCamera
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import midjourney as mj
import bot_settings as bset

# sudo apt-get install python3-dev python3-rpi.gpio
# pip install RPi.GPIO

def button_callback(channel):
    if (bset.get_ignorebutton()):
        return
    
    bset.set_ignorebutton(True)
    print('Button was pushed!')
    take_photo()
    if GPIO.input(8) == GPIO.HIGH:
        print('Switch on')
        bset.set_promptprefix('Anime')
    else:
        print('Switch off')
        bset.set_promptprefix('')


def take_photo():
    file_prefix = time.strftime('%Y%m%d_%H%M%S')
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera_file = f'/home/simon/git/midjourney-bot/camera/{file_prefix}_photo.jpg'
    camera.capture(camera_file)
    camera.close()   

    if bset.get_automode():
        mj.go_describe(camera_file)

def setup_gpio():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

    # Set pins to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Setup event on pin 10 rising edge
    GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback, bouncetime=3000) 
