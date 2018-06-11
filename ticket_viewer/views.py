from . import app
from flask import render_template, request
import requests, os, sys

url = 'https://katsucat1.zendesk.com/api/v2'
user = 'sampadasakpal@hotmail.com'+'/token'
token = 'rmgm9bSehKgL09Eh2DJC98PNFZrgjOYqPQwzX0Zf'
curr_page_num = 1

def check_internet_connection():
	# check for internet connectivity
	if os.system("ping -c 3 google.com") == 1:
		return render_template('internet_disconnect.html')

@app.route('/')
def ticket_list():
	check_internet_connection()
	response = requests.get(url+'/tickets/?page=1&per_page=25', auth=(user, token))
	if response.status_code != 200:
			return render_template('ticket_disp_error.html')
	
	data = response.json()
	return render_template('ticket_list.html', ticket_list=data['tickets'],
		next_pg=data['next_page'], prev_pg=data['previous_page'], page_num=curr_page_num)

@app.route('/page/<page_num>')
def ticket_list_page(page_num):
	curr_page_num = int(page_num)
	response = requests.get(url+'/tickets/?page='+str(curr_page_num)+'&per_page=25', auth=(user, token))
	if response.status_code != 200:
			return render_template('ticket_disp_error.html')
	
	data = response.json()
	return render_template('ticket_list.html', ticket_list=data['tickets'],
		next_pg=data['next_page'], prev_pg=data['previous_page'], page_num=curr_page_num)

@app.route('/ticket/<ticket_id>')
def single_ticket(ticket_id):
	check_internet_connection()

	response = requests.get(url+'/tickets/'+str(ticket_id)+'.json', auth=(user, token))
	if response.status_code != 200:
		return render_template('ticket_disp_error.html') #probs customise it
	
	data = response.json()
	return render_template('ticket_full_details.html', ticket_info=data['ticket'])


