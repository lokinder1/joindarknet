from subprocess import call,Popen,PIPE
import socket
import time
import sys

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

def header():
	print( bcolors.OKGREEN +'---------------------------------'+bcolors.ENDC )
	print( bcolors.FAIL +'-----------JOINDARKNET-----------'+bcolors.ENDC )
	print( bcolors.WARNING +'NOTE:Tor and Apache2 must be installed\n[1]To Install Tor:sudo apt-get install tor\n[2]To install apache2:sudo apt-get update && sudo apt-get install apache2'+bcolors.ENDC )
	print( bcolors.OKGREEN +'---------------------------------'+bcolors.ENDC )

def localip():
	####to get LAN ip of your system
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
	local_ip_address = s.getsockname()[0]
	return local_ip_address
	####to get LAN ip of your system


def edittorrc(local_ip_address):
	####to write on torrc file
	firstline='\nHiddenServiceDir /var/lib/tor/hidden_service\n'
	secondline='HiddenServicePort 80 '+ local_ip_address+':80\n'
	
	with open('/etc/tor/torrc') as f:
		if secondline not in f:
			f.close()
			with open('/etc/tor/torrc','a') as fw:
				fw.writelines(firstline)
				fw.writelines(secondline)
		else:
			print()

	####to write on torrc file

def isnotRunning():
	#Get all running processes and search for "tor" within them
	#The "[" and "]" are used to execlude ps and grep from the returned result.
	CLIResult = Popen(['ps aux | grep -w [t]or'],shell=True,stdout=PIPE)
	#If no processes was found(= Tor is not running..)
	if(CLIResult.stdout.read()):
		return 0
	
	return 1



def starttor():
	####to start tor service
	if(isnotRunning()):
		Popen("tor",shell=True)
		print(bcolors.OKBLUE+(bcolors.OKGREEN +'[+]'+bcolors.ENDC)+'tor service started...\n'+bcolors.ENDC)
	else:
		print((bcolors.WARNING +'[-]'+bcolors.ENDC)+'Tor already running')
	####to start tor service

def startapache():
####to start apache service
	Popen(["service","apache2","restart"], stdout=PIPE)
	#output = p1.communicate()[0]
	#print(output)
	#call(["service","apache2","restart"])
	print(bcolors.OKBLUE+(bcolors.OKGREEN +'[+]'+bcolors.ENDC)+'Apache service started...\n'+bcolors.ENDC)

####to start apache service
def reloadtor():
	####to start tor service
	Popen(["service","tor","reload"])
	#output = p1.communicate()[0]
	#print(output)
	#call(["service","tor","reload"])
	print(bcolors.OKBLUE+(bcolors.OKGREEN +'[+]'+bcolors.ENDC)+'Tor service reloaded...\n'+bcolors.ENDC)
	####to start tor service

def showurl():
	#torsite=Popen('cat /var/lib/tor/hidden_service/hostname',shell=True,stdout=PIPE)
	print( bcolors.OKGREEN +'YOUR DARKNET DOMAIN:'+bcolors.ENDC )
	print( bcolors.OKGREEN +'---------------------------------'+bcolors.ENDC )
	call('cat /var/lib/tor/hidden_service/hostname',shell=True)
	print( bcolors.OKGREEN +'---------------------------------'+bcolors.ENDC )
	#with open('/Desktop/yourdarknetdomain.txt','w+') as ft:
	#			ft.writelines(call('cat /var/lib/tor/hidden_service/hostname',shell=True))
	#			print("present1")
	print(bcolors.FAIL+(bcolors.OKGREEN +'[+]'+bcolors.ENDC)+'Your website public files are located in /var/www/html\n'+bcolors.ENDC)


def main():
	header()
	ip=localip()
	print((bcolors.OKGREEN +'[+]'+bcolors.ENDC)+"Your local Ip : %r" %ip)
	edittorrc(ip)
	starttor()
	time.sleep(5)
	startapache()
	reloadtor()
	showurl()
	
if __name__=='__main__':
	main()

