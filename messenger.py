from PyQt5 import QtWidgets

import design
import time
import datetime
import requests
import threading


class MessengerApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)
        threading.Thread(target=self.receive).start()

    def send(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.plainTextEdit.toPlainText()

        if not username or not password or not text:
            return

        try:
            requests.post(
                'http://127.0.0.1:5000/send',
                json={'username': username, 'password': password, 'text': text}
            )
        except:
            print('Connection error!')

        self.plainTextEdit.setPlainText('')
        self.plainTextEdit.repaint()

    def receive(self):
        last_received = 0

        while True:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': last_received}
            )

            if response.status_code == 200:
                messages = response.json()['messages']
                for message in messages:
                    username = message['username']
                    time_str = datetime.datetime.fromtimestamp(
                        message['time']).strftime('%d/%m/%Y %H:%M:%S')
                    text = message['text']

                    self.textBrowser.append(f'{username} {time_str}')
                    self.textBrowser.append(text)
                    self.textBrowser.append('')

                    last_received = message['time']

            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessengerApp()
    window.show()
    app.exec_()
