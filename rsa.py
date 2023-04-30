import math
from random import randint
import sys
from typing import List, Tuple, Union

HUNDRED_THOUSAND = 100_000


def generate_primes(until: int) -> List[int]:
    primes = [2]
    checkN = 3
    sqrtN = 1
    t = -1
    while primes[-1] < until:
        if (checkN % 5 != 0 or checkN == 5):
            for cprime in primes:
                t = checkN % cprime
                if (cprime > sqrtN or t == 0):
                    break
            if (sqrtN + 1) * (sqrtN + 1) < checkN:
                sqrtN += 1
            if t != 0:
                primes.append(checkN)
        checkN += 2
    return primes[:-1]



def extgcd(a: int, b: int, *, eq: bool = False) -> List[int]:
    if eq:
        out = str_extgcd(a,b)
        print(out[0])
        return out[1]

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

    if not eq:
        print("a\tb\tq\tr\tx\ty")
        for line in table:
            print('\t'.join(map(str, line)))
    return table[0][-2:]

def str_extgcd(a: int, b:int) -> List:
    r = b
    steps = []
    equations = []

    #euclidean
    while True:
        q = a//b
        if a%b == 0:
            break
        r = a % b


        steps.append([a,q,b,r])
        equations.append(f"{a}={q}*{b}+{r}")

        a = b
        b = r

    equations.append(f"{a}={q}*{b}+0")
    equations.append("")

    #extension
    x = 1
    a = steps[-1][0]
    y = steps[-1][1]*-1

    equations.append(f"{r}={x}*{a}+{y}*{b}")

    for i in range(len(steps)-1):
        b = a
        a = steps[-2-i][0]
        _y = y
        y = x + (steps[-2-i][1]*-1)*y
        x = _y
        equations.append(f"{r}={x}*{a}+{y}*{b}")


    equations = "\n".join(equations).replace("+-","-").replace("*","\u2022")

    return [equations,[x,y]]

def public_key(pN: int, N: int) -> Tuple[int, int]:
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

    return (e % pN, N)


def private_key(pN: int, N: int, e: int) -> Tuple[int, int]:
    xy = extgcd(e, pN)
    return (xy[0] % pN, N)


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
