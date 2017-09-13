import base58

from crypto import encode_data
from goofy import Goofy
from coin import Coin
from wallet import Wallet
from blockchain import TransactionBlock

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

def test_generate_coin_id():
    decoded_id = base58.b58decode(coin.coin_id)
    assert len(decoded_id) == 77

def test_sign_coin():
    expected_sign = str(coin.coin_id).encode()
    assert goofy_wallet.public_key.verify(goofy_wallet.sign_coin(coin.coin_id), expected_sign)

def test_sign_transfer_coin():
    recipient = Wallet()
    expected_data = encode_data(coin.coin_id, recipient_pk)
    actual_signature = goofy_wallet.sign_transfer_coin(expected_data)
    
    assert goofy_wallet.public_key.verify(actual_signature, expected_data)

def test_gen_first_block():
    recipient = Wallet()
    actual_block = goofy_wallet.gen_first_block(coin, recipient.public_key)
    assert isinstance(actual_block, TransactionBlock) 
    assert actual_block.prev_block == None
    assert actual_block.prev_hash == None
    assert actual_block.spender_pk 
    assert actual_block.sign

def test_load_goofy():
    key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name)
    wallet_name = "test_load_goofy"
    test_wallet = Wallet()
    test_goofy = Goofy

def test_goofy():
    test_init()
    test_make_coin()
    test_generate_coin_id()
    test_sign_coin()
    test_gen_first_block()

test_goofy()



