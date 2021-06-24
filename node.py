from jsonpickle.pickler import encode
from blockchain import Blockchain
from transactionPool import TransactionPool
from wallet import Wallet
from socketCommunication import SocketCommunication
from nodeAPI import NodeAPI
from message import Message
from blockchainUtils import BlockchainUtils
import copy

class Node():

    def __init__(self, ip, port, key = None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        if key is not None:
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector,'TRANSACTION', transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired:
                self.forge()

    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionValid = self.blockchain.transactionsValid(block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)
        if not blockCountValid:
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def requestChain(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.broadcast(encodedMessage)

    def handleBlockchainRequest(self, requestingNode):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)

    def handleBlockchain(self, blockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)
        if localBlockCount < receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("I'm the next forger")
            block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print("I'm not the next forger")