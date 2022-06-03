import os
import json
import cv2
import base64
import numpy as np
from datetime import datetime
from flask import Flask, request, Response
app = Flask(__name__)
count = 0

# 画像を保存するフォルダの作成
image_dir = "./images"
if not os.path.isdir(image_dir):
  os.mkdir(image_dir)

@app.route('/save', methods=['POST'])

def save_image():
    # データの変換処理
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.fromstring(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)

    # 画像ファイルを保存
    global count
    #filename = "./images/image{}.png".format(count)
    filename = "C:/xampp/webroot/gallery_php/images/image{}.png".format(count)
    cv2.imwrite(filename, decimg)
    count += 1

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was saved".format(filename)}), status=200)

if __name__ == '__main__':
    app.run(host='192.168.23.123', port=444)

