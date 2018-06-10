from . import app
from flask import render_template, request
import requests

url = 'https://katsucat1.zendesk.com/api/v2'
user = 'sampadasakpal@hotmail.com'+'/token'
token = 'rmgm9bSehKgL09Eh2DJC98PNFZrgjOYqPQwzX0Zf'


@app.route('/')
def main():
	response = requests.get(url+'/tickets.json', auth=(user, token))
	
	if response.status_code != 200:
		return render_template('ticket_disp_error.html')
	
	data = response.json()
	
	return render_template('ticket_list.html', ticket_list=data['tickets'])
	
@app.route('/ticket/<ticket_id>') #/ticket/<id>
def single_ticket(ticket_id):
	print(ticket_id)
	return render_template('ticket_full_details.html')
