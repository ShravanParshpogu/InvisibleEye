import RPi.GPIO as GPIO
import time
import gpiozero
import smtplib
import twilio
import telebot

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from picamera import PiCamera
from time import sleep
from twilio.rest import Client

bot_token='752515795:AAGrtBNTk35YNYFG16fFjsaWgREiPSlCCKo'
bot=telebot.TeleBot(token=bot_token)





account_sid = 'AC35021f1802a2f6d6cf102b7cd8ddd8c3'
auth_token = '6426dd111abdb7b702cdb4f6e118aac7'
client = Client(account_sid, auth_token)


camera = PiCamera()
GPIO.setmode(GPIO.BCM)

email_user = 'shravancs2014@gmail.com'
email_password = ******
email_send = 'sravanparsh@gmail.com'
subject='Intruder Information'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

header='To: ' + email_send +'\n' + 'From:'+ email_user+'\n' +'Subject: '+ subject
body='Indtruder in Your Home'
msg.attach(MIMEText(body,'plain'))


#print(header + body)


GPIO.setup(4,GPIO.IN) #pir
GPIO.setup(24,GPIO.OUT) #pir
try:
    time.sleep(5)

    while True:
            i=GPIO.input(4)
            
            if i==0:
                    GPIO.output(24,False)
                    print("motion NOT detected")
                    time.sleep(0.5)#Buzzer turn on for 1secs
            elif i==1:                                               
                        print("Intruder DETECTED")
                        camera.start_preview()
                        sleep(10)
                        camera.capture('/home/pi/Desktop/image.jpg')
                        camera.stop_preview()
                        
                        camera.start_preview()
                        camera.start_recording('/home/pi/Desktop/video.h264')
                        sleep(10)
                        camera.stop_preview()
                        
                        
                        filename='/home/pi/Desktop/video.h264'
                        attachment =open(filename,'rb')                        
                                                
                        part = MIMEBase('application','octet-stream')
                        part.set_payload((attachment).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition',"attachment; filename= "+filename)
                        msg.attach(part)
                        text = msg.as_string()
                        
                        server = smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        server.login(email_user,email_password)
                        server.sendmail(email_user,email_send,text)
                        server.quit()

                        message = client.messages \
                .create(
                     body="You have an intruder",
                     from_='+12044000347',
                     to='+18073566578'
                 )
                        
                        print(message.sid)

                        @bot.message_handler(commands=['start'])
                        def send_welcome(message):
                            bot.reply_to(message,'welcome')
                            GPIO.output(24,True)
                            time.sleep(3)
                            GPIO.output(24,False)                                               
                                                    
                                                                                    
                                               
                        time.sleep(0.5)
                        bot.polling()
except:
        GPIO.cleanup()


