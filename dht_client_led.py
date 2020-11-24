import time
import board
import adafruit_dht
import requests
import RPi.GPIO as GPIO

pins = (10, 9, 11) #19, 21, 23 (25)

GPIO.setmode(GPIO.BCM)

def led (pins, color, t):
    RGBs = (
        (1,0,0), #R
        (0,1,0), #G
        (0,0,1), #B
        )

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)
    GPIO.setup(pins[2], GPIO.OUT)

    GPIO.output(pins[0], RGBs[color][0])
    GPIO.output(pins[1], RGBs[color][1])
    GPIO.output(pins[2], RGBs[color][2])

    time.sleep(t)

    GPIO.cleanup(pins)

GPIO.setup(4,GPIO.IN)
GPIO.setup(18,GPIO.IN)
sig1 = GPIO.input(4) #main sensor #pin 2, 6, (7)
sig2 = GPIO.input(18) #sub sensor  #pin 4, 9, (12)
print(sig1, sig2)
# Initial the dht device, with data pin connected to:
if ((GPIO.input(4)==1)):
    #print("#")
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    temp_url = "http://122.43.56.49:8080/insertTemp"
    while True:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            if (40>= temperature >=0) and (80>= humidity >=0):
                print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
                
                if temperature >= 30:
                    led(pins, 0, 5)
                elif temperature >= 20:
                    led(pins, 1, 5)
                elif temperature:
                    led(pins, 2, 5)
                    
                params = {'temp':temperature, 'hum': humidity, 'time':'20201029', 'sig1' : sig1, 'sig2' : sig2}#time.strftime('%Y %m %d %H %M %S')
                
                requests.post(url=temp_url, data=params, timeout=10)
                
                    
            else:
                print("Main Sensor is broken 1")
                params = {'temp':temperature, 'hum': humidity, 'time':'20201029', 'sig1' : 0, 'sig2' : sig2}#time.strftime('%Y %m %d %H %M %S')
                
                requests.post(url=temp_url, data=params, timeout=10)
                pass 
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            #print(error.args[0])
            #print("Main Sensor is broken")
            pass
            time.sleep(5.0)
        
        #except Exception as error: #EXIT
            #dhtDevice.exit()
            #pass
        
        except requests.exceptions.Timeout:
            print('http post Timeout')
            pass

        time.sleep(5.0)
        
if(GPIO.input(18)==1):
    
    print("Main Sensor is broken 2")
    dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
    temp_url = "http://122.43.56.49:8080/insertTemp"

    while True:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
            
            if temperature >= 30:
                led(pins, 0, 1)
            elif temperature >= 20:
                led(pins, 1, 1)
            elif temperature:
                led(pins, 2, 1)
            
            params = {'temp':temperature, 'hum': humidity, 'time':'20201029', 'sig1' : sig1, 'sig2' : sig2}
            
            requests.post(url=temp_url, data=params, timeout=10)
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            #print(error.args[0])
            print("Main Sensor is broken 3")
            pass
            time.sleep(5.0)
        
        #except Exception as error: #EXIT
            #dhtDevice.exit()
            #pass
        
        except requests.exceptions.Timeout:
            print('http post Timeout')
            pass

        time.sleep(5.0)
        
else:
    print("Device is broken")
