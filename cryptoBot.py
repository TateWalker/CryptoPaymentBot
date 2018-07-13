#cryptoBot.py
import requests
from CryptoPayments import CryptoPayments
import json
import time
import zulu
import sys

API_KEY     = sys.argv[3]
API_SECRET  = sys.argv[4]
GoogleKeyID = sys.argv[6]
GoogleKey = sys.argv[7]
from datetime import datetime, timezone
def exchangeRate(original,convert_to,time):
	time = str(zulu.parse(time)) #put in proper format
	time = time.replace('+00:00','Z')
	url = ('https://rest.coinapi.io/v1/exchangerate/'+str(original)+'/'+str(convert_to)+'?time='+str(time)) #get exchange rate from coinAPI
	headers = {'X-CoinAPI-Key' : sys.argv[5]}
	response = requests.get(url, headers=headers)
	body = response.json()
	# print(body['rate'])
	return body['rate']


## Parameters for your call, these are defined in the CoinPayments API Docs
## https://www.coinpayments.net/apidoc
# post_params = {
#     'amount' : 200,
#     'currency1' : 'USD',
#     'currency2' : 'BTC'
# }
client = CryptoPayments(API_KEY, API_SECRET)
# transaction = client.createTransaction(post_params)
# print(transaction)
# exit()
#CHANGE THIS
# print("Transaction Number: "+sys.argv[1])
# print("User: "+sys.argv[2])
# exit()
#CHANGE THIS
receiptNo = sys.argv[1]
# print(receiptNo)
# --------
tID = {'txid':receiptNo} #change this to input from bot
transaction_info = client.getTransactionInfo(tID) #get transaction id record from provided id
# --------

# print("Getting Transaction ID")
# print(transaction_info)

# --------
curCoin = transaction_info.coin
rate = exchangeRate(curCoin,'USD',transaction_info.time_created) #get exchange rate of coin received and usd
amountPaid = float(transaction_info.amountf)*rate
#uncomment everthing up to "Error" when full prices go in effect

# if sys.argv[8]: #theyre a founder
	if amountPaid > 199 and amountPaid < 201: #paying for firepit
		transactionType = "Fire Pit Purchases"
	elif amountPaid > 997 and amountPaid < 1001: #paying for voodoo hut
		transactionType = "Voodoo Hut Purchases"
	else:
		transactionType = "Error"
# else: #not a founder
# 	if amountPaid > 398 and amountPaid < 402: 
# 		transactionType = "Fire Pit Purchases"
# 	elif amountPaid > 1398 and amountPaid < 1403:
# 		transactionType = "Voodoo Hut Purchases"
# 	else:
# 		transactionType = "Error"
# --------

# print(time.time()-1296000) #they have 15 days to submit receipt
# print(transaction_info.time_created)
# print(str(transaction_info.amountf)+str(transaction_info.coin))

# --------
if transaction_info.time_created < (time.time()-1296000):
	timeCheck = False
	print("Receipt already used")
else:
	timeCheck = True
if transaction_info.status == 0:
	statusCheck = False
	print("Funds haven't been sent")
elif transaction_info.status == 2:
	statusCheck = True
	print("Funds awaiting nightly delivery")
elif transaction_info.status >=100:
	statusCheck = True
	print("Funds received!")
else:
	statusCheck = False
 	print('Issue with funds. Contact Kneedam')
# --------

if transactionType == "Error":
	print("Paid wrong amount. Contact Kneedam")
	exit()
# transaction_info.time_created goes below in arg3
# timeCheck = True
# statusCheck = True
import sheetsTest as sT
if timeCheck and statusCheck:
	present = sT.updateSheet(transactionType,tID['txid'],transaction_info.time,sys.argv[2],GoogleKeyID,GoogleKey)
	if not present:
		print(transactionType)