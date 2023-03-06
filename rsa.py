from ast import Mod
import math
from random import randint
import sys
from typing import Generic, List, Tuple, TypeVar, Union

HUNDRED_THOUSAND = 100_000

def generate_primes(until: int) -> List[int]:
    """Generates primes until the given number (excluding the given number)

    Args:
        until (int): the number to limit the primes generation

    Returns:
        List[int]: the collection of primes until the given limit (excluding the limit)
    """
    primes = [2]
    checkN = 3
    sqrtN = 1
    t = -1
    while primes[-1] < until:
        if checkN % 5 != 0 or checkN == 5:
            for cprime in primes:
                t = checkN % cprime
                if cprime > sqrtN or t == 0:
                    break
            if (sqrtN + 1) * (sqrtN + 1) < checkN:
                sqrtN += 1
            if t != 0:
                primes.append(checkN)
        checkN += 2
    return primes[:-1]


def extgcd(a: int, b: int, *, as_equations: bool = False) -> List[int]:
    """Calculates extended euclidean algorithm of a and b and prints the steps to the solution

    Args:
        a (int): the first argument
        b (int): the second argument
        as_equations (bool, optional): When enabled passes the arguments to `extgcd_eq`. Defaults to False.

    Returns:
        List[int]: in format [x, y]
    """
    if as_equations:
        out = extgcd_eq(a, b)
        return out

    table = []
    r = -1
    while r != 0:
        q = a // b
        r = a % b
        table.append([a, b, q, r])
        a = b
        b = r
    table[-1].extend([0, 1])
    for i in range(2, len(table) + 1):
        table[-i].extend([table[-i + 1][5], table[-i + 1][4] - table[-i][2] * table[-i + 1][5]])

    # won't happen because it returns if eq==True
    print("a\tb\tq\tr\tx\ty")
    for line in table:
        print('\t'.join(map(str, line)))
    return table[0][-2:]


def extgcd_eq(a: int, b: int) -> List[int]:
    """Same as `extgcd`, but it prints the equations 

    Args:
        a (int): the first argument
        b (int): the second argument

    Returns:
        List[int]: in format [x, y] 
    """
    r = b
    steps = []
    equations = []

    # euclidean
    while True:
        q = a // b
        if a % b == 0:
            break
        r = a % b

        steps.append([a, q, b, r])
        equations.append(f"{a}={q}*{b}+{r}")

        a = b
        b = r

    equations.append(f"{a}={q}*{b}+0")
    equations.append("")

    # extension
    x = 1
    a = steps[-1][0]
    y = steps[-1][1] * -1

    equations.append(f"{r}={x}*{a}+{y}*{b}")

    for i in range(len(steps) - 1):
        b = a
        a = steps[-2 - i][0]
        _y = y
        y = x + (steps[-2 - i][1] * -1) * y
        x = _y
        equations.append(f"{r}={x}*{a}+{y}*{b}")

    equations = "\n".join(equations).replace("+-", "-").replace("*", "\u2022")
    print(equations)
    return [x, y]


def public_key(pN: int, N: int) -> Tuple[int, int]:
    """Creates a public key using phi(N), N and a user decidable e

    Args:
        pN (int): phi(N)
        N (int): the product of `p` and `q`

    Returns:
        Tuple[int, int]: the public key in format `(e, N)`
    """
    possible_primes = list(filter(lambda x: math.gcd(N, x) == 1, generate_primes(pN)))
    print("Primes within range:", possible_primes)
    flag = True
    while flag or math.gcd(e, N) != 1:
        if not flag:
            print("Not a valid value for e: %s" % e, file=sys.stderr)
        flag = False
        e = int(input("Choose: "))
        if isinstance(e, float):
            print("Expecting integer; got %s" % type(e).__name__, file=sys.stderr)
            flag = True
        elif e < 0:
            print("WARNING: negative e; instead e %% %s = %s will be used" % (pN, e % pN))
            e %= pN
        elif e <= 1:
            print("Invalid values for e: zero and one", file=sys.stderr)

    return (e, N)


def private_key(pN: int, N: int, e: int, mod_d: bool = True) -> Tuple[int, int]:
    """generating a private key using phi(N), N and e from the public key
       If d will be a negative value it will be taken care of by this function per default
       
    Args:
        pN (int): phi(N)
        N (int): the product of p and q
        e (int): the left part of the public key
        mod_d (bool): when disabled the d-part of this key may return negative values. Defaults to True.

    Returns:
        Tuple[int, int]: the provate key in format `(d, N)`
    """
    xy = extgcd(e, pN)
    d = xy[0]
    if mod_d:
        d %= pN
    return (d, N)


def encrypt(message: Union[str, int], *public_keyset) -> Union[List[int], int]:
    """Exncrypts data which is either string or number

    Args:
        message (int | str): Either a number or a string

    Raises:
        ValueError: if the passed input is invalid

    Returns:
        List[int] | int: the encrypted data. As list of integers if the input was a string. 
        if the input was an integer the encrypted integer will be returned
    """
    if len(public_keyset) == 1 and isinstance(public_keyset[0], (list, tuple)):
        public_keyset = public_keyset[0]
    elif len(public_keyset) != 2:
        raise ValueError("Please provide a key")
    if isinstance(message, str):
        return [encrypt(ord(x), *public_keyset) for x in message]  # type: ignore

    return (message ** public_keyset[0]) % public_keyset[1]


def decrypt(message_to_decrypt: Union[List[int], int], *private_keyset) -> Union[str, int]:
    """Decrpyts data which has been encrypted

    Args:
        message_to_decrypt (List[int] | int): the encrypted message. Either a list of integers or the only an integer

    Raises:
        ValueError: if the passed arguments are invalid

    Returns:
        str | int: the decrypted string or decrypted number
    """
    if len(private_keyset) == 1 and isinstance(private_keyset[0], (list, tuple)):
        private_keyset = private_keyset[0]
    elif len(private_keyset) != 2:
        raise ValueError("Please provide a key")
    if isinstance(message_to_decrypt, int):
        return (message_to_decrypt ** private_keyset[0]) % private_keyset[1]
    return ''.join(map(chr, (decrypt(x, *private_keyset) for x in message_to_decrypt)))


def main() -> Union[Tuple[Tuple[int, int], Tuple[int, int]], str]:
    first_million_primes = generate_primes(HUNDRED_THOUSAND)
    p = int(input("Primzahl 1: "))
    if p < 0:
        return "No negative prime"
    elif p > HUNDRED_THOUSAND:
        print("WARNING: prime value will not be checked", file=sys.stderr)
    elif p not in first_million_primes:
        return "p is not prime"

    q = int(input("Primzahl 2: "))
    if q < 0:
        return "No negative prime"
    elif p > HUNDRED_THOUSAND:
        print("WARNING: prime value will not be checked", file=sys.stderr)
    elif p not in first_million_primes:
        return "q is not prime"
    elif p == q:
        return "p and q may not be equal."

    N = p * q
    pN = (p - 1) * (q - 1)

    pub_key = public_key(pN, N)
    priv_key = private_key(pN, N, pub_key[0])

    print("public key:", pub_key)
    print("private key:", priv_key)

    return pub_key, priv_key
