import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from ticket_viewer import app as create_app
import pytest

@pytest.fixture
def app():
	new_app = create_app
	return new_app
