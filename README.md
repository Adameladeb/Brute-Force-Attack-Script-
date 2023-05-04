🔍 Brute-Force Attack Script 🔍

🔐 This Python script performs brute-force attacks against common protocols such as SSH, FTP, and HTTP.

👤 It takes the target hostname or IP address, port number, username, password file, and an optional proxy as input.

📝 The script reads a list of passwords from a file and loops over them, attempting to log in using the provided username and each password in turn.

🛡️ The script includes a mechanism to detect and handle lockouts, where a certain number of failed login attempts trigger a temporary pause in the attack.

🌐 The script uses the Requests library to make HTTP requests and includes support for proxy servers.

👨‍💻 Written in Python, this script provides a simple and customizable solution for testing the security of target systems.
