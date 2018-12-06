import unittest
import blockchain
import datetime as date
import os.path

class BlockTests(unittest.TestCase):

	def test_create_block(self):
		ts = date.datetime.now()
		b = blockchain.Block(
			index = 0,
			timestamp = ts,
			data = b'Some test data',
			lastHash="0",
			proofOfWork=0
		)
		self.assertEqual(b.index, 0)
		self.assertEqual(b.timestamp, ts)
		self.assertEqual(b.data, b'Some test data')
		self.assertEqual(b.lastHash, "0")
		self.assertEqual(b.proofOfWork, 0)
		# test that hash of this block was generated
		self.assertTrue(b.hash)

	def test_getSerialiedData(self):
		b = blockchain.Block(
			index = 0,
			timestamp = date.datetime.now(),
			data = b'Some test data',
			lastHash="0",
			proofOfWork=0
		)
		self.assertTrue(b.getSerializedData())

class BlockchainTests(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.bcLoading = blockchain.Blockchain()
		self.bcLoading.save('./testLoad.bc')

	def test_addBlock(self):
		bc = blockchain.Blockchain()
		data = b'This is some data that will be added as a block'
		bc.addBlock(data)
		
	def test_getBlockData_ValidIndex(self):
		bc2 = blockchain.Blockchain()
		firstBlockData = b'This is the first block. Should have index 1'
		secondBlockData = b'This is the second block. Should have index 2'
		bc2.addBlock(firstBlockData)
		bc2.addBlock(secondBlockData)
		
		genesisBlock = bc2.getBlockData(0)
		firstBlock = bc2.getBlockData(1)
		secondBlock = bc2.getBlockData(2)
		self.assertNotEqual(genesisBlock, False)
		self.assertEqual(firstBlock, firstBlockData)
		self.assertEqual(secondBlock, secondBlockData)

	def test_getBlockData_InvalidIndex(self):
		bc3 = blockchain.Blockchain()
		self.assertFalse(bc3.getBlockData(78))

	def test_save(self):
		bc4 = blockchain.Blockchain()
		firstBlockData = b'This is the first block. Should have index 1'
		secondBlockData = b'This is the second block. Should have index 2'
		bc4.addBlock(firstBlockData)
		bc4.addBlock(secondBlockData)
		bc4.save('testSave.bc')
		self.assertTrue(os.path.isfile('./testSave.bc'))

	def test_save_extraMetadata(self):
		bc4 = blockchain.Blockchain()
		firstBlockData = b'This is the first block. Should have index 1'
		secondBlockData = b'This is the second block. Should have index 2'
		bc4.addBlock(firstBlockData)
		bc4.addBlock(secondBlockData)
		bc4.save('testSave2.bc', {'finances':{
				'Alice':0.001,
				'Bob':0.072
			}
		})
		self.assertTrue(os.path.isfile('./testSave2.bc'))

	def test_load(self):
		self.bcLoading.load('./testLoad.bc')

	@classmethod
	def tearDownClass(self):
		os.remove('./testLoad.bc')
		os.remove('./testSave.bc')
		os.remove('./testSave2.bc')

class LedgerTests(unittest.TestCase):
	pass

class WalletTests(unittest.TestCase):
	pass

class AppTests(unittest.TestCase):
	pass


# run the tests
if __name__ == '__main__':
    unittest.main()
