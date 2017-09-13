from blockchain import TransactionBlock
from wallet import Wallet
from goofy import Goofy

alice = Wallet()
goofy_wallet = Goofy.load()  
coin = goofy_wallet.make_coin()
first_block = goofy_wallet.gen_first_block(coin, alice.public_key)

bob = Wallet()
spender_pk = alice.public_key
recipient_pk = bob.public_key
prev_block = first_block
alice_sign = alice.sign_transaction(recipient_pk, prev_block)
second_block = TransactionBlock(prev_block, spender_pk, recipient_pk, alice_sign) 

def test_init():
    assert second_block.previous_block
    assert second_block.previous_hash
    assert second_block.spender_public_key
    assert second_block.recipient_public_key
    assert second_block.signature
    assert second_block.hash

def test_str():
    pass

def test_generate_hash():
    block_hash = first_block.generate_hash()
    assert len(block_hash) == 64 

    block_hash = first_block.generate_hash()
    assert len(block_hash) == 64 

def test_chain_is_authentic():
    print(first_block.chain_is_authentic())
    print(second_block.chain_is_authentic())
    fake_block = TransactionBlock(None, spender_pk, recipient_pk, alice_sign) 
    print(fake_block.chain_is_authentic())

def test_blockchain():
    test_init()
    test_str()
    test_generate_hash()
    test_chain_is_authentic()

test_blockchain()
