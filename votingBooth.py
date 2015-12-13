# -*- coding: UTF-8 -*-

import valurna


def createRawTransaction(txid, messageTransactions):
#
# CreateRawTransaction
#
  payload = json.dumps({
  	"method": "createrawtransaction" ,
  	"params" : [
  		[{"txid":txid, "vout":0}], 
  		messageTransactions
  	]
  })
  response = requests.get(url, headers=headers, data=payload)
  pprint.pprint (response.json())
  return

def signTransaction(rawTx, privKey):
#
# Returns a new address
#
  payload   = json.dumps({ "method" : "signrawtransaction" , "params" : [rawTx, privKey]})
  response  = requests.get(url, headers=headers, data=payload)
  partSignedRawTx   = response.json()["result"]
  return partSignedRawTx

def castBallot(ballot, candidate, real=True):

  if not real: candidate = '€' + candidate

  # Format: {key=asciiAddressToSpendTo: value=amoúntToSpend}
  messageTransactions = formatCharPayments(candidate)

  rawTx = createRawTransaction(messageTransactions)
  partSignedRawTx = signrawtransaction(rawTx, ballotPrivKey)

  return partSignedRawTx

  
def castGhostBallot(ballot1, ballot2, candidate):
  tx1 = castBallot(ballot1, candidate)
  tx2 = castBallot(ballot2, candidate, False)
  