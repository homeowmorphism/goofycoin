# Goofycoin 

*Status: Almost done!*

A toy implementation of a cryptocurrency, as described in [Bitcoin and Cryptocurrency Technologies](http://bitcoinbook.cs.princeton.edu/).

## Dependencies
- Python 3
- base58, ecdsa

## Security 
* Goofycoin was written as a toy project by a non-cryptographer. (Enough said)
* Goofycoin depends on the ecdsa library, which is does not protect against timing attacks. 

## Still Left To Do
- Move the folders around. 
- Fix circular dependency with Wallet and goofy_pk.
- (Would be nice to have a user interface for this but not sure what the best way to do this is.)
