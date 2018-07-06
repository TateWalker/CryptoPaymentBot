import pygsheets
import time
import datetime

def updateSheet(spreadsheet,tID,startTime,user):
	# print(tID)
	import gspread
	from oauth2client.service_account import ServiceAccountCredentials
	# print(spreadsheet)
	scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

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
		endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime+2592000))
		startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime))
		values = [tID,startTime,endTime,user]
		wks.append_row(values)
	return present

