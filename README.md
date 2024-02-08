NurCoin Mining Simulator

Welcome to the NurCoin Mining Simulator, an engaging Python application tailored for Windows users, simulating the intricate process of cryptocurrency mining. This simulator introduces the essentials of cryptographic hash generation, secure wallet management, dynamic difficulty adjustment, and more, centered around a fictional cryptocurrency called "NurCoin".

Features
Windows Compatibility: Designed specifically for the Windows operating system, ensuring smooth performance and compatibility.
Secure User Authentication: Safely register and log into your mining account. Initial access requires the key "1980" to start the mining simulation.
Encrypted Wallet Management: Your NurCoin balance is securely managed within an encrypted wallet, safeguarding your virtual earnings.
Dynamic Difficulty Adjustment: Experience realistic mining challenges with difficulty levels that adapt based on the network's performance.
Immersive Mining Experience: Enjoy audio feedback, colorful console output, and motivational messages, enhancing your mining journey.
User Data Management: Upon starting the mining script, a user_info.txt file is created, containing your username, password, and wallet address.
Real-Time Balance Display: Press the "w" key during mining to display your current NurCoin balance and its USD equivalent.
Getting Started
Prerequisites
Before running the NurCoin Mining Simulator on your Windows machine, ensure you have Python 3.x installed along with the following Python libraries:

pyfiglet
cryptography
keyboard
pygame
You can install all required libraries using pip:

bash
Copy code
pip install pyfiglet cryptography keyboard pygame
Installation
Clone this repository or download the source code to your Windows machine.
Ensure the NurCoin.wav sound file is in the same directory as the Python script for mining sound effects.
Navigate to the directory containing the program using Command Prompt or PowerShell.

Running the Simulator
Launch the simulator by executing:
bash
Copy code
python nurcoin_simulator.py
Input the initial access key "1980" to initiate the mining simulation.
Follow the on-screen instructions to register a new user or log in with an existing account.
File Structure
When initiated, the mining script generates the following files in your local environment:

user_info.txt: Stores your username, password, and wallet address.
wallet.txt: Holds your encrypted NurCoin balance, visible when pressing "w" during mining.
wallet.txt.hash: Used for verifying integrity and adjusting mining difficulty.
wallet.txt.key: Encrypts your wallet data using the password you've created.
Decryption
The wallet encryption ensures your NurCoin balance is secure. To decrypt and view your balance outside of the mining simulation, utilize the separate decryption tool provided in another repository, following its instructions for safe decryption.

Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests with bug fixes, new features, or documentation enhancements.

License
This project is open-source and licensed under the MIT License.
