from goofycoin.test_wallet import test_wallet
from goofycoin.test_goofy import test_goofy
from goofycoin.test_blockchain import test_blockchain

def test_all():
    test_wallet()
    test_goofy()
    test_blockchain()

test_all()
