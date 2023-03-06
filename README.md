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
Asks for p, q  
Asks for an e  
Prints the `extgcd($\varphi(N)$, e)` table  
Prints the public & private key

## creating a public key
`public_key(pN: int, N: int)`  
_is asking for `e`_  
pN: $\varphi(N)$  
N: p*q  
Returns: the public key `(e, N)`

## creating a private key
`private_key(pN: int, N: int, e: int)`  
pN: $\varphi(N)$  
N: p*q  
e: the left part of the public key  
Retrusn: the private key `(d, N)`

## "Erweiterter eulkidischer Algorithmus"
`extgcd(a: int, b: int) -> List[int]`  
Prints the table calculation  
Returns `[x, y]`  

## generate primes until
`generate_primes(until: int) -> List[int]`  
Returns a list of primes excluding `until`  
