import paho.mqtt.client as mqtt
import serial, time, ssl, os


topic1 = "dm/log1"
topic2 = "dm/error1"
message_data= "g___d"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def timer_fileCloseOpen():
    global time_fixed, file1, time_mark
    time_mark=int(time.time())
    time_period=time_mark - time_fixed
    if time_period > 86400:  #24hours-> 86400  1hour-> 3600
        file1.close()
        file1 = open(r'/home/pi/pp_ppd/log_txt_serial/Log'+time.strftime("%Y-%m-%d")+
                     '/k'+time.strftime("%m.%d-%H.%M.%S")+'.txt', 'w')
        time_fixed = time_mark
       
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.connect("iot.sinai.io", 8883, 60)
client.username_pw_set(username="dm", password="mac-pack-duck")

while 1:
    count1 = 0
    time.sleep(2)
    try:
        ser=serial.Serial("/dev/ttyUSB0", baudrate = 921600, timeout=2)
        print ("ok")
        client.publish(topic2, "serial port ok")
        try:
            os.mkdir("/home/pi/pp_ppd/log_txt_serial/Log"+time.strftime("%Y-%m-%d"))
        except FileExistsError:
            print ("dir exist")    
        finally:    
            file1 = open(r'/home/pi/pp_ppd/log_txt_serial/Log'+time.strftime("%Y-%m-%d")+
                         '/k'+time.strftime("%m.%d-%H.%M.%S")+'.txt', 'w')
            #client.loop_forever()
            client.loop_start()
            time_fixed=int(time.time())
            time.sleep(6)
            while True:
                try:
                    timer_fileCloseOpen()
                    #mes= ser.readline()
                    #if (mes != ("").encode('utf-8')):
                    sms_serial_utf8=((ser.readline()).decode('utf-8')).strip('\n')
                    if (sms_serial_utf8 != ""): #.encode('utf-8')):
                        client.publish(topic1, sms_serial_utf8)
                        print (sms_serial_utf8)
                        #print (mes)
                        fileWriteResume=str(count1)+"<"+str(time_mark)+">:" + sms_serial_utf8 +'\n'
                        file1.write(fileWriteResume)
                        count1 += 1
                except (serial.serialutil.SerialException):
                    print (count1,"except error serial off ")
                    client.publish(topic2, "except error serial off ")
                    break
                except (UnicodeDecodeError):
                    print ("error UnicodeDecodeError")
                    client.publish(topic2, "error UnicodeDecodeError")  
                           
            file1.close()
            client.loop_stop()
            ser.close()
    
    except serial.serialutil.SerialException:
        print ("error serial port")
        client.publish(topic2, "error serial port")  