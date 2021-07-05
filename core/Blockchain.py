from core.Activity import Activity, SignatureValidationError
from core.Block import Block
from core.Miner import Miner


class BlockChain:
    def __init__(self):
        self.chain = [self.generateGenesisBlock()]
        self.difficulty = 4
        self.pendingActivities = []
        print("Blockchain initiated\n\n")

    def generateGenesisBlock(self):
        # Genesis block with empty data and default hash
        return Block([Activity(None, "Genesis Block")])

    def addBlock(self):
        block = Block(self.pendingActivities)
        # Append future blocks to the chain
        block.previousBlockHash = self.getLastBlock().hash

        miner = Miner(block, self.difficulty)
        # Recalculate the blocks hash with the previous block hash
        block = miner.mine()
        self.chain.append(block)

        # Reset pending activities
        self.pendingActivities = []

        print(f"Block added\n")

    # def minePendingActivities(self):
    #     block = Block(self.pendingActivities)
    #     miner = Miner(block, self.difficulty)
    #     # Recalculate the blocks hash with the previous block hash
    #     block = miner.mine()

    #     self.chain.append(block)

    #     # Reset pending activities
    #     self.pendingActivities = []
    #     print(f"Block added\n")

    def addActivity(self, activity: Activity):
        if not (activity.fromAddress or activity.fromAddress == ""):
            if (activity.fromAddress != None):
                raise ValueError("No from address found")

        if not (activity.isValid()):
            raise ValueError("Activity is not valid")

        self.pendingActivities.append(activity)

    def getActivities(self):
        for block in self.chain:
            for activity in block.activities:
                print(activity)

    def getLastBlock(self):
        return self.chain[-1]

    def verifyIntegrity(self):
        # Iterate through the chain and calculate eash blocks hash
        # and previous blocks hash and verify it mathces with consecuent blocks
        for i in range(len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if not (currentBlock.verifyAllActivities()):
                raise SignatureValidationError(
                    f"Block has unsigned or invalid signature\nFailing block: {currentBlock}")

            if (currentBlock.hash != currentBlock.generateHash() and previousBlock.hash == currentBlock.previousBlockHash):
                print(f"Tampared block: {currentBlock}")
                print(
                    f"Block hash: {currentBlock.hash} | Original hash: {currentBlock.generateHash()}")
                raise ValueError("\nBlockchain tampered.")
        else:
            print("Blockchain is clean")

    def display(self):
        for block in self.chain:
            print(block.hash[0:7], block.activities)
