from transactionPool import TransactionPool
from wallet import Wallet
from blockchain import Blockchain
from socketCommunication import SocketCommunication

class Node():

    def __init__(self, ip, port):
        self.pep = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication()

    