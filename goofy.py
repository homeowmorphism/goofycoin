import json
import random
import base58

import settings
from wallet import Wallet 
from coin import Coin

class Goofy(Wallet):
    def __init__(self, secret_key, public_key):
        Wallet.__init__(self, secret_key, public_key)

    def make_coin(self):
        coin_id = self.generate_coin_id()
        coin_signature = self.sign_coin(coin_id)
        coin = Coin(coin_id, coin_signature)
        return coin

    def generate_coin_id(self):
        coin_id = str(random.getrandbits(settings.coin_id_size))
        coin_id = base58.b58encode(coin_id.encode())
        return coin_id

    def sign_coin(self, coin_id):
        encoded_id = str(coin_id).encode()
        return self.secret_key.sign(encoded_id)

    def sign_transfer_coin(self, coin_id, recipient_pk):
        encoded_data = encode_data(coin.coin_id, recipient_pk)
        return self.sign_transaction(encoded_data)

    def gen_first_block(self, coin, recipient_pk):
        prev_block = None
        prev_hash = None
        spender_pk = self.public_key
        sign = self.sign_transfer_coin(coin.coin_id, recipient_pk)
        return TransactionBlock(prev_block, prev_hash, spender_pk, recipient_pk, sign)

    @classmethod
    def load_goofy(cls, wallet_name):
        goofy_wallet = Wallet.load_wallet(wallet_name)
        return Goofy(wallet.secret_key, wallet.public_key)

# auxiliary
#def make_coin_transfer(coin, recipient_pk, signature):
#   return TransactionBlock(coin, None, goofy_public_key, recipient_pk, signature)  
