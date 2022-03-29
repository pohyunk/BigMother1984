import time
import requests
import getpass
import telnetlib
import parse
import codecs
import csv
import multiprocessing
#import sys
#from imp import reload
#reload(sys)
#sys.setdefaultencoding("utf-8")

import telegram
import time

chat_token = "1402189467:AAHjNpA9_MAAsnhMpgJ22vq5iPrpS_dYUoo"
chat = telegram.Bot(token = chat_token)


AP_IP = '115.140.119.137'
PORT = '2333'
PERIOD = 60

sta_list = [['94:8b:', '마눌님'], ['0c:77:', '영서'], ['d0:b1:', '영훈']]
sta_stat = []
for idx in sta_list:
    sta_stat.append(0)

user400 = 'e400admin'
passwd400 = 'e400!kisan2019!'
user802 = 'e800admin'
passwd802 = 'e800!kisan2019!'
user410 = 'e410admin'
passwd410 = 'e410!kisan2019!'

def open_telnet_port(host_url):
	try:
		requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
		#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
		#r = requests.get("https://211.201.135.97:5010/?zuwufkxpfspt=2333", verify=False)
		r = requests.get(host_url + "?zuwufkxpfspt=" + PORT, verify=False, timeout=2)
	except requests.exceptions.ConnectionError:
		return 'ConnectionError'
	except requests.exceptions.ReadTimeout:
		#return 'ReadTimeout'
		return 'ConnectionError'
	return True

def run_script(host):
	if not host:
		return
	else:
		host_url = "https://" + str(host).strip() + ":5010/"
		
	"""	open telnet port
	"""
	ret = open_telnet_port(host_url)
	if (ret == 'ConnectionError'):
		host_url = "https://" + str(host).strip() + ":5300/"
		ret = open_telnet_port(host_url)
		if (ret == 'ConnectionError'):
			row = [host_url, 'Error (HTTP connect)']
			print(row)
			return
	elif (ret == 'ReadTimeout'):
		row = [host_url, 'Error (HTTP read)']
		print(row)
		return
	
	""" connect telnet
	"""
	try:
		tn = telnetlib.Telnet(host, port=PORT, timeout=2)
	except:
		row = [host_url, 'Error (Telnet connect)']
		print(row)
		return
	
	""" telnet login
	"""
	res = tn.read_until(b"login:", timeout=2)
	#print(res)
	if b"KIWI-E400 login:" in res:
		model = 'E400'
		tn.write(user400.encode('ascii') + b"\n")
	elif b"KIWI-E802 login:" in res:
		model = 'E802'
		tn.write(user802.encode('ascii') + b"\n")
	elif b"KIWI-E410 login:" in res:
		model = 'E410'
		tn.write(user410.encode('ascii') + b"\n")
	else:
		row = [host_url, 'Error (Telnet login prompt)']
		print(row)
		return
		
	res = tn.read_until(b"Password:", timeout=2)
	#print(res)
	if b"Password:" in res:
		if model == 'E400':
			tn.write(passwd400.encode('ascii') + b"\n")
		elif model == 'E410':
			tn.write(passwd410.encode('ascii') + b"\n")
		elif model == 'E802':
			tn.write(passwd802.encode('ascii') + b"\n")
	else:
		row = [host_url, 'Error (Telnet pw prompt)', model]
		print(row)
		return
		
	res = tn.read_until(b"~ #", timeout=2)
	#print(res)
	if b"~ #" not in res:
		row = [host_url, 'Error (Telnet login)', model]
		print(row)
		return

	""" run commands
	"""
	tn.write(b"wlanconfig ath0 list;")
	tn.write(b"wlanconfig ath1 list;")
	tn.write(b"wlanconfig ath2 list;")

	#tn.write(b"killall telnetd\n")
	tn.write(b"exit\n")
	
	try:
		res = tn.read_all()
		#print(res)
	except:
		row = [host_url, 'Error (Telnet)', model]
		print(row)
		return

	""" parse output
	"""
	#print(res)
	token = str(res).split('\\r\\n')
	#print (token)

	global sta_stat
	cur_stat = []
	for idx in sta_list:
		cur_stat.append(0)
 
	for i in range(len(token)):
		for idx, sta in enumerate(sta_list):
			res = parse.parse(sta[0]+"{}", token[i])
			if (res):
				cur_stat[idx] = 1
				continue

	for idx, sta in enumerate(sta_list):
		if (cur_stat[idx] != sta_stat[idx]):
			if (cur_stat[idx] == 1):
				msg = time.strftime('%m/%d %H:%M ') + sta[1] + " 들어오셨습니다!"
			else:
				msg = time.strftime('%m/%d %H:%M ') + sta[1] + " 나가셨습니다."
			print(msg)
			chat.sendMessage(chat_id = '199833049', text = msg)
			sta_stat[idx] = cur_stat[idx]

""" MAIN
"""
while(1):
	run_script(AP_IP)
	time.sleep(PERIOD)
