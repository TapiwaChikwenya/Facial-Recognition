#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 14:38:13 2020

@author: tapiwachikwenya
"""

import numpy as np
import cv2
import pickle


face_cascade =cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
cap = cv2.VideoCapture(0)

labels= {"person_name": 1}
with open("labels.pickle",'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}


while True:
    # capture frame by frame
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces =face_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=5)
    for (x,y,w,h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        #recognize deep learned model predict keras tensor pytorch
        id_, conf = recognizer.predict(roi_gray)
        if conf>=30 :#and conf <= 85:
            print(id_,conf)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color= (255,100,100)
            stroke = 2
            cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
        img_item = "tata.png"
        cv2.imwrite(img_item,roi_color)
        #drawing rectangle around region of interest roi 
        color = (255,0,0)#BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y= y+h
        cv2.rectangle(frame, (x,y),(end_cord_x,end_cord_y),color, stroke)
        #detect eyes on a face
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
        
    
    #display the frames 
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
 # when everything is done release the capture   
cap.release()
cv2.destroyAllWindows()