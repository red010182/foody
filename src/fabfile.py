from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import cd
from fabric.contrib.files import exists


hosts = ['54.64.7.29']
env.user = 'ubuntu'
env.hosts = hosts
env.key_filename = '~/aws_key/japan2.pem'
env.always_yes = True

def hello():
    print("Hello world!")
def init():
	run('sudo apt-get update')
	run('sudo apt-get install -y git')
	run('sudo apt-get install -y python-mysqldb')
	if not exists('foody'):
		run('git clone https://github.com/red010182/foody.git')
	with cd('foody'):
		run('wget http://tpy.tw/db_config.txt')
def fixBug():
	run('mv db_config.txt foody/')
def pull():
	with cd('foody'):
		run('git pull origin master')
def downloadConfig():
	with cd('foody'):
		run('wget http://tpy.tw/db_config.txt')
	