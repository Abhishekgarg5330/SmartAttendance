import os.path
import csv
import cv2
import face_recognition
from datetime import datetime
import numpy as np
import pickle

# function to mark attendance on excel file
def markAttendance(id, attendanceList, date, time):
    attendanceList[id] = ('P', time)
    with open(f'Resources/AttendanceList/{date}.dat', 'wb') as f:
        pickle.dump(attendanceList, f)

def RecognitionAndAttendance(uniqueIds, classNames, encodeListKnown, cam, rep = 200, hlt=10, tolerance = 0.6):
    today = datetime.today()
    today = today.strftime("F%d_%m_%Y")
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    attendanceList = {}
    if os.path.exists(f'Resources/AttendanceList/{today}.dat'):
        with open(f'Resources/AttendanceList/{today}.dat', 'rb') as f:
            attendanceList = pickle.load(f)
    else:
        with open('Resources/StudentDetails.csv') as file:
            reader = csv.reader(file)
            next(reader)
            for Enroll, RollNo, Name, Email, Phone in reader:
                attendanceList[Enroll] = ('A', '00:00:00')


    if cam:
        cap = cv2.VideoCapture(0)
        while rep>0:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurrFrame = face_recognition.face_locations(imgS)
            encodesCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

            for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2

                if matches[matchIndex]:
                    id = uniqueIds[matchIndex]
                    name = classNames[matchIndex]
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(id, attendanceList, today, time)
                else:
                    name = "NOT RECOGNIZED"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Webcam', img)
            cv2.waitKey(10)
            rep = rep - 1
        cv2.destroyAllWindows()
    else:
        path = 'Resources/imagesToCheck'
        # Grab list of images from ImagesAttendance folder
        myList = os.listdir(path)
        print(myList)

        for cl in myList:
            img = cv2.imread(f'{path}/{cl}')
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            facesCurrFrame = face_recognition.face_locations(imgS)
            encodesCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

            for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                y1, x2, y2, x1 = faceLoc

                if matches[matchIndex]:
                    id = uniqueIds[matchIndex]
                    name = classNames[matchIndex]
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(id, attendanceList, today, time)
                else:
                    name = "NOT RECOGNIZED"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
            cv2.imshow('Output', img)
            cv2.waitKey(hlt*1000)
        cv2.destroyAllWindows()
