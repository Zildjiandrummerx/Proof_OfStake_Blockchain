from blockchain import Blockchain
from transactionPool import TransactionPool
from wallet import Wallet
from socketCommunication import SocketCommunication
from nodeAPI import NodeAPI
from message import Message
from blockchainUtils import BlockchainUtils

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
        if not transactionExists and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector,'TRANSACTION', transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired:
                self.forge()

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("I'm the next forger")
        else:
            print("I'm not the next forger")