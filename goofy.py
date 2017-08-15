import json
import random
import base58
from unittest.mock import patch

import settings
from wallet import Wallet 

class Coin(object):
    def __init__(self, coin_id, signature):
        self.coin_id = coin_id 
        self.signature = signature

    def __str__(self):
        return str(self.coin_id)

    def verify(self):
        try: 
            goofy_public_key.verify(self.signature, str(self.coin_id).encode())
            print("Coin is authentic.")
        except ecdsa.keys.BadSignatureError:
            print("Coin is fake.")

class Goofy(Wallet):
    def __init__(self, secret_key, public_key):
        Wallet.__init__(self, secret_key, public_key)

    def make_coin(self):
        coin_id = self.generate_coin_id()
        coin_signature = self.sign_coin(coin_id)
        coin = Coin(coin_id, coin_signature)
        return coin

    def generate_coin_id(self):
        coin_id = str(random.getrandbits(settings.coin_id_len))
        coin_id = base58.b58encode(coin_id.encode())
        return coin_id

    def sign_coin(self, coin_id):
        return self.secret_key.sign(str(coin_id).encode())

    def sign_transfer_coin(self, coin, recipient_pk):
        return self.sign_transaction(recipient_pk, coin.coin_id)

#goofy = Wallet.load('goofy.txt')
#goofy = Goofy(goofy.secret_key, goofy.public_key)

# auxiliary
#def make_coin_transfer(coin, recipient_pk, signature):
#   return TransactionBlock(coin, None, goofy_public_key, recipient_pk, signature)  
