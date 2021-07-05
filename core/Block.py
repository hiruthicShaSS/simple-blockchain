from datetime import datetime
from typing import List
from core.Activity import Activity
from core.Signer import Signer
from Crypto.Hash import SHA1


class Block:
    def __init__(self, activities=[]):
        self.previousBlockHash = "0"
        self.timestamp = datetime.now().strftime("%d/%m/%Y")
        self.activities = activities
        self.nonce = 0
        self.hash = self.generateHash()
        genesis = ""
        if self.activities[0].data == "Genesis Block":
            genesis = "(Genesis)"
        print(f"Block generated: {self.hash} {genesis}")

    def __repr__(self):
        return f"(timestamp: {self.timestamp} | data: {self.activities})"

    def generateHash(self):
        blockString = self.timestamp + self.previousBlockHash + \
            str(self.activities) + str(self.nonce)

        digest = SHA1.new()
        digest.update(blockString.encode())
        return digest.hexdigest()

    def verifyAllActivities(self):
        for activity in self.activities:
            if (activity.data == "Genesis Block" and activity.fromAddress == None):
                return True
            if not (activity.isValid()):
                return False

        return True
