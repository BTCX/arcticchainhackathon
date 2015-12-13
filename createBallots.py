import requests, json, pprint

host=""
user=""
pwd=""
port=
phrase=""

url="http://%s:%s@%s:%d" % (user, pwd, host, port)
headers={"content-type":"application/json"}

master_pub  = "mjcYqTLZ8zvFyJMyv7LMXzdNHj71mnyX8j"                    # Valmyndighetens public key
master      = "cSEgcVzRoQAoL65HgFwDPYf6FjRooS99SuWxncKvNmLF4seuZbUR"  # Valmyndighetens private key with 239 tBTC (somthing)

def getNewAddress():
#
# Returns a new address
#
  payload   = json.dumps({ "method" : "getnewaddress" , "params" : []})
  response  = requests.get(url, headers=headers, data=payload)
  address   = response.json()["result"]
  return address

def getPrivKey(pubAddress):
#
# Returns the private key of a public address
#
  payload   = json.dumps({ "method" : "dumpprivkey" , "params" : [pubAddress]})
  response  = requests.get(url, headers=headers, data=payload)
  address   = response.json()["result"]
  return address

def sendToAddress(address, amount):
#
# Returns a txid
#
  payload   = json.dumps({ "method" : "sendtoaddress" , "params" : [address, amount]})
  response  = requests.get(url, headers=headers, data=payload)
  txid      = response.json()["result"]
  return txid

def getBalance():
#
# Returns the balance of the wallet
#
  payload   = json.dumps({ "method" : "getbalance" , "params" : []})
  response  = requests.get(url, headers=headers, data=payload)
  balance   = response.json()["result"]
  return balance

def createMultisig(key1,key2):
#
# Returns a multisignature address and it's redeemscript
#
  payload       = json.dumps({ "method" : "createmultisig" , "params" : [2, [key1, key2]]})
  response      = requests.get(url, headers=headers, data=payload)
  multiAddress  = response.json()["result"]["address"]
  redeemScript  = response.json()["result"]["redeemScript"]
  return multiAddress, redeemScript

def openWallet():
#
# Decrypt the wallet for 10 seconds
#
  payload = json.dumps({ "method": "walletpassphrase" , "params" : [phrase, 10 ]})
  response = requests.get(url, headers=headers, data=payload)
  return

def closeWallet():
#
# Remove encryption key from memory and lock the wallet down.
#
  payload = json.dumps({ "method" : "walletlock" , "params": []})
  response = requests.get(url, headers=headers, data=payload)
  return

'''
def createRawTransaction(txid):
#
# CreateRawTransaction
#
  payload = json.dumps({ "method": "createrawtransaction" , "params" : [ [{"txid":txid, "vout":0}], {"mjcYqTLZ8zvFyJMyv7LMXzdNHj71mnyX8j":0.001} ]})
  response = requests.get(url, headers=headers, data=payload)
  pprint.pprint (response.json())
  return
'''

def createBallots(number, amount, master_pub):
#
# Number = how many ballots to create
# Amount = how much tBTC to load each ballots with
# Master = valmyndighetens privata nyckel
# Returns an array with prepaired ballots for the public to use
#
  if getBalance() < number * amount:
    return "Error: Not enough testcoins in wallet"
  else:
    ballotPrepared = []
    for i in range(number):
      ballot = getNewAddress()
      multiAddress, redeemScript = createMultisig(ballot,master_pub)
      openWallet()
      txid = sendToAddress(multiAddress, amount)
      ballot_priv = getPrivKey(ballot)
      closeWallet()
      ballotPrepared.append ([redeemScript, ballot_priv, txid])
#      createRawTransaction(txid)
  return ballotPrepared

result = createBallots(2, 1, master_pub)
print result

