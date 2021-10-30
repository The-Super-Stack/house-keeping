import random
import string


def generate_code():
    letters = string.ascii_letters
    num = '0123456789'
    raw_password = letters + num
    password = ''.join(random.sample(raw_password, 16))
    return password


def spv_code_generator():
    letters = string.ascii_letters
    num = '0123456789'
    raw_password = letters + num
    password = ''.join(random.sample(raw_password, 8))
    return password
