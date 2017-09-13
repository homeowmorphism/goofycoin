from test_wallet import test_wallet
from test_goofy import test_goofy
from test_blockchain import test_blockchain

def test_all():
    test_wallet()
    test_goofy()
    test_blockchain()

test_all()
