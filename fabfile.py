from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd
from fabric.contrib.files import exists


hosts = ['54.64.99.67','54.64.99.17','54.64.99.16','54.64.99.49','54.64.99.14','54.64.99.11','54.64.99.4','54.64.98.244']
env.user = 'ubuntu'
env.hosts = hosts
env.key_filename = '~/aws_key/japan2.pem'
env.always_yes = True

def hello():
    print("Hello world!")
def init():
	run('sudo apt-get install -y git')
	if not exists('foody'):
		run('git clone https://github.com/red010182/foody.git')
		cd('foody')
		run('wget http://tpy.tw/db_config.txt')
	else:
		cd('foody')
		run('wget http://tpy.tw/db_config.txt')	

def updateLocation():
	cd('foody')		
	i = 0
	for host in hosts:
		i += 1


