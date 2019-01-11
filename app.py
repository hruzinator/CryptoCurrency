#!/usr/bin/python3

from wallet import Wallet
from ledger import Ledger
import os.path
import random

class App:
    def __init__(self):
        self.ledger = Ledger()
        self.userWallet = Wallet("./wallet.pem")
        uid = self.userWallet.getWID()
        if not self.ledger.checkUserInLedger(uid):
            self.ledger.addUserToLedger(uid)

    def checkCurrentBalance(self):
        print("In a cryptographic ledger, the amount of currency in " 
            +"every account is available for all account users to see" + 
            " (although the user behind the account can be anonymous). " +
             "Therefore, you may check other account balances as well, " +
              " if you would like.")
        
        print("What would you like to do?")
        print("1. Check my balance")
        print("1. Check another balance")
        option = input("Please select 1 or 2: ")
        while option not in ["1", "2"]:
            print("***Invalid. Please enter 1 or 2***")
            print("\nWhat would you like to do?")
            print("1. Check my balance")
            print("1. Check another balance")
            option = input("Please select 1 or 2: ")
        if option == "1":
            uid = self.userWallet.getWID()
            balance = self.ledger.checkBalance(uid)
            if balance is None:
                print("------")
                print("It appears that you do not have any transactions on the ledger yet.")
                print("------")
            else:
                print("------")
                print("Your account number is: " + uid)
                print("Your balance is " + str(balance))
                print("------")
        elif option == "2":
            uid = input("Please enter the ID of the account you would like to check: ")
            while not self.ledger.checkUserInLedger(uid):
                print("user not found in ledger")
                uid = input("Please enter the ID of the account you would like to check: ")
            balance = self.ledger.checkBalance(uid)
            if balance is None:
                print("------")
                print("It appears that this user does not have any transactions on the ledger yet.")
                print("------")
            else:
                print("------")
                print("The balance is " + str(balance))
                print("------")
            

    def sendMoney(self):
        data = {}
        data['sender'] = self.userWallet.getWID()
        data['receiver'] = input("Please enter the ID of the person you wish to send money to: ")
        if not self.ledger.checkUserInLedger(data['receiver']):
            print("We have no record of that user in the ledger. Please check the ID of the sender")
            return
        data['amount'] = float(input("Transaction amount: "))

        message = str(data['sender']) + str(data['receiver']) + str(data['amount'])
       
        data['senderPubKey'] = self.userWallet.getPublicKey().exportKey()
        data['senderSig'] = self.userWallet.signMessage(message)

        print("---Please confirm this trasaction---")
        print("Sender ID: " + data['sender'])
        print("Receiver ID: " + data['receiver'])
        print("Amount: " + str(data['amount']))
        print("\n")
        confirmation = input("Is this correct? Y/N ")
        if confirmation.upper() != "Y":
            print("Transaction not confirmed....exiting without adding to ledger")
            return

        result = self.ledger.addTransaction(data)
        print(result[1])

    def adminTestMenu(self):
        print("This is the admin test menu. Use this for practical testing.")
        if not os.path.exists('./test'):
            os.makedirs('./test')
        #load the test wallets
        testWallets = [Wallet('./test/'+f) for f in os.listdir('./test') if f.endswith('.pem')]
        print("Test wallet loading complete. " + str(len(testWallets)) + " test wallets loaded.")
        for w in testWallets:
            uid = w.getWID()
            if not self.ledger.checkUserInLedger(uid):
                self.ledger.addUserToLedger(uid)
        while True:
            print("")
            print("Please select an option from the list below...")
            print("1. Create test wallets")
            print("2. Create random transactions")
            print("3. Show current users")
            print("4. Return to admin menu")
            option = input("Please make a selection: ")
            if option == '1':
                num = int(input("how many test wallets do you want to create? "))
                amount = input("input an initial value for each wallet. You may leave blank for 0: ")
                if amount == "":
                    amount = 0
                else:
                    amount = float(amount)
                offset = 0
                for i in range(num):
                    filename = "./test/wallet" + str(i+offset) + ".pem"
                    while os.path.isfile(filename):
                        offset+=1
                        filename = "./test/wallet" + str(i+offset) + ".pem"
                    newWallet = Wallet(filename)
                    self.ledger.addUserToLedger(newWallet.getWID(), amount)
                    testWallets.append(newWallet)
            elif option == '2':
                numTransactions = int(input("how many random transactions do you want to generate? "))
                for t in range(numTransactions):
                    senderIdx = random.randint(0, len(testWallets)-1)
                    #Pick an ID that is not the sender in O(1) time
                    receiverIdx = random.randint(0, len(testWallets)-2)
                    if receiverIdx >= senderIdx:
                        receiverIdx += 1
                    data = {}
                    data['sender'] = testWallets[senderIdx].getWID()
                    data['receiver']= testWallets[receiverIdx].getWID()
                    data['amount'] = round(random.uniform(0, 2), 4)
                    data['senderPubKey'] = testWallets[senderIdx].getPublicKey().exportKey()

                    message = str(data['sender']) + str(data['receiver']) + str(data['amount'])
                    data['senderSig'] = testWallets[senderIdx].signMessage(message)

                    result = self.ledger.addTransaction(data)
                    print(data['sender'] +  " sent money to " + data['receiver'] + ". Amount: " + str(data['amount']))
                    if result[0] is False:
                        print(result[1])
            elif option == '3':
                for tw in testWallets:
                    print(tw.getWID())
            elif option == '4':
                return
            else:
                print("invalid option.")

    def adminMenu(self):
        print("Welcome to the admin menu, for testing purposes, this secret menu is included. It should not be included in any production version of the site.")
        while True:
            print("")
            print("Please select an option from the menu below: ")
            print("1. Add or remove money from an account")
            print("2. Show current state of the finance cache")
            print("3. Show size of the blockchain")
            print("4. Testing")
            print("5. Return to main menu")
            option = input("Please select an option: ")
            if option == '1':
                uid = input("account number to add currency to: ")
                while not self.ledger.checkUserInLedger(uid):
                    print("user not found in ledger")
                    uid = input("account number to add currency to: ")
                balance = self.ledger.checkBalance(uid)
                print("The balance in this account is " + str(balance))
                amount = input("Enter an amount. Positive numbers add value to the account. Negative numbers remove value: ")
                amount = int(amount)
                while(balance+amount<0):
                    print("That number would bring the account balance below 0, which we cannot do.")
                    amount = input("Enter an amount. Positive numbers add value to the account. Negative numbers remove value: ")
                self.ledger.addBlockReward(uid, amount)
                balance = self.ledger.checkBalance(uid)
                print("Operation completed. The balance of user " + str(uid) + " is " + str(balance))
            elif option == '2':
                cache = self.ledger.financeCache
                print("This is the current finance cache:")
                print(cache)
            elif option == '3':
                print("This is the current size of the blockchain, including the origin (genesis) block and not including any unapplied transactions: " 
                    + str(self.ledger.ledgerBlockchain.getNumBlocks()))
            elif option == '4':
                self.adminTestMenu()
            elif option == '5':
                return
            else:
                print("invalid option.")

    def mainMenu(self):
        while True:
            filename = input("Let's load a blockchain file to get started: ")
            if os.path.isfile(filename):
                print("loading file....")
                self.ledger.load(filename)
                break
            else:
                response = input("That file does not exist, would you like to create a new blockchain with that filename? Y/N ")
                if response.upper() == "Y":
                    break

        while True:
            print("Please select an option from the menu below:")
            print("1. Check current balance")
            print("2. Send Money")
            print("3. Quit")
            option = input("please select an option: ")
            if option == '1':
                self.checkCurrentBalance()
            elif option == '2':
                self.sendMoney()
            elif option == '3':
                break
            elif option == '99':
                # somewhat secret option for performing options we wouldn't normally allow.
                # this is just for demonstration purposes. Normally, this wouldn't be allowed
                self.adminMenu()
            else:
                print("Please input a valid option")

        saveQuestion = input("Would you like to save your ledger at " + filename + "? This will overwrite data there if it was there before. Y/N ")
        while saveQuestion not in ['Y', 'N', 'y', 'n']:
            print("Please just answer Y or N.")
            saveQuestion = input("Would you like to save your ledger at " + filename + "? This will overwrite data there if it was there before. Y/N ")
        if saveQuestion.upper() == 'Y':
            self.ledger.save(filename)
            print("Saved!")
        print("Goodbye!")


a = App()
a.mainMenu()

