from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from clientui import Ui_Messenger
import time
from datetime import datetime

class Messenger(QtWidgets.QMainWindow, Ui_Messenger):
    def __init__(self,url):
        super().__init__()
        self.setupUi(self)
        self.url = url
        self.after_id = -1
        self.sendButton.pressed.connect(self.button_pressed)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)


    def pr_print(self, message):
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%H:%M')
        first_line = dt + ' ' + message['name']
        self.chat.append(first_line)
        self.chat.append(message['text'])
        self.chat.append('')
        self.chat.repaint()



    def update_messages(self):
        response = None
        try:
            response = requests.get(self.url+ '/messages', params = {'after_id': self.after_id})
        except:
            pass
        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pr_print(message)
                self.after_id = message['id']

    def button_pressed(self):
        name = self.nickinput.text()
        text = self.messageinput.toPlainText()
        data = {
        'name': name,
        'text': text
        }
        response = requests.post(self.url+'/send', json = data)
        self.messageinput.clear()
        self.messageinput.repaint()

app = QtWidgets.QApplication([])
window = Messenger('http://messengerpy-env-1.eba-rs4kjrzc.us-east-2.elasticbeanstalk.com')
window.show()
app.exec_()