#simple blockchain.
from Crypto.Hash import SHA256
import hashlib #TODO still need? Convert to Crypto lib.
import datetime as date
global POWSize #proof of work size
POWSize = 2

#TODO multiple transactions per block
class Block:
    def __init__(self, index, timestamp, data, lastHash, proofOfWork):
        self.index = index
        self.timestamp = timestamp
        self.data = data #array of transactions
        self.lastHash = lastHash
        self.proofOfWork = proofOfWork
        self.hash = self.genHash()


    def genHash(self):
        hashGenerator = hashlib.sha256()
        hashGenerator.update(str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.lastHash))
        return hashGenerator.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        genesisBlock = Block(0, date.datetime.now(), "", "0", 0)
        self.chain.append(genesisBlock)
        self.lastBlock = genesisBlock
        print "Added block 0 (genesisBlock) with hash " + str(genesisBlock.hash)

    def findPOW(self, data):
        #would be nice if Python had a do-while
        proofOfWork = 0
        powDigest = SHA256.new()
        powDigest.update(str(data))
        powDigest.update(str(proofOfWork))
        while powDigest.hexdigest()[0:POWSize] != '0'*POWSize:
            proofOfWork += 1
            powDigest = SHA256.new()
            powDigest.update(str(data))
            powDigest.update(str(proofOfWork))
        return proofOfWork


    def addBlock(self, data):
        proofOfWork = self.findPOW(data)
        nextBlock = Block(len(self.chain), date.datetime.now(), data, self.lastBlock.hash, proofOfWork)
        self.chain.append(nextBlock)
        self.lastBlock = nextBlock
        print "Added block " + str(nextBlock.index) +" with hash " + str(nextBlock.hash)
        print "proof of work was " + str(proofOfWork)

    def getBlockData(self, index):
        if index<0 or index>=len(self.chain):
            print "Error! Invalid index"
            return False
        return self.chain[index].data
