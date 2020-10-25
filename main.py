from flask import Flask, request, abort
import os
from pathlib import Path
from typing import List

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage)
import cv2
import numpy as np
import random

app = Flask(__name__)


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

SRC_IMAGE_PATH = "static/images/{}.jpg"
MAIN_IMAGE_PATH = "static/images/{}_main.jpg"
PREVIEW_IMAGE_PATH = "static/images/{}_preview.jpg"

def save_image(message_id: str, save_path: str) -> None:
    """保存"""
    message_content = line_bot_api.get_message_content(message_id)
    with open(save_path, "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)


def change_kaonasi(src_image_path,main_image_path,preview_image_path):
    face_count=0
    # カスケードファイルを指定して、分類機を作成
    cascade_file = "haarcascade_frontalface_alt.xml"
    face_cascade = cv2.CascadeClassifier(cascade_file)
    img = cv2.imread(str(src_image_path))

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔を検知
    faces = face_cascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        face_count+=1
        img_kaonasi_url="./img/"+str(random.randrange(10))+".jpg"
        img_kaonasi = cv2.imread(img_kaonasi_url)
    
        # 顔に合ったサイズに隠す用画像をリサイズする
        img_kaonasi2 = img_kaonasi.resize((w, h))
        img[0:height, 0:width] = img_kaonasi2
    cv2.imwrite(main_image_path,img)
    cv2.imwrite(preview_image_path,img)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#メッセージ受信時のイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id

    src_image_path = Path(SRC_IMAGE_PATH.format(message_id)).absolute()
    main_image_path = MAIN_IMAGE_PATH.format(message_id)
    preview_image_path = PREVIEW_IMAGE_PATH.format(message_id)

    # 画像を保存
    save_image(message_id, src_image_path)
    change_kaonasi(src_image_path,main_image_path,preview_image_path)


    """
    test_url = "./static/"+event.message.id+".jpg"
    img,face_count=change_kaonasi(test_url)
    text=str(face_count)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

    """
    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url=f"https://date-the-image.herokuapp.com/{main_image_path}",
        preview_image_url=f"https://date-the-image.herokuapp.com/{preview_image_path}",
    )
    line_bot_api.reply_message(event.reply_token, image_message)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)