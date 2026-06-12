import random, string, hashlib, time
def generate_device_id():
    return hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:16]
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))