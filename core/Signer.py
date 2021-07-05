import os
from Crypto.Hash import SHA1
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Signer:
    def __init__(self):
        self.keySize = 1024  # Minimum RSA modulus length must be >= 1024. Greater the better

        # Import the keys if already exists
        if (os.path.exists("private_pem.pem") and os.path.exists("public_pem.pem")):
            self._PRIVATE_KEY = RSA.import_key(
                open('private_pem.pem', 'r').read())
            self.PUBLIC_KEY = RSA.import_key(
                open('public_pem.pem', 'r').read())
            return

        # If file doesnt exist then generate a new pair
        self._PRIVATE_KEY = RSA.generate(self.keySize)
        self.PUBLIC_KEY = self._PRIVATE_KEY.public_key()

        # Convert the RsaKey object to string
        self._PRIVATE_KEY_string = self._PRIVATE_KEY.export_key().decode()
        self.PUBLIC_KEY_string = self.PUBLIC_KEY.export_key().decode()

        with open("private_pem.pem", "w+") as file:
            file.write(self._PRIVATE_KEY_string)

        with open("public_pem.pem", "w+") as file:
            file.write(self.PUBLIC_KEY_string)

        print("Key pair generated!")

    def sign(self, data):
        digest = SHA1.new()
        digest.update(data.encode())

        signer = PKCS1_v1_5.new(self._PRIVATE_KEY)
        sign = signer.sign(digest)

        return sign

    def verifySignature(self, dataDigest, sign: bytes):
        verifier = PKCS1_v1_5.new(self.PUBLIC_KEY)

        digest = SHA1.new()
        digest.update(dataDigest.encode())

        verified = verifier.verify(digest, sign)

        return verified
