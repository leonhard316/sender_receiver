import numpy as np
import cv2
import time
import json
import base64
import requests
import os

corner_x = []
corner_y = []
      
def send_image(img):
    _, encimg = cv2.imencode(".png", img)
    img_str = encimg.tostring()
    img_byte = base64.b64encode(img_str).decode("utf-8")
    img_json = json.dumps({'image':img_byte}).encode('utf-8')
  
    response = requests.post("http://192.168.23.123:444/save", data=img_json)
    print('{0} {1}'.format(response.status_code, json.loads(response.text)["message"]))

def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        corner_x.append(x)
        corner_y.append(y)
        
if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    #file = open()
    # whether exists  text file
    if(os.path.exists('FourCorners.txt')):
        with open('FourCorners.txt', 'r') as f:
            for j in range(4):
                line = f.readline()
                l = str(line).split(",")
                print(l[0].strip("'"))
                print(l[1].strip("'").rstrip("\n"))
                corner_x.append(l[0].strip("'"))
                corner_y.append(l[1].strip("'").rstrip("\n"))
                #print(corner_x)
                #print(corner_y)
    else:
        with open('FourCorners.txt', 'w') as f:
            # obtain corners with mouse click
            _, img = camera.read()
            window_name = 'click corners.'
            cv2.imshow(window_name, img)
            cv2.setMouseCallback(window_name, onMouse)
            cv2.waitKey(0)
            for i in range(4):
                f.write(str(corner_x[i]) + "," + str(corner_y[i]) + "\n")
    p_original = np.float32([[corner_x[0], corner_y[0]], [corner_x[1], corner_y[1]], [corner_x[2], corner_y[2]], [corner_x[3], corner_y[3]]])
    i = 0
    while True:
        time.sleep(1)
        _, img = camera.read()
        filename = "/home/pi/smart119/picture" + str(i) + ".png"
        cv2.imwrite(filename, img)
        # point2
        p_trans = np.float32([[0, 0], [524, 0], [0, 478], [524, 478]])
        
        # transform homography
        M = cv2.getPerspectiveTransform(p_original, p_trans)
        i_trans = cv2.warpPerspective(img, M, (524, 478))
        #cv2.imshow('', img)
        cv2.imshow('', i_trans)
        if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        send_image(i_trans)
        i = i + 1
 
