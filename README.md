# RSA repo
contains Tools for RSA usage

## NOTE

`main()`:
- primes after 100000 are not checked, but assumed to be primes due to time efficiency

`public_key`:
- it is assumed `pN` and `N` are correct

`private_key`:
- parameters are not checked of correctness

`generate_primes`:
- it will exclude the `until` even though it is being calculated

`encrypt`, `decrypt`
- if the message is not within the allowed range, there will be no warning whatsoever

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
## cmd / Powershell, shell
Run the command `python -i rsa.py` in the folder of the file
This will open an interactive python terminal where the commands below are usable

## file
### Linux
run `rsa-tools` in terminal

### Windows
click on `rsa-tools.bat` in the folder. This will open a new window where you can enter the functions from below

# Functions
## creating a key pair
`main() -> Tuple[Tuple[int, int], Tuple[int, int]]`
Asks for p, q  
Asks for an e  
Prints the `extgcd($\varphi(N)$, e)` table  
Prints the public & private key
Returns: a tuple of the key tuples

### How to use this return
```python
public_key, private_key = main()

print(public_key)
print(private_key)
```
the values will be directly be accessable through "unpacking"

## creating a public key
`public_key(pN: int, N: int) -> Tuple[int, int]`  
_is asking for `e`_  
pN: $\varphi(N)$  
N: p*q  
Returns: the public key `(e, N)`

## creating a private key
`private_key(pN: int, N: int, e: int) -> Tuple[int, int]`  
pN: $\varphi(N)$  
N: p*q  
e: the left part of the public key  
Returns: the private key `(d, N)`

## "Extended Euclidean Algorithm"
`extgcd(a: int, b: int, as_equations=False) -> List[int]`  
_Prints the table or equation calculation_  
a, b: integers as input for the "Extended Euclidean Algorithm"  
as_equations: Switch between table and equations output. Defaults to table  
Returns: `[x, y]`  

### Directly as equations
`extgcd_eq(a, b) -> List[int]`  
_Prints the steps as equations_
a, b: integers as inputs for the algorithm
Returns: [x, y]

## generate primes until
`generate_primes(until: int) -> List[int]`  
Returns: a list of primes excluding `until` 

## encrypt a message
`encrypt(message: int, public_key: Tuple[int, int]) -> int`  
message: an integer  
key: a tuple in format `(e, N)`
Returns: the encrypted message

Example
```python
public_key = (47, 77)
secret_message = encrypt(3, public_key)  # 75
```

## decrypt data
`decrypt(message: int, private_key: Tuple[int, int]) -> int`  
message: the message to decrypt. For example from `encrypt`  
private_key: the private key in format `(d, N)`

Example
```python
private_key = (23, 77)
secret_message = decrypt(75, private_key)  # 3
```
