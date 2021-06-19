from transaction import Transaction
from wallet import Wallet
from transactionPool import TransactionPool
from block import Block
from blockchain import Blockchain
from blockchainUtils import BlockchainUtils
from accountModel import AccountModel
from node import Node
import pprint
import sys

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])

    node = Node(ip, port)
    node.startP2P()
    node.startAPI(apiPort)