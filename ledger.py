from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from blockchain import Blockchain
from wallet import Wallet

global TRANSACTIONS_PER_BLOCK
TRANSACTIONS_PER_BLOCK = 5


class Ledger:
    def __init__(self):
        self.ledgerBlockchain = Blockchain()
        self.transactions = [] #an array of transactions to go into a block

    def validateSignatures(self, m, ssig, rsig, sk, rk):
        sValidator = PKCS1_v1_5.new(sk)
        rValidator = PKCS1_v1_5.new(rk)
        certDigest = SHA256.new()
        certDigest.update(m)
        if not sValidator.verify(certDigest, ssig):
            return False
        if not rValidator.verify(certDigest, rsig):
            return False
        return True

    def validateFinances(self, sid, amt):
        return True #TODO


    #Need public keys to validate signatures
    #also, need to mix in an index to prevent a repeat attack!

    def addTransaction(self, data):
        senderID = data['sender']
        receiverID = data['receiver']
        amt = data['amount']
        ssig = data['senderSig']
        rsig = data['receiverSig']
        sPubKey = data['senderPubKey']
        rPubKey = data['receiverPubKey']
        message = str(senderID) + str(receiverID) + str(amt)
        sigsValid = self.validateSignatures(message, ssig, rsig, sPubKey, rPubKey)
        if not sigsValid:
            print "Invalid Signature(s) detected when adding a transaction. Transaction will not be added"
            return False
        hasMoney = self.validateFinances(senderID, amt)
        if not hasMoney:
            print "Sender does not have adequite finances to complete this transaction. Transaction will not be added"
            return False

        self.transactions.append(data)
        if len(self.transactions) >= TRANSACTIONS_PER_BLOCK:
            self.ledgerBlockchain.addBlock(self.transactions)
            self.transactions = []


        return True
