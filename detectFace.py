import cv2

# 读取人脸模型库
face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_alt2.xml')

#获取摄像头
cap = cv2.VideoCapture(0)

def detect():
    # 读取摄像头当前这一帧的画面  ret:True fase image:当前这一帧画面
    ret, img = cap.read()
    # 图片进行灰度处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 人脸检测
    faces = face_cascade.detectMultiScale(gray)

    # 绘制人脸框
    for (x, y, w, h) in faces:
        width = x + w
        height = y + h
        strok = 2
        color = (255, 0, 0)
        cv2.rectangle(img, (x, y), (width, height), color, strok)

    cv2.imwrite('face.png', img)
    cap.release()


detect()


