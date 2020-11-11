#!/usr/bin/python3
import requests 
import json
from datetime import datetime
import sys

coin = ''
file_name_base = ''

def set_file_name_base(coin):
	return coin + '_'+datetime.now().strftime('%Y-%m-%d')	

def grab_historical_prices(coin):
	today = datetime.now().strftime("%Y%m%d")
	req = requests.get("https://coinmarketcap.com/currencies/"+coin+"/historical-data/?start=20130428&end="+today)
	cont = str(req.content)
	quotes = cont.find('"quotes"')
	topd = cont.find('"topDerivatives"')
	cont2 = cont[quotes:topd]
	obrac = cont2.find('[')
	cbrac = cont2.find(']')
	cont3 = cont2[obrac:cbrac+1]
	sonny = json.loads(cont3)
	
	file_name = file_name_base + '.json'
	outfile = open(file_name,'w')
	outfile.write(json.dumps(sonny,sort_keys=True,indent=4))
	outfile.close()

	return sonny

def make_csv_from_json(my_json,outfile_name):
	main_keys = my_json[1].keys()
	quote_keys = my_json[1]['quote']['USD'].keys()

	#Rough sanity check
	for row in my_json:
		if len(row.keys()) != len(main_keys) or len(row['quote']['USD'].keys()) != len(quote_keys):
			print('Key lengths are not all equal. Exiting') 
			exit()
	outfile = open(outfile_name,'w')

	#Populate header row
	lineout = ''
	for key in main_keys:
		if key != 'quote':
			lineout+=key+','
	for key in quote_keys:
		lineout+=key+','
	lineout = lineout[:-1]+'\n'
	outfile.write(lineout)

	#Populate remaining rows
	for row in my_json:
		lineout=''
		for key in main_keys:
			if key != 'quote':
				lineout+=str(row[key])+','

		for key in quote_keys:
			lineout+=str(row['quote']['USD'][key])+','
		lineout=lineout[:-1]+'\n'
		outfile.write(lineout)

	outfile.close()
		

def grab_and_make_csv(coin):
	sonny = grab_historical_prices(coin)
	file_name = file_name_base + '.csv'
	make_csv_from_json(sonny,file_name)

if __name__=='__main__':
	if (len(sys.argv) == 1):
		coin = "bitcoin"
	else:
		coin = sys.argv[1]
	file_name_base = set_file_name_base(coin)
	grab_and_make_csv(coin)

