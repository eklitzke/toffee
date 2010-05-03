import random
import string

def random_email():
    return ''.join(random.choice(string.letters) for x in range(20)).lower() + '@example.com'
