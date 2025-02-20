import csv
import os
import pickle
from datetime import datetime
from datetime import timedelta
import numpy as np

def generate_report(start = '07-04-2023', end = '09-06-2023'):
    start = datetime.strptime(start, '%d-%m-%Y').date()
    end = datetime.strptime(end, '%d-%m-%Y').date()
    f1 = open('report.csv', 'w')
    f1.close()
    f1 = open('report.csv', 'a+')
    f1.write('Enroll,')
    with open('Resources/StudentDetails.csv') as f2:
        r2 = csv.reader(f2)
        next(r2)
        for enroll, roll, name, email, phone in r2:
            f1.write(f'{enroll},')
        f1.write('\n')

    f1.write('RollNo,')
    with open('Resources/StudentDetails.csv') as f2:
        r2 = csv.reader(f2)
        next(r2)
        for enroll, roll, name, email, phone in r2:
            f1.write(f'{roll},')
        f1.write('\n')

    f1.write('Name,')
    with open('Resources/StudentDetails.csv') as f2:
        r2 = csv.reader(f2)
        next(r2)
        for enroll, roll, name, email, phone in r2:
            f1.write(f'{name},')
        f1.write('\n')

    curr = start
    while curr<=end:
        date_str = curr.strftime('%d-%m-%Y')
        curr_file = f'F{date_str.replace("-", "_")}.dat'

        attendanceList = {}
        if os.path.exists(f'Resources/AttendanceList/{curr_file}'):
            with open(f'Resources/AttendanceList/{curr_file}', 'rb') as f:
                attendanceList = pickle.load(f)
        else:
            print(f'File not available for {date_str} date')
            # f1.write(f'{date_str},\n')
            curr = curr + timedelta(days=1)
            continue

        f1.write(f'{date_str},')
        with open('Resources/StudentDetails.csv') as f2:
            r2 = csv.reader(f2)
            next(r2)
            for enroll, roll, name, email, phone in r2:
                if attendanceList.get(enroll) is not None:
                    f1.write(f'{attendanceList[enroll][0]},')
                else:
                    f1.write('A,')
            f1.write('\n')
        curr = curr + timedelta(days=1)

    f1.close()

    with open('report.csv') as file:
        lis = [x.replace(',\n', '').split(',') for x in file]

    # print(lis)

    f1 = open('report.csv', 'w')
    f1.close()
    f1 = open('report.csv', 'a+')

    for x in zip(*lis):
        for y in x:
            f1.write(y + ', ')
        f1.write('\n')

    f1.close()



