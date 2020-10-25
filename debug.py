from flask import Flask, request, abort
import os
from pathlib import Path
from typing import List

import cv2
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFilter

def change_kaonasi(src_image_path):
    face_count=0
    # カスケードファイルを指定して、分類機を作成
    cascade_file = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_file)
    img = cv2.imread(str(src_image_path))
    back_im=Image.open(str(src_image_path))
    #background = Image.new("RGB", image.size, (255, 255, 255))

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔を検知
    faces = face_cascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        face_count+=1
        img_kaonasi_url="./img/"+str(random.randrange(10))+".png"
        im2 = Image.open(img_kaonasi_url)
        im2=im2.resize((w, h))
        back_im.paste(im2, (x, y),mask=im2)
    back_im.save("a.jpg", quality=95)
    #cv2.imwrite("a.jpg",img)
    #cv2.imwrite("b.jpg",img)
    return 1

src_image_path="president.jpg"
a=change_kaonasi(src_image_path)
print(a)

