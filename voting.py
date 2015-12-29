# -*- coding: UTF-8 -*-


import valurna, vtest2

'''
simple & ugly command line interface for casting example
votes using the voter class in vtest2
can be run from its own main class, or by passing an argument to
bitocracy.py
-k
'''


use_vtest=True

def main():

	myvote=""
	parties=valurna.loadPartyNames()
	
	loop=True
	while loop:
		print "Enter the number of the party you want to vote for,"
		print "or write in your own:"
		
		
		for i in range(len(parties)):
			print "%d: %s" %(i, parties[i])


		x=raw_input()
		if isint(x):
			n=int(x)
			if n in range(len(parties)):
				myvote=parties[n]
			else:
				print "There is no party nr "+str(n)
				myvote="nobody, I guess"
				
		else:		
			myvote=x
		
		print "Are you sure you want to vote for "+myvote+" (y/n)?"
			
		x=raw_input()
		
		if x=="y":
			loop=False
		else:
			print ""
	
	doVote(myvote)		
			
def doVote(msg):
	if use_vtest:
		vtest2.voter.pay(msg)
def isint(x):
	try:
		y=int(x)
		return True
	except:
		return False


if __name__=='__main__':
	main()
