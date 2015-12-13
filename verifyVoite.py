import requests, json, pprint

host=""
user=""
pwd=""
port=
phrase=""

url="http://%s:%s@%s:%d" % (user, pwd, host, port)
headers={"content-type":"application/json"}

CHARCOST_INVERSE=10**7

def verifyMyVote( txid ):
  payload   = json.dumps({ "method" : "gettransaction" , "params" : [txid]})
  response  = requests.get(url, headers=headers, data=payload)

  pprint.pprint ( response.json() ) 
  details   = response.json()["results"]["details"]
  dct={}  
  for detail in details:
    address, amount = detail["address"], detail["amount"]  
    dct[address]=amount
    pprint.pprint ( details )
  return dct

def getCharStr(addrDict):
#
# (address, amount)
#
  msg=""
  keys=addrDict.keys()
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

txid = "hello" # please populate this with a TXID. For the full release use the public key from the ballot instead.
getCharStr(verifyMyVote(txid))
