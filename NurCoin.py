import os
import hashlib
import time
import sys
import random
import getpass
import string
import pyfiglet
from cryptography.fernet import Fernet
import keyboard  # Importar la biblioteca keyboard
import pygame  # Importar pygame para efectos de sonido
import logging

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar Pygame Mixer para el sonido
pygame.mixer.init()
current_directory = os.path.dirname(os.path.abspath(__file__))
sound_file_path = os.path.join(current_directory, "NurCoin.wav")
coin_sound = pygame.mixer.Sound(sound_file_path)

# Definiciones de color usando códigos ANSI
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# ASCII Art for NurCoin Logo
NC_LOGO = """
{CYAN}
███╗░░██╗███████╗
████╗░██║██╔════╝   
██╔██╗██║██        
██║╚████║██
██║░╚███║███████╗
╚═╝░░╚══╝╚══════╝ 
{RESET}
""".format(CYAN=Colors.CYAN, RESET=Colors.RESET)



class Wallet:
    """
    Wallet class to manage NurCoin wallet operations.
    """
    def __init__(self, filename='wallet.txt'):
        self.filename = filename
        self.hash_filename = f'{filename}.hash'
        self.key_filename = f'{filename}.key'
        self.key = self.load_key()
        self.nurcoins = self.load_wallet()

    def load_key(self):
        """
        Load or generate a new encryption key for the wallet.
        """
        if os.path.exists(self.key_filename):
            with open(self.key_filename, 'rb') as key_file:
                return key_file.read()
        key = Fernet.generate_key()
        with open(self.key_filename, 'wb') as key_file:
            key_file.write(key)
        return key

    def encrypt_data(self, data):
        """
        Encrypt the given data using Fernet encryption.
        """
        f = Fernet(self.key)
        return f.encrypt(data.encode())

    def decrypt_data(self, data):
        """
        Decrypt the given encrypted data.
        """
        f = Fernet(self.key)
        return f.decrypt(data).decode()

    def load_wallet(self):
        """
        Load the wallet balance, verifying its integrity.
        """
        if os.path.exists(self.filename) and os.path.exists(self.hash_filename):
            with open(self.filename, 'rb') as file, open(self.hash_filename, 'rb') as hash_file:
                encrypted_content = file.read()
                decrypted_content = self.decrypt_data(encrypted_content)
                saved_hash = hash_file.read()
                if hashlib.sha256(decrypted_content.encode()).hexdigest() == saved_hash.decode():
                    return int(decrypted_content)
                logging.warning("Warning: Wallet file has been tampered with.")
                raise ValueError("Wallet file integrity compromised.")
        return 0

    def save_wallet(self):
        """
        Save the wallet balance with encryption and hashing for integrity.
        """
        encrypted_content = self.encrypt_data(str(self.nurcoins))
        with open(self.filename, 'wb') as file:
            file.write(encrypted_content)
        with open(self.hash_filename, 'w') as hash_file:
            hash_file.write(hashlib.sha256(str(self.nurcoins).encode()).hexdigest())

    def add_coins(self, amount):
        """
        Add coins to the wallet and save the new balance.
        """
        self.nurcoins += amount
        self.save_wallet()

    def get_balance(self):
        """
        Return the current balance of the wallet.
        """
        return self.nurcoins

def coins_to_dollars(coins):
    return coins * 0.000459

def load_difficulty(filename='difficulty.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read())
    return 3

def save_difficulty(difficulty, filename='difficulty.txt'):
    with open(filename, 'w') as file:
        file.write(str(difficulty))

def generate_wallet_address():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(40))

def display_motivational_message():
    messages = [
        "Mining in progress, your effort will pay off!",
        "Great things take time, keep going!",
        "Every NurCoin counts, you're doing great!",
        "Patience is the key to success in mining!",
        "Your NurCoins are growing, just like your skills!"
    ]
    return random.choice(messages)

def register_user():
    print("Registering a new user.")
    username = input("Enter a new username: ")
    password = getpass.getpass("Enter a new password: ")
    wallet_address = generate_wallet_address()
    with open('user_info.txt', 'w') as file:
        file.write(username + '\n')
        file.write(password + '\n')
        file.write(wallet_address + '\n')
    print("Registration complete. Your wallet address is:", wallet_address)
    return username, password

def login_user(username, password):
    with open('user_info.txt', 'r') as file:
        registered_username = file.readline().strip()
        registered_password = file.readline().strip()
        wallet_address = file.readline().strip()

    if username == registered_username and password == registered_password:
        print("Login successful!")
        print(f"Your wallet address is: {wallet_address}")
        return wallet_address
    else:
        logging.warning("Incorrect username or password. Please check your credentials.")
        return None

def login():
    while True:
        logging.info("NurCoin current price: $0.000459 USD .")
        print("Press 1 to create a new user.")
        print("Press 2 to login with an existing user.")
        choice = input("Enter your choice: ")

        print(f"{Colors.CYAN}{display_motivational_message():>70}{Colors.RESET}")

        if choice == '1':
            username, password = register_user()
            wallet_address = login_user(username, password)
            if wallet_address:
                return wallet_address
            else:
                print("Incorrect username or password. Please check your credentials and try again.")
        elif choice == '2':
            if not os.path.exists('user_info.txt'):
                logging.info("No registered users found. Please register first.")
            else:
               while True:
                   print("Please login.")
                   username = input("Enter your username: ")
                   password = getpass.getpass("Enter your password: ")
                   wallet_address = login_user(username, password)
                   if wallet_address:
                       return wallet_address
                   else:
                       print("Incorrect username or password. Please check your credentials and try again.")
                       
            print("Please login.")
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            wallet_address = login_user(username, password)
            return wallet_address
        else:
            print("Invalid choice. Please try again.")

def adjust_difficulty(start_time, blocks_found, difficulty, adjustment_factor=1.1, min_difficulty=1, max_difficulty=10):
    if blocks_found % 5 == 0:
        elapsed_time = time.time() - start_time
        avg_time_per_block = elapsed_time / blocks_found

        if avg_time_per_block < 10:
            new_difficulty = min(difficulty * adjustment_factor, max_difficulty)
            logging.info(f"Difficulty increased to: {new_difficulty}")
            difficulty = new_difficulty
        elif avg_time_per_block > 20 and difficulty > min_difficulty:
            new_difficulty = max(difficulty / adjustment_factor, min_difficulty)
            logging.info(f"Difficulty decreased to: {new_difficulty}")
            difficulty = new_difficulty

    return difficulty

def get_reward(hash_rate):
    return hash_rate * 2

def simulate_transaction():
    return f"Transaction: {random.randint(1000, 9999)}"

def wave_animation(step, pattern):
    return "".join(pattern[-step:] + pattern[:-step])

def play_coin_sound():
    try:
        coin_sound.play()
        
        pygame.time.wait(int(coin_sound.get_length() * 100))
    except Exception as e:
        logging.error(f"Error al reproducir el sonido: {e}")

def simulate_crypto_mining_nurcoin(wallet_address):
    wallet = Wallet()
    print("Connecting to the NurCoin Network...", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    time.sleep(2)

    print("\nEstablishing a secure connection with the NurCoin blockchain network...", end="")
    for _ in range(4):
        time.sleep(1)
        print(".", end="", flush=True)
    time.sleep(2)

    print("\nSynchronizing with the latest available block...", end="")
    for _ in range(5):
        time.sleep(1)
        print(".", end="", flush=True)
    time.sleep(2)
    
    wallet = Wallet()
    difficulty = load_difficulty()
    prefix_str = '0'*difficulty
    nonce = 0
    start_time = time.time()
    blocks_found = 0
    animation_step = 0
    pattern = [" ", " ", " ", " ", "█", "█", " ", " ", " ", " "]


    print(NC_LOGO + Colors.RESET)
    print(f"{Colors.GREEN}Welcome to the NurCoin Mining Software{Colors.RESET}")
    print("Connecting to the NurCoin Network...")
    print("Establishing a secure connection with the NurCoin blockchain network.")
    print("Synchronizing with the latest available block.")
    print(f"Miner Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Your wallet address is: {wallet_address}")
    print("Searching for hash solutions for the next block...")
    print(f"{Colors.GREEN}{'=' * 60}{Colors.RESET}")

    while True:
        if keyboard.is_pressed('w'):  # If 'W' key is pressed
            print(f"\n{Colors.YELLOW}Current balance of NurCoins: {wallet.get_balance()} (equivalent to ${coins_to_dollars(wallet.get_balance()):.2f} USD){Colors.RESET}")

        transactions = [simulate_transaction() for _ in range(5)]
        new_hash = hashlib.sha256(f'{nonce}'.encode()).hexdigest()
        hash_rate = random.randint(1, 100)


        animation_step = (animation_step + 1) % len(pattern)
        sys.stdout.write(f"\r{Colors.GREEN}Mining... {wave_animation(animation_step, pattern)}{Colors.RESET}")
        sys.stdout.flush()

            
        if nonce % 100 == 0:
            current_time = time.time()
            duration = time.strftime('%H:%M:%S', time.gmtime(current_time - start_time))
            temperature = random.randint(30, 80)
            print(f"\n{Colors.GREEN}{'-' * 60}{Colors.RESET}")
            print(f"{Colors.CYAN}Attempt {nonce}: Hash = {new_hash}{Colors.RESET}")
            print(f"Mining Speed: {hash_rate} hashes per second.")
            print(f"Current Session Duration: {duration}")
            print(f"Hardware Temperature: {temperature}°C")

        if new_hash.startswith(prefix_str):
            reward = get_reward(hash_rate)  # Amount of coins obtained by this block
            wallet.add_coins(reward)
            blocks_found += 1
            play_coin_sound()# Play coin sound

            print("\n" * 2) 
            
            success_message = pyfiglet.figlet_format("SUCCESS!", font="doom")
            print(f"{Colors.GREEN}{success_message}{Colors.RESET}")
            
            print("\n")  # Space after SUCCESS message
            
            # Información sobre el bloque minado exitosamente y las monedas obtenidas
            print(f"{Colors.GREEN}Success in mining NurCoin! Nonce: {nonce}{Colors.RESET}")
            print(f"{Colors.YELLOW}You mined {reward} NurCoins!{Colors.RESET}")  # Uso de la misma variable 'reward'
            print(NC_LOGO)
            print(f"{Colors.WHITE}NurCoin Hash: {new_hash}{Colors.RESET}")
            print(f"{Colors.YELLOW}Total NurCoins in wallet: {wallet.get_balance()}, which is equivalent to ${coins_to_dollars(wallet.get_balance()):.2f} USD{Colors.RESET}")
            
            difficulty = adjust_difficulty(start_time, blocks_found, difficulty)
            print(f"{Colors.MAGENTA}{'=' * 60}{Colors.RESET}")

        nonce += 1
        time.sleep(0.1)  # Interval between each mining attempt

    # Save the difficulty when exiting
    save_difficulty(difficulty)
    print(f"\n{Colors.RED}Time limit reached. Total NurCoins in wallet: {wallet.get_balance()}.{Colors.RESET}")

def verify_access_key():
# New SHA-256 hash for access key '1980'
    access_key_hash = '051c2e380d07844ffaca43743957f8c0efe2bdf74c6c1e6a9dcccb8d1a3c596b'
    attempt = getpass.getpass("Enter the access key to start NurCoin Miner: ")
    if hashlib.sha256(attempt.encode()).hexdigest() != access_key_hash:
        print("Incorrect access key. Exiting program.")
        sys.exit(0)
    else:
        print("Access key verified. Starting NurCoin Miner.")


def main():
    verify_access_key()
    print(NC_LOGO)
    print(f"{Colors.CYAN}Welcome to NurCoin, a cryptocurrency.{Colors.RESET}")
    wallet_address = login()
    print(f"{Colors.YELLOW}Good luck with your mining! Starting the NurCoin miner...{Colors.RESET}")
    simulate_crypto_mining_nurcoin(wallet_address)

if __name__ == "__main__":
    main()
