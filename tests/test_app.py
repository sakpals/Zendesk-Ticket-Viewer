import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pytest
from urllib.request import urlopen, Request
from flask import url_for
from ticket_viewer.views import *
"""
NOTE: Before running tests, insure server is running in the background
 >> python3 run.py
"""

"""
Test whether server is running locally
"""
@pytest.mark.usefixtures('live_server')
def test_server_is_running(live_server):
	url = 'http://localhost:5000'
	request = Request(url)
	response = urlopen(request)
	assert response.code == 200

"""
Test API response codes for GET requests
"""
@pytest.mark.usefixtures('client')
def test_ticket_list(client):
	res = client.get(url_for('ticket_list'))
	assert res.status_code == 200

def test_ticket_list_page(client):
	assert client.get(url_for('ticket_list_page', page_num=3)).status_code == 200

def test_single_ticket_valid(client):
	assert client.get(url_for('single_ticket', page_num=1, ticket_id=10)).status_code == 200

"""
Test credentials by using the correct token for success and incorrent token
for failure
"""
def test_credentials(client):
	response = requests.get(url+'/tickets/', auth=(user, token)) 
	assert response.status_code == 200
	response = requests.get(url+'/tickets/', auth=(user, 'invalid_token')) 
	assert str(response.status_code)[0] in '345'

"""
Test whether:
-  page which should have tickets, displays exactly 25
- page (out of bounds) which doesn't have any tickets displays 0 tickets
"""
def test_get_page2_tickets(client):
	response, rendered = get_request(url+'/tickets/?page=2&per_page=25')
	data = response.json()
	assert len(data['tickets']) == 25
	assert data['previous_page'] == url+'/tickets.json?page=1&per_page=25'

def test_get_page100_tickets(client):
	response, rendered = get_request(url+'/tickets/?page=100&per_page=25')
	data = response.json()
	assert len(data['tickets']) == 0

"""
Test the contents of tickets (#10 and #100) which should be available
"""
def test_get_ticket_10(client):
	response, rendered = get_request(url+'/tickets/10.json')
	data = response.json()
	assert data['ticket']['subject'] == 'magna reprehenderit nisi est cillum'
	assert data['ticket']['submitter_id'] == 363080123654

def test_get_ticket_100(client):
	response, rendered = get_request(url+'/tickets/100.json')
	data = response.json()
	assert data['ticket']['subject'] == 'adipisicing duis quis consequat velit'
	assert data['ticket']['status'] == 'open'

"""
Test ticket which isn't available (e.g. there is no ticket #200)
"""
def test_get_ticket_200(client):
	response, rendered = get_request(url+'/tickets/200.json')
	assert response.status_code == 404



