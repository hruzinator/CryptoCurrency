This project assumes knowledge of how a Blockchain works. If you are unfamiliar, 3Blue1Brown has an amazing video on it! Check it out here: https://www.youtube.com/watch?v=bBC-nXj3Ng4. It's what this project is based off of!


# Blockchain
The blockchain is an abstract data type. It should not be confused with the ledger, which implements the blockchain to maintain a record of financial transactions. The Blockchain data type should be abstract enough that it could be applied for other uses.

Blockchain.py implements two objects:
1. Block - a single block in the blockchain. Contains:
 * an index field
 * a data segment
 * the hash of the last block
 * a field for the proof of work
2. Blockchain - array of blocks.

You can interact with the Blockchain as such:
Blockchain:
* load(filename): load a blockchain file into memory
* save(filenanme="./blockchain.bc"): save in-memory blockchain to a file


# Ledger
A ledger _implements_ a block chain. It is in charge of creating "tranasactions", and it should only create transactions once the sender signs off on the transaction. It maintains a list of signed transactions until the list is large enough to create a block for the blockchain. The ledger also has load and save a ledger to a file with the .bc extension (BlockChain).

A ledger is made up of multiple entries. Entries are of a certain type. The entries have the following format for their data:
1. Transaction Types
 * type - Field should be set to _transaction_
 * sender - The ID number of the sender
 * reciever - The ID number of the reciever
 * amount - the amount to be transferred
 * senderSig - Signature from the sender
 * senderPubKey - Sender's public key, for validating the signature
 2. Block Reward Types
 * type - Field should be set to _reward_
 * reciever - UID of the recipient
 * amount - the amount of block reward
 3. New User type
 * type - Field should be set to _newUser_
 * reciever - UID of new user
 * amount - starting balance


Ledger.py implements the following API:
_TODO API_

# Wallet
Wallet.py manages actions pertaining to the user's cryptocurrency wallet. Abstractly, a wallet is essentially just a public-private key pair. Wallet.py can create a .pem keyfile, and it supports import of a .pem file. Wallet.py will then use the public-private key pair to sign and verify transactions.

Wallet.py implements the following API:
_TODO API_

# Blockchain file
I have picked the .bc file extension to use as my blockchain file format. Because of the large amounts of data stored in blockchains, I am opting to store data in a serialized manner. The file starts with a header, indicating blockchain version and the block height. This "metadata" is serialzed. This is follwed by serialized Block objects.