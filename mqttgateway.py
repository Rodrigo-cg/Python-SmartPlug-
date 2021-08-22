  
import paho.mqtt.client as mqttClient
import binascii
import time
  
def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")
  
def on_message(client, userdata, message):
    hex_bytes = binascii.hexlify(bytes(message.payload))
    receive=bytes(message.payload)
    header = receive[0] & 0xFF
    if header == 0x21:
        
        print(header)
        length = receive[1] & 0xFF;
        id=receive[2:(2 + length)]
        deviceBytes=receive[(3 + length):len(receive)]
        deviceLength = deviceBytes[0] & 0xff
        mac =deviceBytes[1:7].hex()
        print("mac es:"+str(mac))
        rssi = deviceBytes[7]
        print("rssi es:"+str(rssi))
        dataLength = deviceBytes[8] & 0xff
        print("datalength es:"+str(dataLength))
        rawData=deviceBytes[9:(9+dataLength)].hex()
        print("raw data es:"+str(rawData))
        result = str(rawData).find('ffff')
        result=result+4
            

        
        nameLength = deviceLength - 8 - dataLength
        if nameLength > 0:
            name =deviceBytes[(9+dataLength):(9+dataLength+nameLength)].hex()
            bytes_object = bytes.fromhex(name)
            ascii_string = bytes_object.decode("ASCII")
            print("nombre dispositivo es "+str(ascii_string))
            voltaje=rawData[result+6:result+10]
            corriente=rawData[result+10:result+16]
            power=rawData[result+16:result+20]
            energy=rawData[result+20:result+26]
            voltajeint=int(voltaje, 16)*0.1
            corrienteint=int(corriente, 16)*1.0
            powerint=int(power, 16)*0.1
            energyint=int(energy, 16)/100
            
            print(" voltaje:"+str(voltajeint)+ " v")
            print(" corriente:"+str(corrienteint)+" mA")
            print(" potencia:"+str(powerint)+" W")
            print(" energia:"+str(energyint)+" j")
        
            
        
  #      for i in range(len(receive)):
  #          if i<len(receive):
  #              deviceLength = deviceBytes[i] & 0xff;
  #              i=i+1
            
            
        
    print(hex_bytes)
  
Connected = False   #global variable for the state of the connection
  
broker_address= "www.mqtt-dashboard.com"  #Broker address
port = 1883                         #Broker port
         #Connection password
  
client = mqttClient.Client()               #create new instance
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("sub_g_topic")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print( "exiting")
    client.disconnect()
    client.loop_stop()
