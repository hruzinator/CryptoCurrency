from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import os.path
import dill

class Wallet:
    def __init__(self, walletFile):
        self.walletFile = walletFile
        if not os.path.isfile(walletFile):
            self.key = self.saveNewKey()
        else:
            self.key = self.loadKey()
        self.signer = PKCS1_v1_5.new(self.key)

        widDigest = SHA256.new()
        widDigest.update(dill.dumps(self.getPublicKey()))
        self.wid = widDigest.hexdigest()


    def loadKey(self):
        keyfile = open(self.walletFile, 'r')
        key = RSA.importKey(keyfile.read())
        keyfile.close()
        return key

    def saveNewKey(self):
        print "Generating a new wallet key"
        if os.path.isfile(self.walletFile):
            print "wallet key already exists in current directory"
            key = self.loadKey()
        else:
            #generate the key
            key = RSA.generate(2048)
            #save the key
            keyfile = open(self.walletFile, 'w')
            keyfile.write(key.exportKey('PEM'))
            keyfile.close()
        return key

    def signMessage(self, message):
        #sign the message
        digest = SHA256.new()
        digest.update(message)
        signature = self.signer.sign(digest)
        return signature

    def validateMessage(self, message, sig):
        digest = SHA256.new()
        digest.update(message)
        return self.signer.verify(digest, sig)

    def getPublicKey(self):
        return self.key.publickey()

    #get wallet ID
    def getWID(self):
        return self.wid
