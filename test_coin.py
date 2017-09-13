from coin import Coin
from wallet import Wallet
from goofy import Goofy
from load_central_authority import load_goofy_public_key

casual_coin = Coin("123", "signature")
def test_init():
    assert casual_coin.coin_id
    assert casual_coin.signature

def test_str():
    pass

def test_verify():
    fake_goofy = Wallet()
    fake_goofy = Goofy(fake_goofy.secret_key, fake_goofy.public_key)
    fake_coin = fake_goofy.make_coin()

    real_goofy = Wallet.load_wallet("goofy")
    real_goofy = Goofy.load_goofy(real_goofy)
    real_coin = real_goofy.make_coin()
    
    expected_out = str(real_coin.coin_id) + " : Valid."
    assert real_coin.verify() == expected_out

    expected_out = str(fake_coin.coin_id) + " : Invalid, bad signature."
    assert fake_coin.verify() == expected_out


def test_coin():
    test_init()
    #test_str()
    test_verify()

test_coin()
