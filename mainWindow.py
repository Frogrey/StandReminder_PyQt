from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

import pythoncom
import pyWinhook as pyHook

import cv2, time, threading

# 记录过去每1分钟的键鼠操作次数
mouseKeyNums = [[0,0]]

flagOn = False
nowInd = 0
thread = None
hm = pyHook.HookManager()
# 读取人脸模型库
face_cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_alt2.xml')

def hookInit():
    # 创建一个“钩子”管理对象
    # hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    # pythoncom.PumpMessages(10000)

def detectFace():
    cap = cv2.VideoCapture(0)

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

    cv2.imwrite('./images/' + str(len(mouseKeyNums)) + '.png', img)
    cap.release()

def onMouseEvent(event):
    # 监听鼠标事件
    # print ("MessageName:", event.MessageName)
    # print ("Message:", event.Message)
    # print ("Time:", event.Time)
    # print ("Window:", event.Window)
    # print ("WindowName:", event.WindowName)
    # print ("Position:", event.Position)
    # print ("Wheel:", event.Wheel)
    # print ("Injected:", event.Injected)
    # print ("---")

    mouseKeyNums[-1][0] += 1

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True

def onKeyboardEvent(event):
    # 监听键盘事件
    # print ("MessageName:", event.MessageName)
    # print ("Message:", event.Message)
    # print ("Time:", event.Time)
    # print ("Window:", event.Window)
    # print ("WindowName:", event.WindowName)
    # print ("Ascii:", event.Ascii, chr(event.Ascii))
    # print ("Key:", event.Key)
    # print ("KeyID:", event.KeyID)
    # print ("ScanCode:", event.ScanCode)
    # print ("Extended:", event.Extended)
    # print ("Injected:", event.Injected)
    # print ("Alt", event.Alt)
    # print ("Transition", event.Transition)
    # print ("---")

    mouseKeyNums[-1][1] += 1

    # 同鼠标事件监听函数的返回值
    return True

def onQuit():
    global hm
    hm.UnhookMouse()
    hm.UnhookKeyboard()

def timer():
    global nowInd, flagOn
    while(flagOn):
        time.sleep(60)
        print(mouseKeyNums)
        mouseKeyNums.append([0,0])
        detectFace()

def switch():
    global flagOn, thread, hm
    flagOn = not flagOn
    print(flagOn)

    if (flagOn):
        thread = threading.Thread(target=timer)
        thread.start()
        hm.HookKeyboard()
        hm.HookMouse()
    else:
        hm.UnhookMouse()
        hm.UnhookKeyboard()

class Stats:
    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./ui/main.ui')

        self.ui.btnSw.clicked.connect(switch)

        # self.ui.setFixedSize(self.ui.width(), self.ui.height())

def main():
    hookInit()

    app = QApplication([])
    stats = Stats()
    stats.ui.show()

    app.aboutToQuit.connect(onQuit)
    app.exec_()


if __name__ == "__main__":
    main()