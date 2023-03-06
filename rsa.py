import math
from random import randint

def generate_primes(until):
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


def extgcd(a, b):
	table = []
	r = -1
	while r != 0:
		q = a // b
		r = a % b
		table.append([a, b, q, r])
		a = b
		b = r
	table[-1].extend([0, 1])
	for i in range(2, len(table)+1):
		table[-i].extend([table[-i+1][5], table[-i+1][4] - table[-i][2] * table[-i+1][5]])
	
	print("a\tb\tq\tr\tx\ty")
	for line in table:
		print('\t'.join(map(str, line)))		
	return table[0][-2:]	

def public_key(pN, N):
	possible_primes = list(filter(lambda x: math.gcd(N,x) == 1, generate_primes(pN)))
	print("Moegliche primes:", possible_primes)
	flag = True
	while flag or math.gcd(e, N) != 1:
		if not flag:
			print("Not a valid value for e: %s" % e)
		e = int(input("Choose: "))
		flag = False	
	return (e % pN, N)

def private_key(pN, N, e):
	xy = extgcd(e, pN)
	return (xy[0] % pN, N)


def main():
	p = int(input("Primzahl 1: "))
	q = int(input("Primzahl 2: "))
	if p == q:
		return "p and q may not be equal."
	N = p * q
	pN = (p - 1) * (q - 1)
	
	pub_key = public_key(pN, N)
	priv_key = private_key(pN, N, pub_key[0])
	
	print("public key:", pub_key)
	print("private key:", priv_key)

