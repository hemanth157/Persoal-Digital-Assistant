from datetime import datetime
from pymongo import MongoClient
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from subprocess import Popen, PIPE
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify

def notification(title, message, icon):
    if not 'DISPLAY' in os.environ:
        os.environ['DISPLAY'] = ':0'

    Notify.init('PDA')
    popup = Notify.Notification.new(title, message, icon)
    popup.show()

def main():
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    user = service.users().getProfile(userId='me').execute()
    mailAddress = user['emailAddress']
    
    client = MongoClient()
    db = client['Reminders']
    jobs = db['Jobs']

    now = datetime.now()

    currentTime = now.strftime("%H:%M")

    query = {'mail': mailAddress, 'scheduledTime': currentTime}

    input = jobs.find(query)

    input2 = ''
    id = ''
    for x in input:
        id = ' ' + str(x['_id'])
        input2 = x['remind']

    notification("Reminder", input2, '/home/reminder.png')
    removeCron = Popen(["crontab", "-l"], stdout=PIPE)
    removeCron1 = Popen(["grep", "-v", id], stdin=removeCron.stdout, stdout=PIPE)
    removeCron2 = Popen(["crontab", "-"], stdin=removeCron1.stdout, stdout=PIPE)
    removeCron2.stdout.close()
    removeCron1.stdout.close()
    removeCron.stdout.close()

if __name__ == '__main__':
    main()