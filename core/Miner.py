import time
from core.Block import Block


class Miner:
    def __init__(self, block: Block, difficulty: int):
        self.block = block
        self.difficulty = difficulty

    def mine(self):
        expectedInitial = "".join(map(str, [0]*self.difficulty))

        start = time.time()
        # Recalculate the hash with varying nonce untill we get the desired
        # number of zeros before each blocks hash
        while (self.block.hash[0:self.difficulty] != expectedInitial):
            self.block.nonce += 1
            self.block.hash = self.block.generateHash()

        duration = time.time() - start

        print(f"Block mined: {self.block.hash} ({int(duration)} sec's)")
        return self.block
