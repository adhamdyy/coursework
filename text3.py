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

# Euclidean algorithm to compute the modular inverse
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

# ElGamal encryption class
class ElGamal:
    def __init__(self, bits=8):
        # prime p and primitive root g generation
        self.p = generate_prime(bits)
        self.g = random.randint(2, self.p - 1)  # random generator g
        
        # choosing a secret key x
        self.x = random.randint(1, self.p - 2)  # secret key (private)
        
        # computing the public key y = g^x % p
        self.y = pow(self.g, self.x, self.p)  # public key
        
    def encrypt(self, message):
        """Encrypts the message using ElGamal encryption."""
        if message >= self.p:
            raise ValueError(f"Message must be smaller than the prime p ({self.p}).")
        
        # random integer k for each encryption
        k = random.randint(1, self.p - 2)
        
        # computing the ciphertext components
        c1 = pow(self.g, k, self.p)  # first component: g^k % p
        c2 = (message * pow(self.y, k, self.p)) % self.p  # second component: m * y^k % p
        
        return (c1, c2)
    
    def decrypt(self, ciphertext):
        """Decrypts the ciphertext using the private key x."""
        c1, c2 = ciphertext
        
        # computing the modular inverse of c1^x % p
        s = pow(c1, self.x, self.p)
        s_inv = mod_inverse(s, self.p)  # using the modular inverse
        
        # message decryption
        message = (c2 * s_inv) % self.p
        return message

# Main program logic
if __name__ == "__main__":
    # Get user input for the bit size of the prime number
    try:
        bits = int(input("Enter the bit size for the prime number (e.g., 8): "))
    except ValueError:
        print("Invalid input for bits size!")
        exit()

    # Create the ElGamal system with the given bits
    elgamal = ElGamal(bits=bits)

    # Display generated prime and public key
    print(f"Generated prime p: {elgamal.p}")
    print(f"Public key (g, y): ({elgamal.g}, {elgamal.y})")
    
    # Ask the user whether they want to encrypt or decrypt
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().lower()
    
    if choice == 'e':
        # Encrypt mode
        try:
            message = int(input(f"Enter the message to encrypt (must be an integer smaller than the prime p): "))
            if message < 0:
                raise ValueError("Message must be a non-negative integer.")
            ciphertext = elgamal.encrypt(message)
            print(f"Encrypted message (ciphertext): {ciphertext}")
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    elif choice == 'd':
        # Decrypt mode
        try:
            c1 = int(input("Enter the first ciphertext component (c1): "))
            c2 = int(input("Enter the second ciphertext component (c2): "))
            ciphertext = (c1, c2)
            decrypted_message = elgamal.decrypt(ciphertext)
            print(f"Decrypted message: {decrypted_message}")
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    else:
        print("Invalid choice. Please select 'E' for encryption or 'D' for decryption.")
