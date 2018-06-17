import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pytest
from urllib.request import urlopen, Request
from flask import url_for
from ticket_viewer.views import url, get_request, ticket_list, ticket_list_page, single_ticket

# before running tests, insure server is running in the background 

@pytest.mark.usefixtures('live_server')
def test_server_is_running(live_server):
	url = 'http://localhost:5000'
	request = Request(url)
	response = urlopen(request)
	assert response.code == 200

@pytest.mark.usefixtures('client')
def test_ticket_list(client):
	res = client.get(url_for('ticket_list'))
	assert res.status_code == 200

def test_ticket_list_page(client):
	assert client.get(url_for('ticket_list_page', page_num=3)).status_code == 200

def test_single_ticket_valid(client):
	assert client.get(url_for('single_ticket', page_num=1, ticket_id=10)).status_code == 200

def test_get_ticket_list_template(client):
	assert ticket_list() != ''

def test_get_page2_tickets(client):
	response, rendered = get_request(url+'/tickets/?page=2&per_page')
	data = response.json()
	assert data['tickets'] != []

def test_get_page100_tickets(client):
	response, rendered = get_request(url+'/tickets/?page=100&per_page')
	data = response.json()
	assert data['tickets'] == []

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

def test_get_ticket_200(client):
	response, rendered = get_request(url+'/tickets/200.json')
	assert response.status_code == 404



