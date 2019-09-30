# Lighthub Server
A micropython based server that drives a LED and is controllable over a REST API / Android App  

Android App: https://github.com/manuel2258/lighthub_client  

## Requirements:

* A Micropython compatible ESP8266 microcontroller (tested on a WEMOS D1 MINI, other variants might require a bit of rewriting)
* A WS2811/2/2B compatible LED Chain
* 5V Powersupply (at least 1A, depends on the amount of LEDs)
* [A case](https://www.thingiverse.com/thing:3866419)
* A simple reset button
* (A 3.3V-5V Level Shifter, if your microcontroller outputs 3.3V and the LED wants 5V)
* (A light defusing filter, to spread the LEDs light)
* (Preferable a Linux machine, otherwise you might have to find working tools for your OS to flash the firmware)

## Installation:

### Requirements:

* [Ampy](https://github.com/pycampers/ampy) to flash the code 
* [Esptool](https://github.com/espressif/esptool) to flash the firmware
* ([Picocom](https://github.com/npat-efault/picocom) to debug if something is not working)

### Flash the firmware:

In depth tutorial for a ESP8266 can be found here: http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro  
You can download the ESP8266 micropython firmware here: http://micropython.org/download#esp8266  

To begin erease the flash
> esptool.py --port /dev/ttyUSB0 erase_flash

And then deploy the firmware
> esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 [PATH/TO/THE/FIRMWARE/OF/OUR/BOARD]

Now your board should have the micropython firmware installed and is ready to flash the real code

### Flash the code:

To make ampy nicer to work with we firstly set its port variable
> export AMPY_PORT="/dev/ttyUSB0"

You might have to replace /dev/ttyUSB0. A fast way to find the name is to unplug it, execute `ls /dev/ttyUSB*`, then plug it in, execute it again and check for new devices.  
Then we can check if eveything worked by
> ampy ls

Now we can start to flash the code, for that we have to put every single .py file onto the board  

> ampy put boot.py  
> ampy put main.py

At least we can also put entire folders and its content there
> ampy put ./src/ /src/  
> ampy put ./configs/ /configs/

After that the code should be flashed onto the board and be ready to go.

### Setup:

Install the Android App. Then check for available wifi networks and you should see a network with the name lighthub. Connect to it. 
Once you are connected, disable your mobile connection, open the app and click the setup button.  
Then choose your home wifi network and enter its password and send it.  
WARNING: Doing so will send your wifi credentials in plain text to the microcontroller!  
  
Now the controller should reboot and can connect to your home network again. (Don't forget to turn on mobile data)  
Click on the change button and the app will scan your entire subnet for lighthubs.  
After the scan is complete you can click on change and you can set the color and times as you wish. 

### Wiring:
![Circuit](https://i.ibb.co/B6DQpx0/circuit.png)
You might have to use others signal pins. If you do so don't forget to also change them in the code (main.py).  

And now we should be done! Simply place it into a case that you like and have fun with it!
If anything is not working / was unclear feel free to create a issue or contact me directly!
