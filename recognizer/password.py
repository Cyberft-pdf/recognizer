import random 
import string 

site = input("What website or app:")
email = input("What is the email/username:")

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password

generate_password = generate_password()

with open("password_manager.txt", "a") as f:
    data = site, email, generate_password
    f.write( "\n")
    f.write(str(data))
    f.write("\n")


print(f"New password is: {generate_password}")