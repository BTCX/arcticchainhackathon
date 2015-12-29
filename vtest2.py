import requests, json, pprint
import sys, decimal

"""
Stuff I made for myself before joining the goobit team
mostly contains old code that was later refined in valurna.py
However also contains a Voter class with methods for casting
non-multisig votes for demo & testing purposes
 

"""

import connect, voteCli

DEBUG=False
CHARCOST_INVERSE=10.0**5
CHARCOST= (1/CHARCOST_INVERSE)
MINING_FEE=(1.0/10**3)
testTargetAddr='n2r9JaHfra9yVT1ttX2WVRcdQFLjpDSRsP'
garbageAddr=testTargetAddr;

def printTx(txid):
	donothing=True

def fundVoter(voter):
	c=connect.sendCommand("walletpassphrase", [connect.phrase, 1])
	#print c.json()
	d=connect.sendCommand("sendtoaddress", [voter.addr, 0.1])
	print d.json()
	
def loadCharAddrs():
	addrs=[]
	f=open('charAddrs.txt')
	for line in(f.readlines()):
		addrs.append(line.rstrip())
		
	return addrs
	
charAddrs=loadCharAddrs()

def printreadable(hexed):
	pprint.pprint(connect.sendCommand('decoderawtransaction', [hexed]).json())

def sentCharDebug():
	res=connect.sendCommand('listreceivedbyaddress', [])
	#pprint.pprint(res.json())
	#print 'first 5 char addrs are:'
	#for i in range(0, 5):
		#print charAddrs[i]
	print '\n addrs in lis received:'
	for r in res.json()['result']:
		#print r['address']
		for q in charAddrs[0:10]:
			ra=r['address'].rstrip()
			q=q.rstrip()
			
			print 'now comparing:'
			print ra
			#print len(r['address'])
			print q
			#print len(q)
			if ra==q:
				print '    match!'
			else:
				print 'no match'


def isCharAddr(addr):
	for c in charAddrs:
		c2=c.rstrip()
		addr2=addr.rstrip()
		if c2==addr2:
			return True
	return False
	
#returns list of transactions sent to char addrs	
def sentCharTxs():
		charTxs=[]
		res=connect.sendCommand('listtransactions', ['', 10000])
		for r in res.json()['result']:
			
			if isCharAddr(r['address']):
				#pprint.pprint(r['txid'])
				charTxs.append(r['txid'])
		charTxs=set(charTxs)
		return charTxs
#takes dictionary of outputs indexed by address

#returns message composed of char values in
#addresses in order of charAddrs
def getCharStr(addrDict):
	keys=addrDict.keys()
	msg=''
	for addr in charAddrs:
		if addr in keys:
			amount=addrDict[addr]['amount']
			charval=int(round((amount*CHARCOST_INVERSE)))

			if DEBUG:
				l=amount*CHARCOST_INVERSE
				print amount
				print charval
				print l
				print int(round(l))
				print ''
			msg+=chr(charval)
		else:
			return msg
			
def decodeCharTransactions():
	charTxs=sentCharTxs()
	
	for txid in charTxs:
		if validVote(txid):
			print('displaying vote with txid '+str(txid)+":")
			transaction=connect.sendCommand('gettransaction', [txid]).json()
			details=transaction['result']['details']
			
			addrSorted={}
			for x in details:
				if x['category']=='receive':
					a=x['address']
					addrSorted[a]=x
			msg=getCharStr(addrSorted)
			print(msg)
					
#should check if a txid belongs to a list of valid votes
#i.e is sent from an appropriate address
#currently simply returns True	
def validVote(txid):
	return True
	
	
	
class Voter():
	name='John Q Public'
	addr=''
	phrase=''
	
	def listUnspent(this):
		returns=[]
		res=connect.sendCommand('listunspent', [])
		for r in res.json()['result']:
			#print r
		
			if r['address']==this.addr:
				returns.append(r)
				
				
		return returns
		
	def printUnspent(this):
		pprint.pprint(this.listUnspent())

	#returns json
	def createRawT(this, message):
			inputSum=0
			inputs=[]
			for x in this.listUnspent():
				inputs.append({
					'txid':x['txid'],
					'vout':x['vout']
					})
				inputSum+=x['amount']
			#print inputs

			outputSum=0
			outputs={}
			
			i=0
			for char in message:
				if i <len(charAddrs):
					outputs[charAddrs[i]]=ord(char)*CHARCOST
					outputSum+=(ord(char)*CHARCOST)
					
					i+=1
				
			outputs[garbageAddr]=(inputSum-outputSum-MINING_FEE)


			r=connect.sendCommand('createrawtransaction', [inputs, outputs])
			
			if DEBUG:
				r2=connect.sendCommand('decoderawtransaction', [r.json()['result']])
				pprint.pprint(r2.json())
			
			return r
			
			
	#takes json from create raw transaction
	#returns json		
	def signRawT(this, rawt):
		r=connect.sendCommand('signrawtransaction', [rawt.json()['result']])
		#pprint.pprint(r.json())
		return r
	
	#takes signed raw transaction hex string as input
	#returns json
	def sendRawT(this, rawt):
		r=connect.sendCommand('sendrawtransaction', [rawt])
		return r
		
	def pay(this, message):
	
		this.sayPassphrase(2)
		
		rawt=this.createRawT(message)
		r= rawt.json()
		if r['error']!=None:
			print r['error']
			sys.exit()
		
		rj=this.signRawT(rawt).json()
		#pprint.pprint(r.json())
		error=rj['error']
		signed=rj['result']['hex']
		complete=rj['result']['complete']
	
	
		printreadable(signed)
		
		answ=raw_input("pay this? (y/n):\n")
		if(answ!='y'):
			print 'payment aborted'
			sys.exit()
	
		if(error!=None):
			print error
			return
		elif complete!=True:
			print 'incomplete'
			return
		else:
		
			
		
			print 'sending raw transaction now!'
			r=this.sendRawT(signed)	
			pprint.pprint(r.json())
			
			
			
	def sayPassphrase(this, t):
		connect.sendCommand('walletpassphrase', [this.phrase, t])
	
	
	def cliVote(this):
		msg=voteCli.doVote()
		this.pay(msg)
		
voter=Voter()
voter.name="Steve"
voter.addr='n2Be2i6pht24yLgaX3ewfjtzZavFaLgs9o'
voter.phrase=connect.phrase

#voter.pay("This is a test")
#pprint.pprint(loadCharAddrs())
#printSentToCharAddrs()

#decodeCharTransactions()
#sentChar2()
#voter.guiVote()

#fundVoter(voter)
