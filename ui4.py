from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import base64
from nltk.corpus import wordnet
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter.filedialog import *
import wikipedia
import wolframalpha
import os
import subprocess
import re, string
import speech_recognition as sr
from gtts import gTTS
import notify2
import webbrowser
import time
import math
import datetime
from pymongo import MongoClient
from crontab import CronTab
from subprocess import *
#import keys
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose', 'https://mail.google.com/']
w1 = ''
entries = []
name = ''

def speak(input):
    tts = gTTS(text=input, lang='en')
    tts.save("good.mp3")
    os.system("mpg123 good.mp3")
    
def notification(title, message, icon):
    notify2.init("Basic")
    n = notify2.Notification(title, message, icon)
    n.show()
            
def askfilename():
    filename = askopenfilename(initialdir = "/home")
    entry2.delete(0, 'end')
    entry1.insert(0, filename + ';')
    
def makeform2(w1):
    entries = []
    global entry1
    row = Frame(w1)
    lab = Label(row, width=8, text='To', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('to', ent))
    row = Frame(w1)
    lab = Label(row, width=8, text='Subject', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('subject', ent))
    row = Frame(w1)
    lab = Label(row, width=8, text='Message', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=TOP)
    ent.pack(side=BOTTOM, expand=YES, fill=X)
    entries.append(('body', ent))
    row = Frame(w1)
    lab = Label(row, width=5, text='File', anchor='w')
    entry1 = Entry(row)
    b1 = Button(row, text='Browse', fg='green', bg='white', command=askfilename)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    b1.pack(side=RIGHT, padx=5, pady=5)
    entry1.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('file', ent))
    return entries

def fetch2(entries):
    global w1
    try:
        toaddr = entries[0][1].get()
        toaddr1 = toaddr.split(';')
        msg = MIMEMultipart()
        msg['from'] = 'me'
        msg['To'] = ', '.join(toaddr1)
        msg['Subject'] = entries[1][1].get()
        body = entries[2][1].get()
        msg.attach(MIMEText(body))
        filename = entry1.get()
        if (body == '' and filename == ''):
            showerror("Error", "Please enter a message!!!")
        else:
            filename1 = filename.split(';')
            filename1.remove('')
            for f in filename1:
                attachment = MIMEApplication(open(f, "rb").read(), _subtype="txt")
                attachment.add_header('Content-Disposition','attachment', filename=f)
                msg.attach(attachment)
            raw_message = base64.urlsafe_b64encode(msg.as_string().encode("utf-8"))
            message1 = {'raw': raw_message.decode("utf-8")}
            try:
                message = service.users().messages().send(userId='me', body=message1).execute()
                notification("Mail", "Mail sent successfully!!!",'/home/vinay/Downloads/mail.png')
                w1.withdraw()

            except Exception as e:
                print(e)
                showerror("Error", "Unable to send!!!")

    except Exception as e:
        print(e)
        showerror("Error", "Unable to send!!!")
        
def sendmail():
    global w1
    w1 = Toplevel()
    w1.geometry("+500+200")
    w1.title('Mail')
    ents = makeform2(w1)
    w1.bind('<Return>', (lambda event, e=ents: fetch2(e)))
    b1 = Button(w1, text='Send', fg='green', bg='white', command=(lambda e=ents: fetch2(e)))
    b1.pack(side=BOTTOM, pady=5)
    
def read():
    global entries
    r = sr.Recognizer()
    with sr.Microphone() as source:
        notification("Recognition", "listening...", '/home/vinay/Downloads/mic.png')
        r.adjust_for_ambient_noise(source)
        audio  = r.listen(source)
    input = ''
    notification("Recognition", "processing...", '/home/vinay/Downloads/mic.png')
    try:
        input = r.recognize_google(audio)
        entry2.delete(0, 'end')
        entry2.insert(0, input)
        fetch1(entries)
    except sr.UnknownValueError:
        showerror("Error", "Sorry haven't understood!!!")
        
    except sr.RequestError:
        showerror("Error", "Connection error!!!")
        exit()
    
def check():
    try:
        results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
            msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
            email_snippet = msg['snippet']
            for message in msg['payload']['headers']:
                if (message['name'] == 'Subject'):
                    email_subject = message['value']
                    break

            for message in msg['payload']['headers']:
                if (message['name'] == 'From'):
                    email_from = message['value']
                    break

            
            
            notification("Mail", 'From: ' + email_from + '\n' + 'Subject: ' + email_subject + '\n' + 'Snippet: ' + email_snippet, '/home/vinay/Downloads/mail.png')

    except Exception as e:
        showerror("Error", "Oops!!! Something went wrong...")

def openapp(input):
    os.chdir('/usr/share/applications') 
    f = False
    files = Popen(["ls"], stdout=PIPE)
    files = Popen(["grep", ".desktop"], stdin=files.stdout, stdout=PIPE).communicate()[0]
    files = str(files, 'utf-8').splitlines()
    command = ''
    for file in files:
        name = Popen(["cat", file], stdout=PIPE)
        appName = Popen(["grep", "^Name="], stdin=name.stdout, stdout=PIPE).communicate()[0]
        name.stdout.close()
        apps = str(appName, 'utf-8').splitlines()
        for app in apps:
            appName1 = app.replace('Name=', '').lower()
            if input == appName1:
                name = Popen(["cat", file], stdout=PIPE)
                cmd = Popen(["grep", "^Exec="], stdin=name.stdout, stdout=PIPE).communicate()[0]
                name.stdout.close()
                cmd1 = str(cmd, 'utf-8').replace('Exec=', '')
                for cmd in cmd1.splitlines():
                    command = cmd.split()
                    command.append('&')
                    break
                f = True
                break
        if f:
            break

    try:
        subprocess.call(command)

    except Exception as e:
        showerror("error", "Not Found!!!")
  
def browse(input):
    webbrowser.open(input)
    
def remind(input2, time, ampm):
    global name
    time1 = time.split(':')
    
    if (len(time1[0]) < 3 and len(time1[1]) < 3 and int(time1[0]) < 24 and int(time1[0]) < 60 and int(time1[0]) > -1 and int(time1[1]) > -1):
        if (ampm == 'am'):
            if int(time1[0]) >= 12:
                hours = str(int(time1[0]) - 12)
                if int(hours) < 10:
                    hours = '0' + hours

            else:
                hours = time1[0]
                if int(hours) < 10:
                    hours = '0' + hours


        if (ampm == 'pm'):
            hours = time1[0]
            if int(hours) < 12:
                hours = str(int(hours) + 12)
            

        minutes = time1[1]
        if len(minutes) < 2:
            minutes = '0' + minutes

        user = service.users().getProfile(userId='me').execute()
        mailAddress = user['emailAddress']
        client = MongoClient()
        db = client['Reminders']
        jobs = db['Jobs']
        print('jobs')
        now = datetime.datetime.now()
        id = jobs.insert_one(
            {
                "name": name,
                "remind": input2,
                "mail": mailAddress,
                "time": str(now.strftime("%Y-%m-%d %H:%M")),
                "scheduledTime": hours + ':' + minutes
            }
        )

        cmt = str(id.inserted_id)
        cron = CronTab(user=True)
        job1 = cron.new(command='/usr/bin/python3 /home/hemanth/Desktop/notification.py',  comment=cmt)

        job1.minute.also.on(minutes)
        job1.hour.also.on(hours)

        cron.write()
        notification("Reminder", "Will remind you at " + time + ' ' + ampm, '/home/vhemanth/Downloads/reminder.png')
    
    else:
        showerror("Error!","Enter valid time!!!!")

def fetch1(entries):
    for entry in entries:
        text = entry[1].get().lower()
    if text == '':
        showerror('error', 'Enter an input')
    input1 = re.split('[-. _|\]]', text)
    print(input1[0])
    length = len(input1)
    if (length == 0):
        showerror("Error", "Do a valid search!!!")
    elif (input1[0] == 'mail'):
        sendmail()
    elif (input1[0] == 'open' and length > 1):
        input = ''
        for i in range(1, length):
            input = input + input1[i]
        openapp(input)
    elif (input1[0] == 'search' and length > 1):
        input = ''
        for i in range(1, length):
            input = input + input1[i]
        input = 'https://www.google.co.in/search?channel=fs&client=ubuntu&q=' + input
        browse(input)
    elif (input1[0] == 'voiceinput' and length == 1):
        read()
    elif (input1[0] == 'checkmail' and length == 1):
        check()
    elif (input1[0] == 'remind' and length > 1):
        input2 = ''
        for i in range(1, length - 3):
            input2 = input2 + input1[i] + ' '
        remind(input2, input1[length - 2], input1[length - 1])
    elif (input1[0] == 'time' and length == 1):
        now = datetime.datetime.now()
        time1 = str(datetime.time(now.hour, now.minute, now.second))
        notification("Time", time1, '/home/vinay/Downloads/time.png')
        speak(time1)
    elif (input1[0] == 'date' and length == 1):
        now = datetime.datetime.now()
        time1 = str(now.strftime("%Y-%m-%d %H:%M"))
        notification("Date", time1, '/home/vinay/Downloads/date.png')
        #speak(time1)
    
    else:
        try:
            syn = wordnet.synsets(text)
            messagebox.showinfo(text, syn[0].definition())
        
        except:      
            try:
                app_id = '7A99T5-E6QKE95J4G' #keys.wolframalpha_key
                client = wolframalpha.Client(app_id)
                res = client.query(text)
                answers = next(res.results).text
                messagebox.showinfo(text, answers)
            
            except:
                try:
                    answer = wikipedia.summary(text, sentences = 4)
                    messagebox.showinfo(text, answer)

                except:
                    text = 'https://www.google.co.in/#q=' + text
                    webbrowser.open(text)
def makeform1(w):
    global entry2
    global entries
    entries = []
    row = Frame(w)
    lab = Label(row, width=40, text='Hey I am Group 22, How can I help you?', anchor='w')
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack()
    row = Frame(w)
    entry2 = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    entry2.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('1', entry2))
    return entries

def fetch4(entries):
    global service
    global name
    name = entries[0][1].get()
    '''for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        values.append(text)'''
    f = True
    #print values
    if name == '':
        showerror("error", "All Values are not entered!!!")
        f = False
    else:    
        try:
            creds = None
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('gmail', 'v1', credentials=creds)
            
        except:
            showerror("error", "Unable to Login!!!")
            f = False
            
    if f:
        root.withdraw()
        w = Toplevel()
        w.geometry("+500+300")
        w.title('Group 22')
        ents = makeform1(w)
        w.bind('<Return>', (lambda event, e=ents: fetch1(e)))
        b1 = Button(w, text='Check mail', bg='white', fg='green', command=check)
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(w, text='Quit', fg='red', bg='white', command=root.destroy)
        b2.pack(side=RIGHT, padx=5, pady=5)
        w.protocol('WM_DELETE_WINDOW', root.destroy)
        # b3 = Button(w, text='Voice Input', bg='white', fg='green', command=read)
        # b3.pack(side=LEFT, padx=25, pady=5)

def fetch(entries):
    global service
    global name
    name = entries[0][1].get()
    '''for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        values.append(text)'''
    f = True
    #print values
    if name == '':
        showerror("error", "All Values are not entered!!!")
        f = False
    else:    
        try:
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('gmail', 'v1', credentials=creds)

        except:
            showerror("error", "Unable to Login!!!")
            f = False
            
    if f:
        root.withdraw()
        w = Toplevel()
        w.title('Group 22')
        w.geometry("+500+300")
        ents = makeform1(w)
        w.bind('<Return>', (lambda event, e=ents: fetch1(e)))
        b1 = Button(w, text='Check mail', bg='white', fg='green', command=check)
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(w, text='Quit', fg='red', bg='white', command=root.destroy)
        b2.pack(side=RIGHT, padx=5, pady=5)
        w.protocol('WM_DELETE_WINDOW', root.destroy)
        # b3 = Button(w, text='Check mail', bg='white', fg='green', command=check)
        # b3 = Button(w, text='Voice Input', bg='white', fg='green', command=read)
        # b3.pack(side=LEFT, padx=25, pady=5)
        
def makeform(root):
    entries = []
    row = Frame(root)
    lab = Label(row, width=15, text='Name', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(('Name', ent))
    row = Frame(root)
    return entries

if __name__ == '__main__':
    root = Tk()
    root.title('Login')
    root.geometry("+500+300")
    ents = makeform(root)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = Button(root, text='Login', fg = 'green', bg = 'white', command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Other Account', fg = 'green', bg = 'white', command=(lambda e=ents: fetch4(e)))
    b2.pack(side=RIGHT, padx=5, pady=5)
    root.mainloop()
