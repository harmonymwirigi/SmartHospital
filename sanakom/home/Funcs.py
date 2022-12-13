from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os
from flask import Flask
from flask import render_template
from flask import request,redirect
from flask import Flask, render_template, request,url_for
import copy
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO
import logging
from sys import stdout
from apps.home.camera import VideoCamera
import cv2
import dlib
#from cap import name
t = []

'''def facepredect(frame,img):
    Boxes = []  # to store the face co-ordinates
    face_detector = dlib.get_frontal_face_detector()
    # converting to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -------------detecting the faces--------------#
    faces = face_detector(img_gray)
    print("faces")
    model_mean = (78.4263377603, 87.7689143744, 114.895847746)

    # If no faces our detected
    if not faces:
        mssg = 'No face detected'
        cv2.putText(img, f'{mssg}', (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (200), 2)
        cv2.imshow('Age detected', img)
        print("no face")


    else:
        # --------- Bounding Face ---------#
        for face in faces:
            x = face.left()  # extracting the face coordinates
            y = face.top()
            x2 = face.right()
            y2 = face.bottom()

            # rescaling those coordinates for our image
            box = [x, y, x2, y2]
            Boxes.append(box)
            cv2.rectangle(frame, (x, y), (x2, y2),
                          (00, 200, 200), 2)

        for box in Boxes:
            face = frame[box[1]:box[3], box[0]:box[2]]
            cv2.imshow("face", face)
            cv2.imwrite('face2.jpg', face)

            # ----- Image preprocessing --------#
            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), model_mean, swapRB=False)
        return blob,face

def agedetect(blob):
    print("hiii")
    # ------------ Model for Age detection --------#
    age_weights = "age_deploy.prototxt"
    age_config = "age_net.caffemodel"
    age_Net = cv2.dnn.readNet(age_config, age_weights)

    # Model requirements for image
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
               '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    age_Net.setInput(blob)
    age_preds = age_Net.forward()
    age = ageList[age_preds[0].argmax()]
    print("age")
    print(age)
    return age
def cropface(imagepath):
    img = cv2.imread(imagepath)
    print("i am in")

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces and crop the faces
    padding=20
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x-padding, y-padding), (x+padding + w, y+padding + h), (0, 0, 255), 2)
        faces = img[y-padding:y + h+padding, x-+padding:x + w+padding]
        cv2.imshow("face", faces)
        cv2.imwrite("static/images/crpd.png", faces)

    # Display the output
    cv2.imwrite('detcted.jpg', img)
    cv2.imshow('img', img)
    return(faces)

'''
def autisticpic(imagepath):

    model = load_model('keras_model.h5', compile=False)
    print("1")

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    # namee=name
    image = Image.open(imagepath)
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image=image.resize(size)

    # turn the image into a numpy array
    image_array = np.asarray(image)
    cv2.imwrite("static/images/crpd23.png", image_array)
    cv2.imshow('img', image_array)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    #data[0] = image

    # run the inference
    predictionn = model.predict(data)
    class_names = {"autistic", "Non-autistic"}
    y = predictionn.argmax(axis=-1)
    t.append(y)
    print("2")
    if (y == 0):
        res = "Autistic"
        print("Autistic")
        return res
    elif(y==1):
        res = "non Autistic"
        return res
        print("non autistic")
    else:
        print("didnt work")
        return "didnt work"
