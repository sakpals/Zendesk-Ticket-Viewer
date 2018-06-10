from . import app
from flask import render_template, request
import requests, os, sys

url = 'https://katsucat1.zendesk.com/api/v2'
user = 'sampadasakpal@hotmail.com'+'/token'
token = 'rmgm9bSehKgL09Eh2DJC98PNFZrgjOYqPQwzX0Zf'


def check_internet_connection():
	# check for internet connectivity
	if os.system("ping -c 3 google.com") == 1:
		return render_template('internet_disconnect.html')

@app.route('/')
def main():
	check_internet_connection()

	if os.system("ping -c 5 google.com") == 1:
		return render_template('internet_disconnect.html')

	url = 'https://katsucat1.zendesk.com/api/v2/tickets.json'
	while url:
		response = requests.get(url+'?per_page=25', auth=(user, token))
		if response.status_code != 200:
			return render_template('ticket_disp_error.html')
	
		data = response.json()
		url = data['next_page']
		return render_template('ticket_list.html', ticket_list=data['tickets'])
	
	#response = requests.get(url+'/tickets.json', auth=(user, token))
	#if response.status_code != 200:
	#	return render_template('ticket_disp_error.html')
	
	#data = response.json()
	#return render_template('ticket_list.html', ticket_list=data['tickets'])

@app.route('/ticket/<ticket_id>')
def single_ticket(ticket_id):
	check_internet_connection()

	response = requests.get(url+'/tickets/'+str(ticket_id)+'.json', auth=(user, token))
	if response.status_code != 200:
		return render_template('ticket_disp_error.html') #probs customise it
	
	data = response.json()
	return render_template('ticket_full_details.html', ticket_info=data['ticket'])


