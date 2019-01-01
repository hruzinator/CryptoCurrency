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
        if not self.financeCache:
            self.buildCache()
        return uid in self.financeCache

    #DOES NOT PERFORM CHECKS RIGHT NOW
    def buildCache(self):
        self.financeCache = {} #clear data
        for i in range(1, self.ledgerBlockchain.getNumBlocks()):
            blockBytes = self.ledgerBlockchain.getBlockData(i)
            blockData = pickle.loads(blockBytes)

            rec = blockData['reciever']
            amount = blockData['amount']

            if rec not in self.financeCache:
                self.financeCache[rec] = 0
     
            if blockData['type'] == 'reward':
                self.financeCache[rec] += amt
            elif blockData['type'] == 'transaction':
                send = blockData['sender']
                if send not in self.financeCache:
                    self.financeCache[send] = 0
                self.financeCache[send] -= amt
                self.financeCache[rec] += amt


    #TODO substitute for a simple lookup and ensure that lookup table is kept
    #up-to-date
    def checkBalance(self, uid):
        if uid not in self.financeCache:
            return None
        return self.financeCache[uid]

    def transactionsToBlocks(self):
        while len(self.transactions) >= TRANSACTIONS_PER_BLOCK:
            block = pickle.dumps(
                self.transactions[0:TRANSACTIONS_PER_BLOCK])
            self.ledgerBlockchain.addBlock(block)
            self.transactions = self.transactions[TRANSACTIONS_PER_BLOCK:]

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
        self.buildCache()

    # also, need to mix in an index to prevent a repeat attack!

    def addTransaction(self, data):
        data['type'] = 'transaction'
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
            return (False, "Sender does not have adequite finances to complete" +
                  "this transaction. Transaction will not be added")

        self.transactions.append(data)
        self.transactionsToBlocks()
        self.financeCache[recieverID] += amount
        self.financeCache[senderID] -= amount

        return (True, "Transaction added")



    def addBlockReward(self, reciever, amount):
        # validation
        if not self.checkUserInLedger(reciever):
            raise Exception("Tried to add a block reward to a user that doesn't exist.")
        if type(amount) is not int:
            raise TypeError("amount must be of type int")
        data = {
            'type': 'reward',
            'receiver': reciever,
            'amount': amount
        }
        
        self.transactions.append(data)
        self.transactionsToBlocks()
        self.financeCache[reciever] += amount

        return (True, "Reward added")
        

