from datetime import datetime
from Crypto import PublicKey
from Crypto.Hash import SHA1
from core.Signer import Signer


class SignatureValidationError(Exception):
    pass


class Activity:
    def __init__(self, fromAddress, data):
        self.fromAddress = fromAddress
        self.data = str(data)
        self.timestamp = datetime.now().strftime("%d/%m/%Y")
        self.sign = None
        self.signer = Signer()

    def __repr__(self):
        return f"Activity(timestamp: {self.timestamp} | data: {self.data})"

    def generateHash(self):
        digest = SHA1.new()
        digest.update(
            (str(self.fromAddress) + self.data + self.timestamp).encode())

        return digest.hexdigest()

    def signActivity(self, key):
        # Check if the one who adds the activity is really the one that they seem
        # or simply put verify the identity. Because if some impersonates by using
        # others public key then it wouldnt math the private key.
        if (self.signer.PUBLIC_KEY.export_key().decode() != self.fromAddress):
            raise ValueError("Your public key doesnt match the from adderss")

        activityHash = self.generateHash()
        self.sign = self.signer.sign(activityHash)

    def isValid(self):
        if (self.sign == ""):
            raise SignatureValidationError("Activity is not signed!")

        # If the key is present then verify the identity
        activityHash = self.generateHash()
        return self.signer.verifySignature(activityHash, self.sign)
