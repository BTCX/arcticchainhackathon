import json
import jsonrpc
import requests, pprint


import requests, json, pprint
import sys

'''
contains a bunch of methods for connecting
to the bitcoin api used during the hackathon,
methods which are called from test2 & voting
(not needed in valurna, which has its own
api-interfacing methods)
-k
'''


host='193.15.170.35'
user='hackathon3'
pwd='duke-revolt'
port=18862
phrase='gully-come'


url=("http://%s:%s@%s:%d" % (user, pwd, host, port))
headers={'content-type':'application/json'}

#made valet?
#{u'error': None, u'id': None, u'result': u'mrHoctbTRmBCBAAoY9QUZcbZr6BfrKU9MH'}
#{u'error': None, u'id': None, u'result': u'mgqFGVV7yFqPAxkhaV5eDBsbMzjxbAxn5C'}


#this one actually tied to my account?
#{u'error': None, u'id': None, u'result': u'muoiZ6hUbPw2miGMiGFArgpNm1GKyzkDC1'}


#testtransactionid
#9560607a95d7cd20d58efc4bacca71b9f3717be748ab36f6f2b3730aa33a7a8e


def makeValetTest():
	payload=json.dumps({'method':'getnewaddress',
	'params':['']
	
	})
	response=sendPayload(payload)
	pprint.pprint(response.json())
	
	
def listTransTest():
	payload=json.dumps({
		'method':'listtransactions',
		'params':[]
	})
	response = requests.get(url, headers=headers, data=payload)
	pprint.pprint(response.json())

	
def sendPayload(payload):
		response = requests.get(url, headers=headers, data=payload)
		return response

def sendCommand1(command, param):
	payload=json.dumps({
		'method':command,
		'params':[param]
	})
	return sendPayload(payload)

def sendCommand(command, params):
	payload=json.dumps({
		'method':command,
		'params':params
	})
	return sendPayload(payload)

def actest():
	payload=json.dumps({
		'method':'getaccountaddress',
		'params': [""]
	})
	r=sendPayload(payload)
	
	q=r.json()
	

	
	print r.json()

def waletlocktest():
	payload=json.dumps({
		'method':'walletlock',
		'params': []
	})
	r=sendPayload(payload)	
	pprint.pprint( r.json())

def listacc():
	payload=json.dumps({
		'method':'listaccounts',
		'params':[1]
	
	})
	print(sendPayload(payload).json())

#listTransTest()
#actest()
#makeValetTest()

def transfertest():
	w=sendCommand('walletpassphrase', [phrase, 2])
	print w.json()
	r=sendCommand('sendfrom', ['', 'muoiZ6hUbPw2miGMiGFArgpNm1GKyzkDC1', 10.0,])
	print 'printing r.json()'
	print r.json()


def customCmd(cmd):
	r=None
	if cmd=="1":

		sys.exit()
	
	elif cmd=="2":
		makeLotsOfAddrs(32)
	
	elif cmd=='3':
		r=sendCommand('walletpassphrase', [phrase, 60])
	if r!=None:
		pprint.pprint(r.json())
		
	sys.exit()

def makeLotsOfAddrs(n):
	for i in range(0, n):
		n=sendCommand('getnewaddress',[])
		addr=n.json()['result']
		print addr
	
def main():
	argl=len(sys.argv)
	if argl==1:
		print 'no args, exiting\n'
		sys.exit()

	cmd=''
	params=[]
	if argl>1:
		cmd=sys.argv[1]
		
	if cmd=="foo":
		customCmd(sys.argv[2])
	if argl>2:
		params=sys.argv[2:argl]
		


	pprint.pprint(sendCommand(cmd, params).json())


if __name__=='__main__':
	main()
