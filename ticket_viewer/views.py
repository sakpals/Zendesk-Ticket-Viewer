from . import app
from flask import render_template, request
import requests

url = 'https://katsucat1.zendesk.com/api/v2'
user = 'sampadasakpal@hotmail.com'+'/token'
token = 'rmgm9bSehKgL09Eh2DJC98PNFZrgjOYqPQwzX0Zf'


@app.route('/')
def main():
	response = requests.get(url+'/tickets.json', auth=(user, token))
	
