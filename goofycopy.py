import dill 
import json
from wallet import * 
from goofycoin import *

#Seed is for testing purposes.
random.seed(0)

class Goofy(Wallet):
    def __init__(self, secret_key, public_key):
        Wallet.__init__(self, secret_key, public_key)

    def make_coin(self):
        coin_id = self.generate_coin_id()
        coin_signature = self.sign_coin(coin_id)
        coin = Coin(coin_id, coin_signature)
        return coin

    def generate_coin_id(self):
        coin_id = str(random.getrandbits(256))
        coin_id = base58.b58encode(coin_id.encode())
        return coin_id

    def sign_coin(self, coin_id):
        return self.secret_key.sign(str(coin_id).encode())

    def sign_transfer_coin(self, coin, recipient_pk):
        return self.sign_transaction(recipient_pk, coin.coin_id)

# this fails if you are not the central authority.
with open('goofy-secret_key.pkl', 'rb') as file:
    goofy_secret_key = dill.load(file)

goofy = Goofy(goofy_secret_key, goofy_public_key)

# auxiliary
def make_coin_transfer(coin, recipient_pk, signature):
   return TransactionBlock(coin, None, goofy_public_key, recipient_pk, signature)  
