import json
import random
import base58

import settings
from wallet import Wallet 
from coin import Coin
from blockchain import TransactionBlock
from crypto import encode_data

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
        encoded_data = encode_data((coin_id, recipient_pk))
        return self.secret_key.sign(encoded_data)

    def gen_first_block(self, coin, recipient_pk):
        prev_block = coin
        spender_pk = self.public_key
        sign = self.sign_transfer_coin(coin.coin_id, recipient_pk)

#        print("Coin " + str(coin) + " has been transferred to" + recipient_pk.to_string())
        return TransactionBlock(prev_block, spender_pk, recipient_pk, sign)

    @classmethod
    def load(cls):
        wallet_name = settings.GOOFY_FILENAME 
        wallet = Wallet.load_wallet(wallet_name)
        return Goofy(wallet.secret_key, wallet.public_key)
