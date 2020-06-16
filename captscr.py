import pyautogui
import threading
import datetime

import ftplib
import os

def SendFile(filename):
    try:
        ftp=ftplib.FTP()
        ftp.connect("211.201.135.90",2121)
        ftp.login("paul","djemals!")
        ftp.cwd("./")
        os.chdir(r"D:\movie\screen")
        myfile = open(filename,'rb')
        ftp.storbinary('STOR ' +filename, myfile )
        myfile.close()
        ftp.close
    except:
        pass

def CaptureScreen():
    time = datetime.datetime.now()
    timestr = time.strftime('%m%d_%H%M')
    filename = f"scr_{timestr}.jpg"
    try:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(f'D:\movie\screen\{filename}')
        SendFile(filename)
    except:
        pass
    
    threading.Timer(60, CaptureScreen).start()
   
CaptureScreen()
#print ("End")
