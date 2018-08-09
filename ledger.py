#!/usr/bin/python3

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from blockchain import Blockchain
from wallet import Wallet

import array, pickle

global TRANSACTIONS_PER_BLOCK
TRANSACTIONS_PER_BLOCK = 1500


class Ledger:
    def __init__(self, transactionsPerBlock=1500):
        self.ledgerBlockchain = Blockchain()
        self.transactions = [] #an array of transactions to go into a block
        TRANSACTIONS_PER_BLOCK = transactionsPerBlock

    def validateSignatures(self, m, ssig, rsig, sk, rk):
        sValidator = PKCS1_v1_5.new(sk)
        rValidator = PKCS1_v1_5.new(rk)
        certDigest = SHA256.new()
        certDigest.update(str.encode(m))
        if not sValidator.verify(certDigest, ssig):
            return False
        if not rValidator.verify(certDigest, rsig):
            return False
        return True

    def validateFinances(self, sid, amt):
        return True #TODO

    def save(self, filename="./ledger.bc"):
        #save as a .bc (blockchain) file
        while len(self.transactions) != 0:
            transactionBytes = pickle.dumps(self.transactions[0:TRANSACTIONS_PER_BLOCK])
            self.ledgerBlockchain.addBlock(transactionBytes)
            self.transactions = self.transactions[TRANSACTIONS_PER_BLOCK:]
        self.ledgerBlockchain.save(filename)

    def load(self, filename):
        if type(filename) is not str:
            raise TypeError("Filename must be of type str")
        self.ledgerBlockchain.load(filename)

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
            print("Invalid Signature(s) detected when adding a transaction. Transaction will not be added")
            return False
        hasMoney = self.validateFinances(senderID, amt)
        if not hasMoney:
            print("Sender does not have adequite finances to complete this transaction. Transaction will not be added")
            return False

        self.transactions.append(data)
        while len(self.transactions) >= TRANSACTIONS_PER_BLOCK:
            transactionBytes = pickle.dumps(self.transactions[0:TRANSACTIONS_PER_BLOCK])
            self.ledgerBlockchain.addBlock(transactionBytes)
            self.transactions = self.transactions[TRANSACTIONS_PER_BLOCK:]

        return True
