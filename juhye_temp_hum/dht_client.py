import time
import board
import adafruit_dht
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4,GPIO.IN)
GPIO.setup(18,GPIO.IN)
sig1 = GPIO.input(4) #메인센서 전원여부 #pin 2, 6, (7)
sig2 = GPIO.input(18) # 서브센서 전원여부 #pin 4, 9, (12)
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
            if (40>= temperature >=18) and (80>= humidity >=30):
                print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
                
                params = {'temp':temperature, 'hum': humidity, 'time':'20201029', 'sig1' : sig1, 'sig2' : sig2}#time.strftime('%Y %m %d %H %M %S')
                
                requests.post(url=temp_url, data=params, timeout=10)
            else:
                print("메인 센서 고장")
                pass 
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            #print(error.args[0])
            print("메인 센서 고장")
            pass
            time.sleep(2.0)
            break
        
        except Exception as error:
            dhtDevice.exit()
            pass
        
        except requests.exceptions.Timeout:
            print('http post Timeout')
            pass

        time.sleep(3.0)
if(GPIO.input(18)==1):
    
    print("메인 센서 고장")
    dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
    temp_url = "http://122.43.56.49:8080/insertTemp"

    while True:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
            
            params = {'temp':temperature, 'hum': humidity, 'time':'20201029', 'sig1' : sig1, 'sig2' : sig2}
            
            requests.post(url=temp_url, data=params, timeout=10)
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            #print(error.args[0])
            print("메인 센서 고장")
            pass
            time.sleep(2.0)
            break
        
        except Exception as error:
            dhtDevice.exit()
            pass
        
        except requests.exceptions.Timeout:
            print('http post Timeout')
            pass

        time.sleep(3.0)
else:
    print("기기 고장")
        