#!/usr/bin/python3

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from blockchain import Blockchain

import pickle

global TRANSACTIONS_PER_BLOCK
TRANSACTIONS_PER_BLOCK = 1500


class Ledger:
    def __init__(self, transactionsPerBlock=1500):
        self.ledgerBlockchain = Blockchain()
        self.transactions = []
        self.TRANSACTIONS_PER_BLOCK = transactionsPerBlock
        self.financeCache = {}

    def validateSignature(self, m, ssig, sk):
        sValidator = PKCS1_v1_5.new(sk)
        certDigest = SHA256.new()
        certDigest.update(str.encode(m))
        if not sValidator.verify(certDigest, ssig):
            return False
        return True

    def checkUserInLedger(self, uid):
        return True #TODO implement

    def calculateAllFinances(self):
        self.financeCache = {} #clear data
        for i in range(1, self.ledgerBlockchain.getNumBlocks()):
            blockBytes = self.ledgerBlockchain.getBlockData(i)

    #TODO substitute for a simple lookup and ensure that lookup table is kept
    #up-to-date
    def checkBalance(self, uid):
        finances = 0
        for i in range(1, self.ledgerBlockchain.getNumBlocks()):
            blockBytes = self.ledgerBlockchain.getBlockData(i)
            import pdb; pdb.set_trace()
            blockData = pickle.loads(blockBytes)
            if blockData['receiver'] == uid:
                finances += blockData['amount']
            if blockData['sender'] == uid:
                finances -= blockData['amount']
        for transaction in self.transactions:
            if transaction['receiver'] == uid:
                finances += transaction['amount']
            if transaction['sender'] == uid:
                finances -= transaction['amount']
        return finances

    def save(self, filename="./ledger.bc"):
        # save as a .bc (blockchain) file
        while len(self.transactions) != 0:
            block = pickle.dumps(
                self.transactions[0:TRANSACTIONS_PER_BLOCK])
            self.ledgerBlockchain.addBlock(block)
            self.transactions = self.transactions[TRANSACTIONS_PER_BLOCK:]
        self.ledgerBlockchain.save(filename)

    def load(self, filename):
        if type(filename) is not str:
            raise TypeError("Filename must be of type str")
        self.ledgerBlockchain.load(filename)
        self.calculateAllFinances()

    # also, need to mix in an index to prevent a repeat attack!

    def addTransaction(self, data):
        senderID = data['sender']
        receiverID = data['receiver']
        amt = data['amount']
        ssig = data['senderSig']
        sPubKey = data['senderPubKey']
        message = str(senderID) + str(receiverID) + str(amt)
        sigsValid = self.validateSignature(message, ssig,
                                            sPubKey)
        if not sigsValid:
            return (False, "Invalid Signature(s) detected when adding a " +
                  "transaction. Transaction will not be added")
        hasMoney = self.checkBalance(senderID)
        if not hasMoney:
            print()
            return (False, "Sender does not have adequite finances to complete" +
                  "this transaction. Transaction will not be added")

        self.transactions.append(data)
        while len(self.transactions) >= TRANSACTIONS_PER_BLOCK:
            block = pickle.dumps(
                self.transactions[0:TRANSACTIONS_PER_BLOCK])
            self.ledgerBlockchain.addBlock(block)
            self.transactions = self.transactions[TRANSACTIONS_PER_BLOCK:]

        return (True, "Transaction added")

