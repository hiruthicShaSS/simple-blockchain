from Crypto.Hash import SHA1
from core.Activity import Activity
from core.Blockchain import BlockChain
from core.Signer import Signer

signer = Signer()
myPublicKey = signer.PUBLIC_KEY.export_key().decode()

blockchain = BlockChain()

activity1 = Activity(fromAddress=myPublicKey,
                     data="I am writing a new article right now")
activity1.signActivity(myPublicKey)
blockchain.addActivity(activity1)

activity2 = Activity(fromAddress=myPublicKey, data="Just finished my lunch")
activity2.signActivity(myPublicKey)
blockchain.addActivity(activity2)

activity3 = Activity(fromAddress=myPublicKey,
                     data="I am gonna play valorant...")
activity3.signActivity(myPublicKey)
blockchain.addActivity(activity3)
blockchain.addBlock()


blockchain.display()

blockchain.verifyIntegrity()
