from datetime import datetime
import os
import pickle
import csv
import ReportGeneration

today = datetime.today()
today = today.strftime("F%d_%m_%Y")
attendanceList = {}
if os.path.exists(f'AttendanceList/{today}.dat'):

    with open(f'AttendanceList/F07_06_2023.dat', 'rb') as f:
        attendanceList = pickle.load(f)
        print(attendanceList)
        print(len(attendanceList))
else:
    print(f'{today} File Not Found')

ReportGeneration.generate_report('01-04-2023', '09-06-2023')




