import random 
import string 
import sys

site = input("What website or app:")

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password

generate_password = generate_password()

with open("data.txt", "a") as f:
    data = site , generate_password
    f.write( "\n")
    f.write(str(data))
    f.write("\n")


print(f"New password is: {generate_password}")