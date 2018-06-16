import pytest
from urllib.request import urlopen, Request
from flask import url_for
from ticket_viewer.views import ticket_list, ticket_list_page

# insure server is running in the background 

@pytest.mark.usefixtures('live_server')
def test_server_is_running(live_server):
	url = 'http://localhost:5000'
	request = Request(url)
	response = urlopen(request)
	assert response.code == 200

@pytest.mark.usefixtures('client')
def test_ticket_list(client):
	assert client.get(url_for('ticket_list')).status_code == 200

def test_ticket_list_page(client):
	assert client.get(url_for('ticket_list_page', page_num=3)).status_code == 200


	