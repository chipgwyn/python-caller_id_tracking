#!/usr/bin/env python

import sqlite3 as sqlite
from time import sleep, time
from serial import Serial, serialutil

### Define some settings
DB_FILE_NAME 	= 'calls.db'
SERIAL_PORT 	= '/dev/ttyACM0'
BAUD_RATE 		= 9600
TIMEOUT 		= 1 #seconds
INIT_STRING		= ''.join(['AT',  #http://support.usr.com/support/5637/5637-ug/ref_data.html
					'E0', # Disable local echo
					'M0', # Turn off the speaker
					'L0', # or at least set it to a really low volume
					'Q0', # Display result codes
					'V1', # Display verbal result codes
					'#CID=1', # Enable caller id
					])



def read_buffer(modem_object):
	''' read everything out of the buffer, return it '''
	response = str()
	while 1:
		sleep(1)
		data = modem_object.read(size=1000)
		if not data: 
			break
		else: 
			response = response + data
	return response
	


def clean_response(response):
	''' Removes line feeds, returns list of responses '''
	clean = list()
	response_parts = response.split('\r\n')
	for item in response_parts:
		if len(item) > 0:
			clean.append(item)
	return clean



def execute_cmd(modem_object, cmd_string):
	''' Sends a command to the device, returns "somewhat" formatted output '''

	modem_object.write(cmd_string + '\r')
	response = read_buffer(modem_object)
	return clean_response(response)



def init_modem(modem_object, init_string):
	response = execute_cmd(modem_object, init_string)
	if 'OK' in response:
		print '- Modem Initialized'
		return 1
	else:
		return 0



def display_call(response):
	data = dict()
	for item in response:
		if '=' in item:
			parts = item.split('=', 1)
			data[parts[0]] = parts[1]
	if len(data) > 1:
		print data



def insert_call(response):
	connection = sqlite.connect('calls.db')
	cur = connection.cursor()
	
	data = dict()
	for item in response:
		if '=' in item:
			parts = item.split('=', 1)
			data[parts[0]] = parts[1]
	
	if len(data) > 1:
		info = list()
		info.append(int(time()))
		info.append(data['NMBR'])
		info.append(data['NAME'])
		
		with connection:
			cur.execute('INSERT INTO CALLS(TIMESTAMP,NUMBER,NAME) VALUES(?,?,?)', info)

		

def call_poller(modem_object, callback_func):
	while 1:
		sleep(1)
		response = clean_response(read_buffer(modem_object))
		if response:
			callback_func(response)
		


def main():
	modem = Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
	read_buffer(modem)  # empty the buffer
	init_modem(modem, INIT_STRING)
	call_poller(modem, insert_call)

	

if __name__ == '__main__':
	main()

#fin!