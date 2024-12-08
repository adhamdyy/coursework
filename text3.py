import random

# function checking credibility of prime number
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# function generating small prime number to test
def generate_prime(bits=8):
    while True:
        prime_candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1  # Ensure odd and of the correct size
        if is_prime(prime_candidate):
            return prime_candidate

# euclidean algorithm to compute the modular inverse
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# ElGamal Encryption Class
class ElGamal:
    def __init__(self, bits=8):  # bits reduced for faster testing
        # prime p and primitive root g generation
        self.p = generate_prime(bits)  # smaller prime number to test
        self.g = random.randint(2, self.p - 1)  # random generator g
        
        # choosing a secret key x
        self.x = random.randint(1, self.p - 2)  # secret key (private)
        
        # computing the public key y = g^x % p
        self.y = pow(self.g, self.x, self.p)  # public key
        
    def encrypt(self, message):
        """
        Encrypts the message using ElGamal encryption.
        The message must be an integer smaller than p.
        """
        if message >= self.p:
            raise ValueError(f"Message must be smaller than the prime p ({self.p}).")
        
        # random integer k for each encryption
        k = random.randint(1, self.p - 2)
        
        # computing the ciphertext components
        c1 = pow(self.g, k, self.p)  # first component: g^k % p
        c2 = (message * pow(self.y, k, self.p)) % self.p  # second component: m * y^k % p
        
        return (c1, c2)
    
    def decrypt(self, ciphertext):
        """
        Decrypts the ciphertext using the private key x.
        The ciphertext is a tuple (c1, c2).
        """
        c1, c2 = ciphertext
        
        # computing the modular inverse of c1^x % p
        s = pow(c1, self.x, self.p)
        s_inv = mod_inverse(s, self.p)  # using the modular inverse
        
        # message decryption
        message = (c2 * s_inv) % self.p
        return message

# example 
if __name__ == "__main__":
    # start ElGamal system
    elgamal = ElGamal(bits=8)  # using a smaller prime number for quicker testing
    
    # encrypted messsag (must be smaller than the prime p)
    message = 25 
    
    print(f"Original Message: {message}")
    
    # messafe encryption
    ciphertext = elgamal.encrypt(message)
    print(f"Ciphertext: {ciphertext}")
    
    # message decryption
    decrypted_message = elgamal.decrypt(ciphertext)
    print(f"Decrypted Message: {decrypted_message}")
