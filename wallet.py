from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import os.path

class Wallet:
    def __init__(self):
        if not os.path.isfile('./walletKey.pem'):
            self.key = self.saveNewKey()
        else:
            self.key = self.loadKey()
        self.signer = PKCS1_v1_5.new(self.key)


    def loadKey(self):
        keyfile = open('walletKey.pem', 'r')
        key = RSA.importKey(keyfile.read())
        keyfile.close()
        return key

    def saveNewKey(self):
        print "Generating a new wallet key"
        if os.path.isfile('./walletKey.pem'):
            print "wallet key already exists in current directory"
            key = self.loadKey()
        else:
            #generate the key
            key = RSA.generate(2048)
            #save the key
            keyfile = open('walletKey.pem', 'w')
            keyfile.write(key.exportKey('PEM'))
            keyfile.close()
        return key

    def signMessage(self, message):
        #sign the message
        digest = SHA.new()
        digest.update(message)
        signature = self.signer.sign(digest)
        return signature

    #message must be a byte string
    def validateMessage(self, message, sig):
        digest = SHA.new()
        digest.update(message)
        return self.signer.verify(digest, sig)

    def getPublicKey(self):
        return self.key.publickey