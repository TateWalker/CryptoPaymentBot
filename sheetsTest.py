import time
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
def updateSheet(spreadsheet,tID,startTime,user,GooglePrivateKeyID,GooglePrivateKey):
	#adding google keys to json file
	

	with open('client_secret.json','r') as json_file:
		data = json.load(json_file)
	data['private_key_id'] = GooglePrivateKeyID #adding secret keys to data struct temporarily
	data['private_key'] = GooglePrivateKey.replace("\\n","\n") #THIS IS SO IMPORTANT
	
	scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_dict(data,scopes=scope)
	
	gc = gspread.authorize(credentials)
	del data
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
	present = False
	value_list = wks.col_values(1)
	prev_value_list = preWks.col_values(1)
	for cell in value_list: #is value in current months list
		if cell == str(tID):
			present = True
			print('This receipt has already been redeemed this month')
	for cell in prev_value_list: #is value in previous months list
		if cell == str(tID):
			present = True
			print('This receipt was used last month')

	if not present:
		# endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime+2592000))
		# startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime))
		endTime = 99999;
		startTime = 11111;
		values = [tID,startTime,endTime,user]
		wks.append_row(values)
	return present

