from blockchain import TransactionBlock
from wallet import Wallet

alice = Wallet()
bob = Wallet()
alice_sign = alice.sign_transaction(bob.public_key, "123")

prev_block = "dud"
block = TransactionBlock(prev_block, "123", alice.public_key, bob.public_key, alice_sign)
def test_init():
    assert block.previous_block
    assert block.previous_hash
    assert block.spender_public_key
    assert block.recipient_public_key
    assert block.signature
    assert block.hash

def test_str():
    pass

def test_generate_hash():
    actual_hash = block.generate_hash()
    assert len(actual_hash) == 77

def test_verify_chain():
    pass

def test_blockchain():
    test_init()
    test_str()
    test_generate_hash()

test_blockchain()
