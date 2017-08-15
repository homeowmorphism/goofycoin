# TO DO
# refactore your unit test code into a proper class.
# seed sign_transaction -- or seed ecdsa sign!!

from wallet import *
from goofycoin import *
from goofy import *
import goofy

import settings

import ecdsa

# imports entropy seed  
from ecdsa.util import PRNG

import random
from binascii import hexlify
from unittest.mock import patch

# patches
def seeded_randbits():
    random.seed(0)
    return random.getrandbits(settings.coin_id_len)

# tests
def test_wallet():
    saved_bob_str = 'secret key: 9f04dcc770eb29a4323b4d43de2b6cc8d258104379efeef7c36643fece996f96 \n public key: deea6364bb4445106eee6707815e6c8138bc08c6ca8d927235390c6519df9800aa52a80c6ec7665659ec47fb549e980c73d5d0fc6b13b528cb685d112f935871'

    anna = Wallet()
    anna.save_wallet('anna.txt')
    anna_copy = Wallet.load('anna.txt')
    assert anna.secret_key.to_string() == anna_copy.secret_key.to_string()
    assert anna.public_key.to_string() == anna_copy.public_key.to_string()
    
    bob = Wallet.load('bob.txt')
    assert str(bob) == saved_bob_str 

@patch('random.getrandbits', return_value =
seeded_randbits())
def test_goofy(mock_seeded_randbits):
    entropy_seed = PRNG("seed")
    saved_coin_id = '2bZcPUkdCaHuTfhdgGS4Cz96AAv4S5vqWaeHYH8YGUCXAxa5eXNSwbFTcpaAkK6JULZp7J1wj7LoFYACTooKYd2F7aAjiqJkvq1qJSjrnbA'
    saved_coin_signature = b'\xcb\xce\x0f\x84\xce]-\x19<\x8f\x19\xf6\xc0E\xb9\xf7\x00u\xe6\xddv\x14k\xeb\xcddR\xab\xb4\x00t\xeb\xc8Ej\x187w\x0c\xd4\xe4\xf9Cwh\xebT\xd2\xa5\t\xef4\xb1\xaaM\x9eir(@;\xec3\x8a'

    goofy_wallet = Wallet.load('goofy.txt')
    goofy_wallet = goofy.Goofy(goofy_wallet.secret_key,goofy_wallet.public_key)

    coin = goofy_wallet.make_coin()
    coin_signature = goofy_wallet.secret_key.sign(str(coin.coin_id).encode(), entropy = entropy_seed)
    #coin_transfer_signature = goofy_wallet.sign_transfer_coin(coin, bob.public_key)
    
    assert isinstance(coin, Coin) == True
    assert coin.coin_id == saved_coin_id 
    assert coin_signature == saved_coin_signature 
    #assert coin_transfer-signature

def test_goofycoin():
    saved_goofy_pk = None
    saved_signature = None

    signature = goofy_wallet.sign_transfer_coin(coin, anna.public_key)

    first_transaction = make_coin_transfer(coin, anna.public_key, signature)
    first_transaction.verify_chain()
    print(first_transaction.hash)

    second_transaction = TransactionBlock(first_transaction, first_transaction.hash, anna.public_key, bailey.public_key, anna.sign_transaction(bailey.public_key, first_transaction.hash)) 
    second_transaction.verify_chain()

    second_transaction = TransactionBlock(first_transaction, first_transaction.hash, goofy.public_key, bailey.public_key, anna.sign_transaction(bailey.public_key, first_transaction.hash)) 
    second_transaction.verify_chain()

def test_all():
    test_wallet()
    test_goofy()
    test_goofycoin()

#test_wallet()
#test_goofy()
#test_goofycoin()

test_all()
