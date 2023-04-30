# RSA repo
contains Tools for RSA usage

## NOTE
in most cases there are more possible inputs than they should.
- all numbers when using `main()` arem accepted; **not only** primes
- ...and more

# Install
## by git
**Advantage**: update possible by `git pull`

1. open git terminal
2. enter the command `git clone https://github.com/TobisMa/RSA`
   the git command will create a folder

## from Website
1. Clicking on the green button labeled `Code`
2. Clicking on `Download ZIP`
3. Extract the ZIP file locally


# Usage
Run the command `python -i main.py` in the folder of the file
This will open an interactive python terminal where the commands below are usable

## creating a key pair
`main()`

## creating a public key
`public_key(pN, N)`  
pN: $\varphi(N)$  
N: p*q  

## creating a private key
`private_key(pN, N, e)`  
pN: $\varphi(N)$  
N: p*q  
e: the left part of the public key  

## "Erweiterter eulkidischer Algorithmus"
`extgcd(a, b)`  
Prints the table calculation  
Returns `[x, y]`  

## generate primes until
`generate_primes(until: int)`  
Returns a list of primes excluding `until`  
