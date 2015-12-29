#! /usr/bin/python

import sys, pprint
from sys import argv
import vtest2, connect, valurna, voting


'''
primary command line interface for my stuff,
takes one argument when called from the command line
invokes different functions in different files depending on this
-k
'''

def main():
	if len(argv)<2:
		sys.exit()
	
	if argv[1]=='vote-old':
		vtest2.voter.cliVote()
	elif argv[1]=='vote':
		voting.main()
	elif argv[1]=='show':
		vtest2.decodeCharTransactions()
	elif argv[1]=='show2':
		valurna.printVoteCount(True)
	elif argv[1]=='pay':
		print 'relaying funds to voting address'
		vtest2.fundVoter(vtest2.voter)
	elif argv[1]=='balance':
		vtest2.voter.printUnspent()
	elif argv[1]=='tot':
		r=connect.sendCommand('listreceivedbyaddress', [])
		pprint.pprint(r.json())
	elif argv[1]=='count':
		valurna.printVoteCount()
		
if  __name__=='__main__':
	main()
