import uuid
import time
import copy

class Transaction():
    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = '' #Only the sender/owner of the private key is entitled to create transaction under his name

    # Will return a human readable form of the object when testing with MAIN.PY
    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self): # Avoids changing the original object and gets a consistant representation copy of the json obj.
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False