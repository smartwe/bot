import pyqrcode
qr = pyqrcode.create('hello')
qr.png('qr.png', scale=100)