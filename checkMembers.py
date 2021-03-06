# checkMembers.py
import time
import datetime
import sys
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
def checkMembers(spreadsheet,GooglePrivateKeyID,GooglePrivateKey):

	with open('client_secret.json','r') as json_file:
		data = json.load(json_file)
	data['private_key_id'] = GooglePrivateKeyID #adding secret keys to data struct temporarily
	data['private_key'] = GooglePrivateKey.replace("\\n","\n") #THIS IS SO IMPORTANT
	
	scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_dict(data,scopes=scope)
	
	gc = gspread.authorize(credentials)

	now = datetime.datetime.now()
	month = str(now.month)
	year = str(now.year)
	currentSheetTitle = (month+'/'+year)
	prevSheetTitle = (str(now.month-1)+'/'+year)

	sh = gc.open(spreadsheet) # Open a worksheet from spreadsheet with one shot
	try: #do we have one for this month yet
		wks = sh.worksheet(currentSheetTitle)
		preWks = sh.worksheet(prevSheetTitle)

	except:
		wks = sh.add_worksheet(currentSheetTitle,0,0)
		headers = ['Transaction ID','Date Purchased','Date Expired','User']
		wks.append_row(headers)
	
	users = preWks.col_values(4)
	expiration = preWks.col_values(3)
	expiredUsers = []
	del(expiration[0])
	del(users[0])
	for i in range(0,len(expiration)):
		expiration[i] = datetime.datetime.strptime(expiration[i], '%Y-%m-%d %H:%M:%S')
		if expiration[i] < now: #expired
			expiredUsers.append(users[i]) #add users to list of expired users
	curUsers = wks.col_values(4)
	del(curUsers[0])
	for i in expiredUsers:
		for j in curUsers: #they renewed
			if i == j:
				del[i] #remove them from expired users
	for i in expiredUsers:
		print(i)
def main(spreadsheet,GooglePrivateKeyID,GooglePrivateKey):
	checkMembers(spreadsheet,GooglePrivateKeyID,GooglePrivateKey)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2],sys.argv[3])