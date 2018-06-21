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


# Ledger
A ledger _implements_ a block chain. It is in charge of creating "tranasactions", and it should only create transactions once both parties have signed off on the transaction. It maintains a list of signed transactions until the list is large enough to create a block for the blockchain. The ledger also has load and save a ledger to a file with the .bc extension (BlockChain).

A ledger is made up of multiple tranasactions. The transactions have the following format for their data:
 * sender - The ID number of the sender
 * reciever - The ID number of the reciever
 * amount - the amount to be transferred
 * senderSig - Signature from the sender
 * recieverSig - Signature from the receiver
 * sendePubKey - Sender's public key, for validating the signature
 * receiverPubKey - Reciever's public key, for validating the signature


Ledger.py implements the following API:
_TODO API_

# Wallet
Wallet.py manages actions pertaining to the user's cryptocurrency wallet. Abstractly, a wallet is essentially just a public-private key pair. Wallet.py can create a .pem keyfile, and it supports import of a .pem file. Wallet.py will then use the public-private key pair to sign and verify transactions.

Wallet.py implements the following API:
_TODO API_