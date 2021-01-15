import paho.mqtt.client as mqtt
import serial, time, ssl, os

#count1 = 0
topic1 = "dm/test1"
topic2 = "dm/test2"
message_data= "g___d"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def timer_fileCloseOpen():
    global time_fixed, file1, time_mark
    time_mark=int(time.time())
    time_period=time_mark - time_fixed
    if time_period > 70:  #24 hours -86400
        file1.close()
        file1 = open(r'C:\pp-ppd\Python\Log'+time.strftime("%Y-%m-%d")+'\k'+time.strftime("%m.%d-%H.%M.%S")+'.txt', 'w')
        time_fixed = time_mark
       
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.connect("iot.sinai.io", 8883, 60)
client.username_pw_set(username="dm", password="mac-pack-duck")
n=-1
while 1:
    n +=1
    count1 = 0
    time.sleep(2)
    try:
        ser=serial.Serial("COM9", baudrate = 9600, timeout=2)
        print (n,"ok")
        try:
            os.mkdir("C:\pp-ppd\Python\Log"+time.strftime("%Y-%m-%d"))
        except FileExistsError:
            print ("dir exist")    
        finally:
            file1 = open(r'C:\pp-ppd\Python\Log'+time.strftime("%Y-%m-%d")+'\k'+time.strftime("%m.%d-%H.%M.%S")+'.txt','w')
            #client.loop_forever()
            client.loop_start()
            time_fixed=int(time.time())
            time.sleep(6)
            while True:
                try:
                    timer_fileCloseOpen()
                    sms_serial_utf8=((ser.readline()).decode('utf-8')).strip('\n')
                    client.publish(topic1, sms_serial_utf8)
                    print (sms_serial_utf8)
                    fileWriteResume=str(count1)+"<"+str(time_mark)+">:" + sms_serial_utf8 +'\n'
                    file1.write(fileWriteResume)
                except serial.serialutil.SerialException:
                    print (count1,"except error serial off ")
                    break
           
                count1 += 1
                if  count1 == 30000:        
                 break
           
            file1.close()
            client.loop_stop()
            ser.close()
    
    except serial.serialutil.SerialException:
        print (n, "error")
       