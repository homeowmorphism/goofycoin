import dill 
import json
from wallet import * 
from goofycoin import *

class Goofy(Wallet):
    def __init__(self, sk, pk):
        Wallet.__init__(self, sk, pk)

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
        return self.sk.sign(str(coin_id).encode())

    def sign_transfer_coin(self, coin, recipient_pk):
        return self.sign_transaction(recipient_pk, coin.coin_id)

# load goofy
with open('goofy-pk.pkl', 'rb') as file:
    goofy_pk = dill.load(file)

with open('goofy-sk.pkl', 'rb') as file:
    goofy_sk = dill.load(file)

goofy = Goofy(goofy_sk, goofy_pk)

# auxiliary
def make_coin_transfer(coin, recipient_pk, signature):
   return TransactionBlock(coin, None, goofy_pk, recipient_pk, signature)  
