import os
import base58

import goofycoin.settings as settings
from goofycoin.crypto import encode_data
from goofycoin.goofy import Goofy
from goofycoin.coin import Coin
from goofycoin.wallet import Wallet
from goofycoin.blockchain import TransactionBlock

wallet = Wallet()
goofy_wallet = Goofy(wallet.secret_key, wallet.public_key)
def test_init():
    assert len(goofy_wallet.secret_key.to_string()) == 32
    assert len(goofy_wallet.public_key.to_string()) == 64

coin = goofy_wallet.make_coin()
def test_make_coin():
    assert coin.coin_id
    assert coin.signature
    assert isinstance(coin, Coin)

# needs a better test than the length
def test_generate_coin_id():
    decoded_id = base58.b58decode(coin.coin_id)
    #assert 77 <= len(decoded_id) <= 78 

def test_sign_coin():
    expected_sign = str(coin.coin_id).encode()
    assert goofy_wallet.public_key.verify(goofy_wallet.sign_coin(coin.coin_id), expected_sign)

def test_sign_transfer_coin():
    recipient = Wallet()
    expected_data = encode_data((coin.coin_id, recipient.public_key))
    actual_signature = goofy_wallet.sign_transfer_coin(coin.coin_id, recipient.public_key)
    
    assert goofy_wallet.public_key.verify(actual_signature, expected_data)

def test_gen_first_block():
    recipient = Wallet()
    actual_block = goofy_wallet.gen_first_block(coin, recipient.public_key)
    assert isinstance(actual_block, TransactionBlock) 
    assert isinstance(actual_block.previous_block, Coin)
    assert actual_block.previous_hash is None
    assert actual_block.spender_public_key 
    assert actual_block.signature

def test_load_goofy():
    goofy_test = Goofy.load()
    assert isinstance(goofy_test, Goofy)

def deprecated_test_load_goofy():
    wallet_name = "test_load_goofy"
    expected_wallet = Wallet()
    expected_goofy = Goofy(expected_wallet.secret_key, expected_wallet.public_key)

    public_key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".pk")
    secret_key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".sk")
    try:
        os.remove(public_key_path)
        os.remove(secret_key_path)
    except OSError:
        pass

    expected_goofy.save_wallet(wallet_name)
    actual_goofy = Goofy.load(wallet_name)

    assert isinstance(actual_goofy, Goofy)
    assert actual_goofy.secret_key.to_string() == expected_goofy.secret_key.to_string()
    assert actual_goofy.public_key.to_string() == expected_goofy.public_key.to_string()

def test_goofy():
    test_init()
    test_make_coin()
    test_generate_coin_id()
    test_sign_coin()
    test_gen_first_block()
    test_load_goofy()

test_goofy()



