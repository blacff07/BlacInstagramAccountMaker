import random
import string

first_names = [
    "Rajesh", "Priya", "Amit", "Neha", "Vikram", "Sneha", "Rahul", "Anjali",
    "Suresh", "Deepa", "Manish", "Kavita", "Ravi", "Pooja", "Sanjay", "Meera",
    "Ajay", "Sunita", "Vijay", "Asha", "Anil", "Rekha", "Pankaj", "Jyoti",
    "Alok", "Madhuri", "Nitin", "Shilpa", "Tarun", "Usha", "Kunal", "Divya"
]

last_names = [
    "Sharma", "Verma", "Gupta", "Kumar", "Singh", "Patel", "Reddy", "Rao",
    "Yadav", "Jha", "Malhotra", "Mehta", "Choudhary", "Thakur", "Mishra",
    "Joshi", "Nair", "Menon", "Das", "Pandey", "Tiwari", "Dubey", "Khan",
    "Kapoor", "Khanna", "Sinha", "Saxena", "Kaur", "Arora", "Bansal", "Goyal"
]

def generate_username():
    base = random.choice(first_names).lower() + random.choice(last_names).lower()
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(2,4)))
    sep = random.choice(['.', '_', ''])
    username = base + sep + suffix
    return username[:30]

def generate_password():
    return "blac@123"

def generate_fullname():
    return f"{random.choice(first_names)} {random.choice(last_names)}"