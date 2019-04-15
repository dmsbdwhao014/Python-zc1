

import getpass


username = input("username:").strip()
passwd = getpass.getpass()

print(username,passwd)