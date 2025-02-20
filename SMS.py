import requests
from datetime import datetime
import os
import pickle
import csv

def send_quick_sms(name, phone, date):
    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {"authorization": "NcT3OAB6evKMDphmjgLbYzoEUiuxkFRy8dJ7SWtGrIZlH1f2VnGQ9p0O54uTeRB8XySonhCzDiJ1tf2K",
                   "message": f'Your ward {name} was absent on {date}', "language": "english", "route": "q", "numbers": f'{phone}'}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    print(f'message sent to phone no {phone}')

def send_bulk_sms(name, phone, date):
    import requests

    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {"authorization": "NcT3OAB6evKMDphmjgLbYzoEUiuxkFRy8dJ7SWtGrIZlH1f2VnGQ9p0O54uTeRB8XySonhCzDiJ1tf2K", "sender_id": "TXTIND",
                   "message": f"Your ward {name} was absent on {date}",
                   "route": "v3", "numbers": f'{phone}'}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    print(f'message sent to phone no {phone}')

def smsToAbsentees():
    # sending mails to absentees
    today = datetime.today()
    file_name = today.strftime("F%d_%m_%Y")
    today = today.strftime("%d-%m-%Y")
    attendanceList = {}
    if os.path.exists(f'Resources/AttendanceList/{file_name}.dat'):
        with open(f'Resources/AttendanceList/{file_name}.dat', 'rb') as f:
            attendanceList = pickle.load(f)
    else:
        print(f'{file_name} File Not Found')
        return

    with open('Resources/StudentDetails.csv') as f1:
        reader1 = csv.reader(f1)
        next(reader1)
        for enroll, roll, name, email, phone in reader1:
            if attendanceList[enroll][0] == 'A':
                # send_quick_sms(name, phone, today)
                send_bulk_sms(name, phone, today)
                break

