import json
from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("secret.key", "rb").read()


def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()


def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")
    encrypted_password = encrypt_password(password)
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[website] = {"username": username, "password": encrypted_password.decode()}
    with open("passwords.json", "w") as file:
        json.dump(data, file)
    print("Password added successfully.")



def show_passwords():
    with open("passwords.json", "r") as file:
        data = json.load(file)
    for website, info in data.items():
        print(f"Website: {website}, Username: {info['username']}, Password: {decrypt_password(info['password'].encode())}")


def main():
    while True:
        print("\n1. Add Password\n2. Show Passwords\n3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            add_password()
        elif choice == "2":
            show_passwords()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


try:
    load_key()
except FileNotFoundError:
    generate_key()


if __name__ == "__main__":
    main()
