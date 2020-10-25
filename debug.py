from flask import Flask, request, abort
import os
from pathlib import Path
from typing import List

import cv2
import numpy as np
import random

def change_kaonasi(src_image_path):
    face_count=0
    # カスケードファイルを指定して、分類機を作成
    cascade_file = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_file)
    img = cv2.imread(str(src_image_path))

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔を検知
    faces = face_cascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        face_count+=1
        img_kaonasi_url="./img/"+str(random.randrange(10))+".png"
        img_kaonasi = cv2.imread(img_kaonasi_url)
    
        # 顔に合ったサイズに隠す用画像をリサイズする
        img_kaonasi2 =cv2.resize(img_kaonasi ,(w, h))
        #img_kaonasi2 = img_kaonasi.resize((w, h))
        img[y:y+h,x:x+w] = img_kaonasi2
        #img[x:x+w, y:y+h] = img_kaonasi2
    cv2.imwrite("a.jpg",img)
    cv2.imwrite("b.jpg",img)
    return 1

src_image_path="president.jpg"
a=change_kaonasi(src_image_path)
print(a)