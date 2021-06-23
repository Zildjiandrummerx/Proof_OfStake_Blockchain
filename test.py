from proofOfStake import ProofOfStake
from lot import Lot
import string
import random

def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString

if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update('bob', 10)
    pos.update('alice', 100)

    bobWins = 0
    aliceWins = 0

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == 'bob':
            bobWins += 1
        elif forger == 'alice':
            aliceWins += 1

    print('Bob Won: ' + str(bobWins) + ' times')
    print('Alice Won: ' + str(aliceWins) + ' times')