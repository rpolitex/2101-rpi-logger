import paho.mqtt.client as mqtt
#from serial import serial
import serial, time, ssl


count_log = 0
#count_break = 0
topic1 = "dm/test1"
topic2 = "dm/test2"
message_data= "g___d"
time_fixed=int(time.time())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def timer_fileCloseOpen():
    global time_fixed, file1, time_mark, count_log
    time_mark=int(time.time())
    time_period=time_mark - time_fixed
    if time_period > 86400:  #24 hours->86400 sec; 1hour->3600 sec
        file1.close()
        file1 = open(r'/home/pi/pp_ppd/log_txt_serial/dm_'+(time.strftime("%m%d%H%M"))+'.txt', 'w')
        time_fixed = time_mark
        count_log = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.connect("iot.sinai.io", 8883, 60)
client.username_pw_set(username="dm", password="mac-pack-duck")

ser = serial.Serial('/dev/ttyUSB0', baudrate = 921600, timeout=2)
file1 = open(r'/home/pi/pp_ppd/log_txt_serial/dm_'+(time.strftime("%m%d%H%M"))+'.txt', 'w')

#client.loop_forever()
client.loop_start()
time.sleep(6)
while True:
    timer_fileCloseOpen()
    message_serial= ser.readline()
    if (message_serial != ('').encode('utf-8')):
        #sms_serial_utf8= ser.readline().decode('utf-8').strip('\n')
        client.publish(topic1, message_serial)
        #client.publish(topic1, sms_serial_utf8)

        #print (message_serial)
        #print ('utf8=', sms_serial_utf8)
        #print (ser.readline())
        #print (str(message_serial))

        #fileWriteResume=str(count_log)+"<"+str(time_mark)+">:"+sms_serial_utf8+'\n'
        fileWriteResume=str(count_log)+"<"+str(time_mark)+">:"+str(message_serial)+'\n'
        file1.write(fileWriteResume)
        print (fileWriteResume)
        count_log += 1

    """count_break +=1
    if  count_break == 86400:
        break
    print (count_break)"""

file1.close()
client.loop_stop()
ser.close()