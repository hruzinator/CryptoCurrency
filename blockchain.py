#!/usr/bin/python3

# simple blockchain.
from Crypto.Hash import SHA256
import hashlib
import datetime as date
import os.path
import pickle

global POWSize  # proof of work size
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
        hashStr = str(self.index) + str(self.timestamp) + \
            str(self.data) + str(self.lastHash)
        hashGenerator.update(str.encode(hashStr))
        return hashGenerator.hexdigest()

    def getSerializedData(self):
        data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'lastHash': self.lastHash,
            'hash': self.hash,
            'proofOfWork': self.proofOfWork,
            'data': self.data
        }
        p = pickle.dumps(data)
        return p


class Blockchain:
    VERSION_NUMBER = 0.1

    def __init__(self):
        self.chain = []
        genesisBlock = Block(0, date.datetime.now(), b'', "0", 0)
        self.chain.append(genesisBlock)
        self.lastBlock = genesisBlock

    '''
    Header of the blockchain, which contains some metadata about it.
    Allows some space for miscilaenous data, but that data can't overwrite
    versionNum or blockHeight.
    '''
    def writeHeaderBytes(self, f, misc_metadata={}):
        header = misc_metadata
        header.update({
            "versionNum": self.VERSION_NUMBER,
            "blockHeight": len(self.chain)
        })
        headerBytes = pickle.dumps(header)
        f.write(headerBytes)

    def save(self, filename="./blockchain.bc", misc_metadata={}):
        # TODO handle appending to file so we don't have to rewrite the whole
        # blockchain every time
        bcFile = open(filename, 'wb')
        self.writeHeaderBytes(bcFile, misc_metadata)
        # write any new blocks to blockchain file
        for block in self.chain:
            blockBits = block.getSerializedData()
            bcFile.write(blockBits)
        bcFile.close()

    '''
    Note: this will clear the current blockchain loaded in memory
    '''
    def load(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError("file does not exist. Could not load")
        blockFile = open(filename, 'rb')
        header = pickle.load(blockFile)
        lastBlock = None
        self.chain = []
        for i in range(header['blockHeight']):
            blockData = pickle.load(blockFile)
            lastBlock = Block(i, blockData['timestamp'], blockData['data'],
                              blockData['lastHash'], blockData['proofOfWork'])
            self.chain.append(lastBlock)
        self.lastBlock = lastBlock
        blockFile.close()

    def findPOW(self, data):
        if type(data) is not bytes:
            raise TypeError('Data argument needs to be of type \'bytes\'')
        proofOfWork = 0
        powDigest = SHA256.new()
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
        proofOfWork = self.findPOW(data)
        nextBlock = Block(len(self.chain), date.datetime.now(), data,
                          self.lastBlock.hash, proofOfWork)
        self.chain.append(nextBlock)
        self.lastBlock = nextBlock

    def getBlockData(self, index):
        if index < 0 or index >= len(self.chain):
            return False
        return self.chain[index].data

    def getNumBlocks(self):
        return len(self.chain)
