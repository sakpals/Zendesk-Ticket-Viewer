from . import app
from flask import render_template, request
import requests, os, sys, re

url = 'https://katsucat1.zendesk.com/api/v2'
user = 'sampadasakpal@hotmail.com'+'/token'
token = 'rmgm9bSehKgL09Eh2DJC98PNFZrgjOYqPQwzX0Zf'

def get_request(url):
	try:
		response = requests.get(url, auth=(user, token))
		return response, False
	except requests.exceptions.ConnectionError: 
		return render_template('internet_disconnect.html'), True
	except requests.exceptions.Timeout:
		return render_template('timeout_error.html'), True
	except requests.exceptions.SSLError:
		return render_template('SSL_error.html'), True
	except requests.exceptions.HTTPError:
		return render_template('HTTP_error.html'), True


def handle_error_response(code):
	if code == 401:
		return render_template('authentication_error.html')
	elif code == 404: # trying to get ticket that doesn't exist
		return render_template('phantom_ticket_error.html')
	elif code == 409:
		return render_template('merge_conflict_error.html')
	elif code == 422:
		return render_template('unprocessable_entity_error.html')
	elif code == 429:
		# wait and retry
		return render_template('rate_limit_error.html')
	elif str(code)[0] in '4':
		return render_template('unsuccessful_request_error.html')
	elif code == 503:
		# wait and retry
		return render_template('database_timeout_error.html')
	elif str(code)[0] in '5':
		return render_template('temp_warning.html')
	else:
		return render_template('uncaught_error.html')

@app.route('/')
def ticket_list():
	response, rendered = get_request(url+'/tickets/?page=1&per_page=25')
	if rendered:
		return response
	if response.status_code != 200:
			return handle_error_response(response.status_code)
	
	data = response.json()

	# in the case there are no tickets to display
	if len(data['tickets']) == 0:
		return render_template('no_tickets_error.html')

	# getting the current page
	if data['next_page']:
		curr_page = int(re.search('page=(\d+)', data['next_page']).group(1)) - 1
	elif data['previous_page']:
		curr_page = int(re.search('page=(\d+)', data['previous_page']).group(1)) + 1
	else:
		curr_page = 1

	return render_template('ticket_list.html', ticket_list=data['tickets'],
		next_pg=data['next_page'], prev_pg=data['previous_page'], page_num=curr_page)

@app.route('/page/<page_num>')
def ticket_list_page(page_num):
	curr_page = int(page_num)
	response, rendered = get_request(url+'/tickets/?page='+str(curr_page)+'&per_page=25')
	if rendered:
		return response
	if response.status_code != 200:
			return handle_error_response(response.status_code)
	data = response.json()
	
	# in the case there are no tickets to display
	if len(data['tickets']) == 0:
		return render_template('no_tickets_error.html')

	return render_template('ticket_list.html', ticket_list=data['tickets'],
		next_pg=data['next_page'], prev_pg=data['previous_page'], page_num=curr_page)

@app.route('/page=<page_num>?ticket=<ticket_id>')
def single_ticket(page_num, ticket_id):
	response, rendered = get_request(url+'/tickets/'+str(ticket_id)+'.json')
	if rendered:
		return response
	if response.status_code != 200:
		return handle_error_response(response.status_code)

	data = response.json()
	return render_template('ticket_full_details.html', ticket_info=data['ticket'], page_num=page_num)

