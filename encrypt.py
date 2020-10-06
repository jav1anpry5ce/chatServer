import pyAesCrypt
import io,os,sys,time


class encrypt(object):
    def __init__(self):
        self.password = "superSecureDataHere"
        self.bufferSize = 1024

    def encryptData(self, msg):
    	data = msg.encode('utf-8')
    	fIn = io.BytesIO(data)
    	fCiph = io.BytesIO()
    	pyAesCrypt.encryptStream(fIn, fCiph, self.password, self.bufferSize)
    	message = fCiph.getvalue()
    	return message

    def decryptData(self, msg):
    	fullData = b''
    	fCiph = io.BytesIO()
    	fDec = io.BytesIO()
    	fCiph = io.BytesIO(msg)
    	ctlen = len(fCiph.getvalue())
    	fCiph.seek(0)
    	pyAesCrypt.decryptStream(fCiph, fDec, self.password, self.bufferSize, ctlen)
    	message = str(fDec.getvalue().decode('utf-8'))
    	return message
