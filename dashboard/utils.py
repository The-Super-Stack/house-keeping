import random
import string


def generate_code():
    letters = string.ascii_letters
    num = '0123456789'
    raw_password = letters + num
    password = ''.join(random.sample(raw_password, 16))
    return password

