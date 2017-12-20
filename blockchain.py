#simple blockchain

import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, lastHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.lastHash = lastHash
        self.hash = self.genHash()
        

    def genHash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index) 
            + str(self.timestamp)
            + str(self.data) 
            + str(self.lastHash))
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        genesisBlock = Block(0, date.datetime.now(), "", "0")
        self.chain.append(genesisBlock)
        self.lastBlock = genesisBlock
        print "Added block 0 (genesisBlock) with hash " + str(genesisBlock.hash)

    def addData(self, data):
        nextBlock = Block(len(self.chain), date.datetime.now(), data, self.lastBlock.hash)
        self.chain.append(nextBlock)
        self.lastBlock = nextBlock
        print "Added block " + str(nextBlock.index) +" with hash " + str(nextBlock.hash)

    def getBlockData(self, index):
        if index<0 or index>=len(self.chain):
            print "Error! Invalid index"
            return False
        return self.chain[index].data


#test the code
ledger = Blockchain()
ledger.addData("test")
ledger.addData(" another test")
print ledger.getBlockData(1)