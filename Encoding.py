import os
import cv2
import face_recognition
import pickle
import numpy as np
import csv


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        currEnc = face_recognition.face_encodings(img)[0]
        encodeList.append(currEnc)
    return encodeList

def generateEncoding() :
    if os.path.exists('Resources/Encoding.dat'):
        # Load face encodings
        with open('Resources/Encoding.dat', 'rb') as f:
            all_face_encodings = pickle.load(f)

        # Grab the list of names and the list of encodings
        classNames = []
        encodeListKnown = []
        uniqueIds = list(all_face_encodings.keys())
        for id in uniqueIds:
            classNames.append(all_face_encodings[id][0])
            encodeListKnown.append(all_face_encodings[id][1])
        return uniqueIds, classNames, encodeListKnown

    else:
        path = 'Resources/KnownImages'
        images = []
        uniqueIds = []
        classNames = []
        myList = os.listdir(path)

        for cl in myList:
            currImg = cv2.imread(f'{path}/{cl}')
            images.append(currImg)
            uniqueIds.append(os.path.splitext(cl)[0])

        encodeListKnown = findEncodings(images)

        for id in uniqueIds:
            with open('Resources/StudentDetails.csv') as file:
                reader = csv.reader(file)
                next(reader)
                flag = 0
                for Enroll, RollNo, Name, Email, Phone in reader:                  #do changes here
                    if id == Enroll:
                        flag = 1
                        classNames.append(Name)
                if flag == 0:
                    classNames.append('Unknown')


        all_face_encodings = {}
        for enc, name, roll in zip(encodeListKnown, classNames, uniqueIds):
            all_face_encodings[roll] = (name, enc)

        with open('Resources/Encoding.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)

        return uniqueIds, classNames, encodeListKnown