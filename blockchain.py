#!/usr/bin/python3

#simple blockchain.
from Crypto.Hash import SHA256
import hashlib #TODO still need? Convert to Crypto lib.
import datetime as date
import os.path

global POWSize #proof of work size
POWSize = 2

class Block:
    def __init__(self, index, timestamp, data, lastHash, proofOfWork):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.lastHash = lastHash
        self.proofOfWork = proofOfWork
        self.hash = self.genHash()


    def genHash(self):
        hashGenerator = hashlib.sha256()
        hashStr = str(self.index) + str(self.timestamp) + str(self.data)+ str(self.lastHash)
        hashGenerator.update(str.encode(hashStr))
        return hashGenerator.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        genesisBlock = Block(0, date.datetime.now(), "", "0", 0)
        self.chain.append(genesisBlock)
        self.lastBlock = genesisBlock
        print("Added block 0 (genesisBlock) with hash " + str(genesisBlock.hash))

    def writeHeader(self, f):
        header = {
            "versionNum" : 0.1,
            "blockHeight" : 0
        }
        f.write(str(header))
        f.write(str("\n"))

    def save(self, filename="./blockchain.bc"):
        if not os.path.isfile(filename):
            #write a header in new file
            bcFile = open(filename, 'w')
            self.writeHeader(bcFile)
        #write any new blocks to blockchain file
        for blocks in self.chain:
            bcFile.write("test\n")
        bcFile.close()

    def load(self, filename):
        if not os.path.isFile(filename):
            print("file does not exist. Could not load")

    def findPOW(self, data):
        if type(data) is not bytes:
            raise TypeError('Data argument needs to be of type \'bytes\'')
        #would be nice if Python had a do-while
        proofOfWork = 0
        powDigest = SHA256.new()
        print(type(data))
        powDigest.update(data)
        powDigest.update(bytes(proofOfWork))
        while powDigest.hexdigest()[0:POWSize] != '0'*POWSize:
            proofOfWork += 1
            powDigest = SHA256.new()
            powDigest.update(data)
            powDigest.update(bytes(proofOfWork))
        return proofOfWork


    def addBlock(self, data):
        if type(data) is not bytes:
            raise TypeError('Data argument needs to be of type \'bytes\'')
        print("Adding block. About to find proof of work....")
        proofOfWork = self.findPOW(data)
        nextBlock = Block(len(self.chain), date.datetime.now(), data, self.lastBlock.hash, proofOfWork)
        self.chain.append(nextBlock)
        self.lastBlock = nextBlock
        print("Added block " + str(nextBlock.index) +" with hash " + str(nextBlock.hash))
        print("proof of work was " + str(proofOfWork))

    def getBlockData(self, index):
        if index<0 or index>=len(self.chain):
            print("Error! Invalid index")
            return False
        return self.chain[index].data
