import telnetlib
import getpass

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"cd /home\n")
tn.write(b"ls\n")
tn.write(b"exit\n")

tn.read_until(b"$").decode('ascii')
print(tn.read_all().decode('ascii'))