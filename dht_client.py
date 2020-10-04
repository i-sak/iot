import time
import board
import adafruit_dht
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4,GPIO.IN)
GPIO.setup(18,GPIO.IN)
print(GPIO.input(4))
print(GPIO.input(18))
# Initial the dht device, with data pin connected to:
if ((GPIO.input(4)==1)):
    print("#")
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    temp_url = "http://192.168.0.4:8080/insertTemp"
    while True:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            if (temperature >=18) and (humidity >=40):
                print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
                
                params = {'temp':temperature, 'hum': humidity, 'time':time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}
                
                requests.post(url=temp_url, data=params, timeout=10)
            else:
                print("메인 센서 고장")
                pass
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            print("메인 센서 고장")
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
    temp_url = "http://192.168.0.4:8080/insertTemp"

    while True:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
            
            params = {'temp':temperature, 'hum': humidity, 'time':time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}
            
            requests.post(url=temp_url, data=params, timeout=10)
            
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            print("메인 센서 고장")
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
        
# dhtDevice = adafruit_dht.DHT22(board.D18, use_purseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)     
